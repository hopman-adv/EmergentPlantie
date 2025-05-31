import requests
import sys
import random
import string
from datetime import datetime

class PlantExchangeAPITester:
    def __init__(self, base_url):
        self.base_url = base_url
        self.token = None
        self.tests_run = 0
        self.tests_passed = 0
        self.user_id = None
        self.username = None
        self.plant_id = None

    def run_test(self, name, method, endpoint, expected_status, data=None, params=None):
        """Run a single API test"""
        url = f"{self.base_url}/api/{endpoint}"
        headers = {'Content-Type': 'application/json'}
        if self.token:
            headers['Authorization'] = f'Bearer {self.token}'

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, params=params)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers)
            
            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    return success, response.json()
                except:
                    return success, {}
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                try:
                    print(f"Response: {response.json()}")
                except:
                    print(f"Response: {response.text}")
                return False, {}

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}

    def test_api_root(self):
        """Test API root endpoint"""
        success, response = self.run_test(
            "API Root",
            "GET",
            "",
            200
        )
        return success

    def test_register(self):
        """Test user registration"""
        # Generate random username to avoid conflicts
        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        self.username = f"testuser_{random_suffix}"
        
        success, response = self.run_test(
            "User Registration",
            "POST",
            "register",
            200,
            data={
                "username": self.username,
                "email": f"{self.username}@example.com",
                "password": "Test123!"
            }
        )
        
        if success and 'access_token' in response:
            self.token = response['access_token']
            return True
        return False

    def test_login(self):
        """Test user login"""
        success, response = self.run_test(
            "User Login",
            "POST",
            "login",
            200,
            data={
                "username": self.username,
                "password": "Test123!"
            }
        )
        
        if success and 'access_token' in response:
            self.token = response['access_token']
            return True
        return False

    def test_get_me(self):
        """Test get current user info"""
        success, response = self.run_test(
            "Get Current User",
            "GET",
            "me",
            200
        )
        
        if success and 'id' in response:
            self.user_id = response['id']
            print(f"User ID: {self.user_id}")
            return True
        return False

    def test_get_sample_images(self):
        """Test get sample images"""
        success, response = self.run_test(
            "Get Sample Images",
            "GET",
            "sample-images",
            200
        )
        
        if success and 'images' in response:
            self.sample_images = response['images']
            print(f"Found {len(self.sample_images)} sample images")
            return True
        return False

    def test_create_plant(self):
        """Test creating a new plant"""
        if not hasattr(self, 'sample_images') or not self.sample_images:
            print("No sample images available, using a default URL")
            photo_url = "https://images.pexels.com/photos/3076899/pexels-photo-3076899.jpeg"
        else:
            photo_url = self.sample_images[0]
        
        success, response = self.run_test(
            "Create Plant",
            "POST",
            "plants",
            200,
            data={
                "name": "Test Plant",
                "description": "This is a test plant",
                "price": 19.99,
                "photo_url": photo_url
            }
        )
        
        if success and 'id' in response:
            self.plant_id = response['id']
            print(f"Created plant with ID: {self.plant_id}")
            return True
        return False

    def test_get_plants(self):
        """Test getting all plants"""
        success, response = self.run_test(
            "Get All Plants",
            "GET",
            "plants",
            200
        )
        
        if success and isinstance(response, list):
            print(f"Found {len(response)} plants")
            return True
        return False

    def test_get_my_plants(self):
        """Test getting user's plants"""
        success, response = self.run_test(
            "Get My Plants",
            "GET",
            "plants/my",
            200
        )
        
        if success and isinstance(response, list):
            print(f"Found {len(response)} plants owned by current user")
            return True
        return False

    def test_like_plant(self):
        """Test liking a plant"""
        if not self.plant_id:
            print("No plant ID available for testing like functionality")
            return False
        
        success, response = self.run_test(
            "Like Plant",
            "POST",
            f"plants/{self.plant_id}/like",
            200
        )
        
        return success

    def test_get_plant_likes(self):
        """Test getting plant likes"""
        if not self.plant_id:
            print("No plant ID available for testing get likes functionality")
            return False
        
        success, response = self.run_test(
            "Get Plant Likes",
            "GET",
            f"plants/{self.plant_id}/likes",
            200
        )
        
        if success and 'likes_count' in response:
            print(f"Plant has {response['likes_count']} likes")
            return True
        return False

    def test_unlike_plant(self):
        """Test unliking a plant"""
        if not self.plant_id:
            print("No plant ID available for testing unlike functionality")
            return False
        
        success, response = self.run_test(
            "Unlike Plant",
            "DELETE",
            f"plants/{self.plant_id}/like",
            200
        )
        
        return success

def main():
    # Get backend URL from frontend .env
    backend_url = "https://50bbadb6-ccc3-4214-886c-e9d5ffa2b6cd.preview.emergentagent.com"
    
    print(f"Testing Plant Exchange API at: {backend_url}")
    
    # Setup tester
    tester = PlantExchangeAPITester(backend_url)
    
    # Run tests
    tests = [
        ("API Root", tester.test_api_root),
        ("User Registration", tester.test_register),
        ("Get Current User", tester.test_get_me),
        ("Get Sample Images", tester.test_get_sample_images),
        ("Create Plant", tester.test_create_plant),
        ("Get All Plants", tester.test_get_plants),
        ("Get My Plants", tester.test_get_my_plants),
        ("Like Plant", tester.test_like_plant),
        ("Get Plant Likes", tester.test_get_plant_likes),
        ("Unlike Plant", tester.test_unlike_plant),
        ("Login", tester.test_login)
    ]
    
    for test_name, test_func in tests:
        if not test_func():
            print(f"❌ {test_name} test failed, stopping tests")
            break
    
    # Print results
    print(f"\n📊 Tests passed: {tester.tests_passed}/{tester.tests_run}")
    return 0 if tester.tests_passed == tester.tests_run else 1

if __name__ == "__main__":
    sys.exit(main())
