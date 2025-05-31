import React, { useState, useEffect } from 'react';
import './App.css';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Auth context
const AuthContext = React.createContext();

function App() {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token'));

  useEffect(() => {
    if (token) {
      // Verify token and get user info
      axios.get(`${API}/me`, {
        headers: { Authorization: `Bearer ${token}` }
      }).then(response => {
        setUser(response.data);
      }).catch(() => {
        localStorage.removeItem('token');
        setToken(null);
      });
    }
  }, [token]);

  const login = (newToken) => {
    localStorage.setItem('token', newToken);
    setToken(newToken);
  };

  const logout = () => {
    localStorage.removeItem('token');
    setToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, token, login, logout }}>
      <div className="App min-h-screen bg-gray-50">
        {user ? <MainApp /> : <AuthForm />}
      </div>
    </AuthContext.Provider>
  );
}

function AuthForm() {
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState({ username: '', email: '', password: '' });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const { login } = React.useContext(AuthContext);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const endpoint = isLogin ? '/login' : '/register';
      const data = isLogin 
        ? { username: formData.username, password: formData.password }
        : formData;

      const response = await axios.post(`${API}${endpoint}`, data);
      login(response.data.access_token);
    } catch (err) {
      setError(err.response?.data?.detail || 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="max-w-md w-full space-y-8 p-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            🌱 Plant Exchange
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            {isLogin ? 'Sign in to your account' : 'Create a new account'}
          </p>
        </div>
        
        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          <div className="rounded-md shadow-sm space-y-4">
            <input
              type="text"
              required
              className="relative block w-full px-3 py-2 border border-gray-300 rounded-md placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-green-500 focus:border-green-500"
              placeholder="Username"
              value={formData.username}
              onChange={(e) => setFormData({...formData, username: e.target.value})}
            />
            
            {!isLogin && (
              <input
                type="email"
                required
                className="relative block w-full px-3 py-2 border border-gray-300 rounded-md placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-green-500 focus:border-green-500"
                placeholder="Email"
                value={formData.email}
                onChange={(e) => setFormData({...formData, email: e.target.value})}
              />
            )}
            
            <input
              type="password"
              required
              className="relative block w-full px-3 py-2 border border-gray-300 rounded-md placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-green-500 focus:border-green-500"
              placeholder="Password"
              value={formData.password}
              onChange={(e) => setFormData({...formData, password: e.target.value})}
            />
          </div>

          {error && (
            <div className="text-red-600 text-sm text-center">{error}</div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 disabled:opacity-50"
          >
            {loading ? 'Loading...' : (isLogin ? 'Sign in' : 'Sign up')}
          </button>

          <div className="text-center">
            <button
              type="button"
              className="text-green-600 hover:text-green-500"
              onClick={() => setIsLogin(!isLogin)}
            >
              {isLogin ? "Don't have an account? Sign up" : 'Already have an account? Sign in'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

function MainApp() {
  const [currentView, setCurrentView] = useState('discover');
  const { user, logout } = React.useContext(AuthContext);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation */}
      <nav className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-green-600">🌱 Plant Exchange</h1>
            </div>
            
            <div className="flex items-center space-x-4">
              <button
                onClick={() => setCurrentView('discover')}
                className={`px-3 py-2 rounded-md text-sm font-medium ${
                  currentView === 'discover' 
                    ? 'bg-green-100 text-green-700' 
                    : 'text-gray-500 hover:text-gray-700'
                }`}
              >
                Discover
              </button>
              
              <button
                onClick={() => setCurrentView('add')}
                className={`px-3 py-2 rounded-md text-sm font-medium ${
                  currentView === 'add' 
                    ? 'bg-green-100 text-green-700' 
                    : 'text-gray-500 hover:text-gray-700'
                }`}
              >
                Add Plant
              </button>
              
              <button
                onClick={() => setCurrentView('my-plants')}
                className={`px-3 py-2 rounded-md text-sm font-medium ${
                  currentView === 'my-plants' 
                    ? 'bg-green-100 text-green-700' 
                    : 'text-gray-500 hover:text-gray-700'
                }`}
              >
                My Plants
              </button>
              
              <div className="flex items-center space-x-2">
                <span className="text-sm text-gray-600">Hello, {user?.username}!</span>
                <button
                  onClick={logout}
                  className="text-sm text-red-600 hover:text-red-500"
                >
                  Logout
                </button>
              </div>
            </div>
          </div>
        </div>
      </nav>

      {/* Content */}
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        {currentView === 'discover' && <DiscoverPlants />}
        {currentView === 'add' && <AddPlant />}
        {currentView === 'my-plants' && <MyPlants />}
      </main>
    </div>
  );
}

function DiscoverPlants() {
  const [plants, setPlants] = useState([]);
  const [loading, setLoading] = useState(true);
  const { token } = React.useContext(AuthContext);

  useEffect(() => {
    fetchPlants();
  }, []);

  const fetchPlants = async () => {
    try {
      const response = await axios.get(`${API}/plants`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setPlants(response.data);
    } catch (error) {
      console.error('Error fetching plants:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleLike = async (plantId, isLiked) => {
    try {
      if (isLiked) {
        await axios.delete(`${API}/plants/${plantId}/like`, {
          headers: { Authorization: `Bearer ${token}` }
        });
      } else {
        await axios.post(`${API}/plants/${plantId}/like`, {}, {
          headers: { Authorization: `Bearer ${token}` }
        });
      }
      fetchPlants(); // Refresh plants
    } catch (error) {
      console.error('Error liking plant:', error);
    }
  };

  if (loading) {
    return <div className="text-center py-8">Loading plants...</div>;
  }

  return (
    <div className="px-4 sm:px-0">
      <h2 className="text-2xl font-bold mb-6">Discover Plants</h2>
      
      {plants.length === 0 ? (
        <div className="text-center py-8 text-gray-500">
          No plants available yet. Be the first to add one!
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {plants.map(plant => (
            <PlantCard
              key={plant.id}
              plant={plant}
              onLike={() => handleLike(plant.id, plant.is_liked_by_user)}
            />
          ))}
        </div>
      )}
    </div>
  );
}

function PlantCard({ plant, onLike, showLikes = false }) {
  const { user } = React.useContext(AuthContext);
  const isOwner = plant.owner_id === user?.id;

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden">
      <img
        src={plant.photo_url}
        alt={plant.name}
        className="w-full h-48 object-cover"
      />
      
      <div className="p-4">
        <div className="flex justify-between items-start mb-2">
          <h3 className="text-lg font-semibold">{plant.name}</h3>
          <span className="text-lg font-bold text-green-600">${plant.price}</span>
        </div>
        
        <p className="text-gray-600 text-sm mb-3">{plant.description}</p>
        
        <div className="flex justify-between items-center text-sm text-gray-500 mb-3">
          <span>By {plant.owner_username}</span>
          <span>{plant.likes_count} likes</span>
        </div>

        {showLikes && plant.liked_by && plant.liked_by.length > 0 && (
          <div className="mb-3">
            <p className="text-sm font-medium mb-1">Liked by:</p>
            <div className="flex flex-wrap gap-1">
              {plant.liked_by.map(user => (
                <span key={user.id} className="bg-green-100 text-green-700 text-xs px-2 py-1 rounded">
                  {user.username}
                </span>
              ))}
            </div>
          </div>
        )}
        
        {!isOwner && (
          <button
            onClick={onLike}
            className={`w-full py-2 px-4 rounded-md text-sm font-medium transition-colors ${
              plant.is_liked_by_user
                ? 'bg-red-100 text-red-700 hover:bg-red-200'
                : 'bg-green-100 text-green-700 hover:bg-green-200'
            }`}
          >
            {plant.is_liked_by_user ? '💔 Unlike' : '❤️ Like'}
          </button>
        )}
      </div>
    </div>
  );
}

function AddPlant() {
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    price: '',
    photo_url: ''
  });
  const [sampleImages, setSampleImages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const { token } = React.useContext(AuthContext);

  useEffect(() => {
    // Fetch sample images
    axios.get(`${API}/sample-images`).then(response => {
      setSampleImages(response.data.images);
    });
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setSuccess(false);

    try {
      await axios.post(`${API}/plants`, {
        ...formData,
        price: parseFloat(formData.price)
      }, {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      setFormData({ name: '', description: '', price: '', photo_url: '' });
      setSuccess(true);
    } catch (error) {
      console.error('Error creating plant:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="px-4 sm:px-0 max-w-2xl">
      <h2 className="text-2xl font-bold mb-6">Add New Plant</h2>
      
      {success && (
        <div className="mb-4 p-4 bg-green-100 border border-green-400 text-green-700 rounded">
          Plant added successfully!
        </div>
      )}
      
      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Plant Name
          </label>
          <input
            type="text"
            required
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-green-500 focus:border-green-500"
            value={formData.name}
            onChange={(e) => setFormData({...formData, name: e.target.value})}
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Description
          </label>
          <textarea
            required
            rows={3}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-green-500 focus:border-green-500"
            value={formData.description}
            onChange={(e) => setFormData({...formData, description: e.target.value})}
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Price ($)
          </label>
          <input
            type="number"
            step="0.01"
            required
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-green-500 focus:border-green-500"
            value={formData.price}
            onChange={(e) => setFormData({...formData, price: e.target.value})}
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Photo URL
          </label>
          <input
            type="url"
            required
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-green-500 focus:border-green-500"
            placeholder="Or choose from samples below"
            value={formData.photo_url}
            onChange={(e) => setFormData({...formData, photo_url: e.target.value})}
          />
        </div>

        {/* Sample Images */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Or choose from sample images:
          </label>
          <div className="grid grid-cols-4 gap-2">
            {sampleImages.map((imageUrl, index) => (
              <img
                key={index}
                src={imageUrl}
                alt={`Sample ${index + 1}`}
                className={`w-full h-20 object-cover rounded cursor-pointer border-2 ${
                  formData.photo_url === imageUrl ? 'border-green-500' : 'border-gray-200'
                }`}
                onClick={() => setFormData({...formData, photo_url: imageUrl})}
              />
            ))}
          </div>
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 disabled:opacity-50"
        >
          {loading ? 'Adding Plant...' : 'Add Plant'}
        </button>
      </form>
    </div>
  );
}

function MyPlants() {
  const [plants, setPlants] = useState([]);
  const [loading, setLoading] = useState(true);
  const [plantLikes, setPlantLikes] = useState({});
  const { token } = React.useContext(AuthContext);

  useEffect(() => {
    fetchMyPlants();
  }, []);

  const fetchMyPlants = async () => {
    try {
      const response = await axios.get(`${API}/plants/my`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setPlants(response.data);
      
      // Fetch likes for each plant
      for (const plant of response.data) {
        fetchPlantLikes(plant.id);
      }
    } catch (error) {
      console.error('Error fetching my plants:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchPlantLikes = async (plantId) => {
    try {
      const response = await axios.get(`${API}/plants/${plantId}/likes`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setPlantLikes(prev => ({
        ...prev,
        [plantId]: response.data.liked_by
      }));
    } catch (error) {
      console.error('Error fetching plant likes:', error);
    }
  };

  if (loading) {
    return <div className="text-center py-8">Loading your plants...</div>;
  }

  return (
    <div className="px-4 sm:px-0">
      <h2 className="text-2xl font-bold mb-6">My Plants</h2>
      
      {plants.length === 0 ? (
        <div className="text-center py-8 text-gray-500">
          You haven't added any plants yet.
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {plants.map(plant => (
            <PlantCard
              key={plant.id}
              plant={{
                ...plant,
                liked_by: plantLikes[plant.id] || []
              }}
              showLikes={true}
            />
          ))}
        </div>
      )}
    </div>
  );
}

export default App;