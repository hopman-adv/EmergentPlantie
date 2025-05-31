from fastapi import FastAPI, APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
from datetime import datetime, timedelta
import jwt
import bcrypt

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# JWT settings
JWT_SECRET = "plant_exchange_secret_key_2025"
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Security
security = HTTPBearer()

# Models
class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    username: str
    email: str
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    created_at: datetime

class Plant(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    price: float
    photo_url: str
    owner_id: str
    owner_username: str
    likes_count: int = 0
    liked_by: List[str] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)

class PlantCreate(BaseModel):
    name: str
    description: str
    price: float
    photo_url: str

class PlantResponse(BaseModel):
    id: str
    name: str
    description: str
    price: float
    photo_url: str
    owner_id: str
    owner_username: str
    likes_count: int
    liked_by: List[str]
    created_at: datetime
    is_liked_by_user: bool = False

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

# Utility functions
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    user = await db.users.find_one({"id": user_id})
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return User(**user)

# Sample plant images for testing
SAMPLE_PLANT_IMAGES = [
    "https://images.pexels.com/photos/3076899/pexels-photo-3076899.jpeg",
    "https://images.pexels.com/photos/1005058/pexels-photo-1005058.jpeg",
    "https://images.unsplash.com/photo-1551893665-f843f600794e?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njd8MHwxfHNlYXJjaHwyfHxzdWNjdWxlbnRzfGVufDB8fHx8MTc0ODY4MTQwOHww&ixlib=rb-4.1.0&q=85",
    "https://images.pexels.com/photos/2132227/pexels-photo-2132227.jpeg",
    "https://images.pexels.com/photos/85773/pexels-photo-85773.jpeg",
    "https://images.pexels.com/photos/931177/pexels-photo-931177.jpeg",
    "https://images.unsplash.com/photo-1490750967868-88aa4486c946?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njl8MHwxfHNlYXJjaHwyfHxmbG93ZXJzfGVufDB8fHx8MTc0ODY4MTQxMnww&ixlib=rb-4.1.0&q=85",
    "https://images.unsplash.com/photo-1519378058457-4c29a0a2efac?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njl8MHwxfHNlYXJjaHwzfHxmbG93ZXJzfGVufDB8fHx8MTc0ODY4MTQxMnww&ixlib=rb-4.1.0&q=85"
]

# Routes
@api_router.get("/")
async def root():
    return {"message": "Plant Exchange API"}

@api_router.get("/sample-images")
async def get_sample_images():
    return {"images": SAMPLE_PLANT_IMAGES}

@api_router.post("/register", response_model=TokenResponse)
async def register(user_data: UserCreate):
    # Check if user exists
    existing_user = await db.users.find_one({"$or": [{"username": user_data.username}, {"email": user_data.email}]})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already registered")
    
    # Create user
    hashed_password = hash_password(user_data.password)
    user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hashed_password
    )
    
    await db.users.insert_one(user.dict())
    
    # Create token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@api_router.post("/login", response_model=TokenResponse)
async def login(user_data: UserLogin):
    user = await db.users.find_one({"username": user_data.username})
    if not user or not verify_password(user_data.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["id"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@api_router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return UserResponse(**current_user.dict())

@api_router.post("/plants", response_model=PlantResponse)
async def create_plant(plant_data: PlantCreate, current_user: User = Depends(get_current_user)):
    plant = Plant(
        name=plant_data.name,
        description=plant_data.description,
        price=plant_data.price,
        photo_url=plant_data.photo_url,
        owner_id=current_user.id,
        owner_username=current_user.username
    )
    
    await db.plants.insert_one(plant.dict())
    
    plant_response = PlantResponse(**plant.dict())
    return plant_response

@api_router.get("/plants", response_model=List[PlantResponse])
async def get_plants(current_user: User = Depends(get_current_user)):
    plants = await db.plants.find().to_list(1000)
    plant_responses = []
    
    for plant in plants:
        plant_response = PlantResponse(**plant)
        plant_response.is_liked_by_user = current_user.id in plant["liked_by"]
        plant_responses.append(plant_response)
    
    return plant_responses

@api_router.get("/plants/my", response_model=List[PlantResponse])
async def get_my_plants(current_user: User = Depends(get_current_user)):
    plants = await db.plants.find({"owner_id": current_user.id}).to_list(1000)
    return [PlantResponse(**plant) for plant in plants]

@api_router.post("/plants/{plant_id}/like")
async def like_plant(plant_id: str, current_user: User = Depends(get_current_user)):
    plant = await db.plants.find_one({"id": plant_id})
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    
    if current_user.id in plant["liked_by"]:
        raise HTTPException(status_code=400, detail="Plant already liked")
    
    # Add like
    await db.plants.update_one(
        {"id": plant_id},
        {
            "$push": {"liked_by": current_user.id},
            "$inc": {"likes_count": 1}
        }
    )
    
    return {"message": "Plant liked successfully"}

@api_router.delete("/plants/{plant_id}/like")
async def unlike_plant(plant_id: str, current_user: User = Depends(get_current_user)):
    plant = await db.plants.find_one({"id": plant_id})
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    
    if current_user.id not in plant["liked_by"]:
        raise HTTPException(status_code=400, detail="Plant not liked yet")
    
    # Remove like
    await db.plants.update_one(
        {"id": plant_id},
        {
            "$pull": {"liked_by": current_user.id},
            "$inc": {"likes_count": -1}
        }
    )
    
    return {"message": "Plant unliked successfully"}

@api_router.get("/plants/{plant_id}/likes")
async def get_plant_likes(plant_id: str, current_user: User = Depends(get_current_user)):
    plant = await db.plants.find_one({"id": plant_id})
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    
    # Check if current user owns this plant
    if plant["owner_id"] != current_user.id:
        raise HTTPException(status_code=403, detail="Only plant owner can view likes")
    
    # Get users who liked this plant
    liked_by_ids = plant["liked_by"]
    users = await db.users.find({"id": {"$in": liked_by_ids}}).to_list(1000)
    
    liked_by_users = [{"id": user["id"], "username": user["username"]} for user in users]
    
    return {
        "plant_id": plant_id,
        "likes_count": plant["likes_count"],
        "liked_by": liked_by_users
    }

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()