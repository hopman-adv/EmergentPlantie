# 🌱 Plant Exchange

A social plant exchange platform where users can discover, like, and exchange plants in a Tinder-style interface.

## 🚀 Features

- **User Authentication**: Secure registration and login with JWT tokens
- **Plant Management**: Add plants with photos, descriptions, and prices
- **Social Discovery**: Browse plants in a beautiful grid layout
- **Like System**: Like/unlike plants similar to dating apps
- **Plant Analytics**: See who liked your plants
- **Sample Images**: Pre-loaded plant images for testing

## 🛠️ Tech Stack

- **Frontend**: React 18, Tailwind CSS
- **Backend**: FastAPI (Python), JWT Authentication
- **Database**: MongoDB
- **Image Handling**: URL-based with sample images

## 📋 Prerequisites

Before running this application locally, make sure you have:

- **Python 3.11+** installed
- **Node.js 18+** and **Yarn** package manager
- **MongoDB** running locally or MongoDB Atlas account
- **Git** for cloning the repository

## 🔧 Installation & Setup

### 1. Clone the Repository

```bash
git clone <your-github-repo-url>
cd plant-exchange
```

### 2. Backend Setup

#### Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

#### Environment Configuration

Create a `.env` file in the `backend` directory:

```bash
# backend/.env
MONGO_URL=mongodb://localhost:27017
DB_NAME=plant_exchange
```

**MongoDB Setup Options:**

**Option A: Local MongoDB**
```bash
# Install MongoDB locally
# macOS
brew install mongodb-community

# Ubuntu
sudo apt-get install mongodb

# Start MongoDB
mongod
```

**Option B: MongoDB Atlas (Cloud)**
1. Create account at [MongoDB Atlas](https://cloud.mongodb.com)
2. Create a new cluster
3. Get connection string and update `MONGO_URL` in `.env`

### 3. Frontend Setup

#### Install Dependencies

```bash
cd ../frontend
yarn install
```

#### Environment Configuration

Create a `.env` file in the `frontend` directory:

```bash
# frontend/.env
REACT_APP_BACKEND_URL=http://localhost:8001
```

## 🚀 Running the Application

### 1. Start Backend Server

```bash
cd backend
uvicorn server:app --host 0.0.0.0 --port 8001 --reload
```

The backend will be available at: http://localhost:8001

### 2. Start Frontend Development Server

```bash
cd frontend
yarn start
```

The frontend will be available at: http://localhost:3000

## 📱 Using the Application

### Getting Started

1. **Register**: Create a new account with username, email, and password
2. **Login**: Sign in with your credentials
3. **Add Plants**: Go to "Add Plant" section and create your first plant
4. **Discover**: Browse plants in the "Discover" section
5. **Like Plants**: Click the heart button to like plants
6. **My Plants**: View your plants and see who liked them

### Sample Data

The app includes 8 beautiful sample plant images for testing. When adding a plant, you can either:
- Paste your own image URL
- Click on one of the sample images to select it

## 🔗 API Endpoints

### Authentication
- `POST /api/register` - Register new user
- `POST /api/login` - User login
- `GET /api/me` - Get current user info

### Plants
- `GET /api/sample-images` - Get sample plant images
- `POST /api/plants` - Create new plant
- `GET /api/plants` - Get all plants
- `GET /api/plants/my` - Get current user's plants
- `POST /api/plants/{id}/like` - Like a plant
- `DELETE /api/plants/{id}/like` - Unlike a plant
- `GET /api/plants/{id}/likes` - Get plant likes (owner only)

## 🧪 Testing

### Backend API Testing

Test the backend endpoints:

```bash
# Test API root
curl http://localhost:8001/api/

# Test sample images
curl http://localhost:8001/api/sample-images
```

### Frontend Testing

The frontend includes:
- Responsive design for mobile and desktop
- Real-time like count updates
- Form validation
- Error handling

## 🛠️ Development

### Project Structure

```
plant-exchange/
├── backend/
│   ├── server.py          # FastAPI application
│   ├── requirements.txt   # Python dependencies
│   └── .env              # Backend environment variables
├── frontend/
│   ├── src/
│   │   ├── App.js        # Main React component
│   │   ├── App.css       # Styles
│   │   └── index.js      # React entry point
│   ├── package.json      # Node.js dependencies
│   ├── tailwind.config.js # Tailwind configuration
│   └── .env             # Frontend environment variables
└── README.md            # This file
```

### Key Components

**Backend (`server.py`):**
- User authentication with JWT
- Plant CRUD operations
- Like/unlike system
- MongoDB integration

**Frontend (`App.js`):**
- `AuthForm` - Registration/login
- `MainApp` - Main application layout
- `DiscoverPlants` - Plant discovery grid
- `AddPlant` - Plant creation form
- `MyPlants` - User's plants view
- `PlantCard` - Individual plant display

## 🎨 Styling

The app uses **Tailwind CSS** for styling with:
- Responsive grid layouts
- Green color scheme (plant theme)
- Hover effects and animations
- Mobile-first design

## 🔒 Security Features

- **JWT Authentication**: Secure token-based auth
- **Password Hashing**: Using bcrypt for secure password storage
- **CORS Configuration**: Proper cross-origin setup
- **Input Validation**: Pydantic models for API validation

## 🐛 Troubleshooting

### Common Issues

**Backend won't start:**
- Check if MongoDB is running
- Verify `.env` file exists with correct `MONGO_URL`
- Check if all Python dependencies are installed

**Frontend can't connect to backend:**
- Verify backend is running on port 8001
- Check `REACT_APP_BACKEND_URL` in frontend `.env`
- Ensure no firewall blocking the connection

**MongoDB connection issues:**
- For local MongoDB: ensure `mongod` service is running
- For MongoDB Atlas: verify connection string and network access

**Port conflicts:**
- If port 8001 or 3000 are busy, update the ports in commands and `.env` files

### Logs and Debugging

**Backend logs:**
- Check console output when running `uvicorn server:app`
- Add `print()` statements for debugging

**Frontend logs:**
- Check browser console for errors
- Network tab to verify API calls

## 🚀 Deployment

### Production Considerations

- Set up proper environment variables
- Use production MongoDB instance
- Configure CORS for production domains
- Add proper error logging
- Implement rate limiting
- Add input sanitization

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License.

## 🙋\u200d♂️ Support

If you encounter any issues:

1. Check this README for troubleshooting steps
2. Ensure all prerequisites are installed
3. Verify environment variables are set correctly
4. Check that both backend and frontend are running

