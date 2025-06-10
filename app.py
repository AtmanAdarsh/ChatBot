from flask import Flask, render_template, request, jsonify, send_file, session, redirect, url_for
from flask_cors import CORS  # Importing CORS for omnichannel support
from cryptography.fernet import Fernet  # Importing Fernet for encryption
import os
import uuid
import logging
import sqlite3
from pathlib import Path
from flask_cors import CORS
from gtts import gTTS
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import datetime
import requests
import json
import numpy as np

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask App
app = Flask(__name__)
app.config["SESSION_COOKIE_SECURE"] = True  # Ensure secure session cookies
app.config['SECRET_KEY'] = os.urandom(24)  # Flask session key
FERNET_KEY = Fernet.generate_key()  # Separate Fernet key if needed
CORS(app, resources={r"/*": {"origins": "http://localhost:5000"}})  # Enable CORS for omnichannel support

# Paths & Directories
AUDIO_FOLDER = Path('static/audio')
DATABASE_PATH = Path('database.sqlite3')
UPLOAD_FOLDER = Path('static/uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Ensure Directories Exist
AUDIO_FOLDER.mkdir(parents=True, exist_ok=True)
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

# Initialize Chatbot
chatbot = ChatBot("TuktukBot", storage_adapter="chatterbot.storage.SQLStorageAdapter",
                  database_uri=f'sqlite:///{DATABASE_PATH}', read_only=True)

WEATHER_API_KEY = "eda605e0e1efdb94dedd7510610d88ad"
NEWS_API_KEY = "a6a6a0846ce8439792c4ea9de0a4fd68"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        # Logic to handle user login will go here
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        # Logic to handle user registration will go here
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/get_response', methods=['POST'])  # Endpoint for chatbot responses
def get_response():
    """Chatbot Response API with emotion analysis"""
    user_input = request.form.get('user_input', '').strip().lower()  # Get user input
    emotion = request.form.get('emotion', 'neutral')
    # Adjust response based on detected emotion
    if emotion in ['sad', 'angry']:
        response_text = get_empathetic_response(user_input, emotion)
    else:
        response_text = chatbot.get_response(user_input)  # Get response based on user input
    audio_filename = generate_audio(str(response_text))
    return jsonify({
        'response': str(response_text), 
        'audio_url': audio_filename,
        'emotion': emotion
    })

@app.route('/get_audio/<filename>')
def get_audio(filename):
    """Serve generated chatbot voice audio"""
    audio_path = AUDIO_FOLDER / filename
    if audio_path.exists():
        return send_file(audio_path, mimetype="audio/mpeg")
    logger.error(f"Audio file not found: {filename}")
    return jsonify({'error': 'Audio not found'}), 404

@app.route('/weather')  # Endpoint for weather data
def get_weather():
    """Get weather data based on coordinates"""
    try:
        lat = request.args.get('lat')
        lon = request.args.get('lon')
        
        # Update to use weatherstack API with direct city query
        url = f"http://api.weatherstack.com/current?access_key={WEATHER_API_KEY}&query={lat},{lon}&units=m"
        
        response = requests.get(url)
        data = response.json()
        
        if 'current' in data and 'location' in data:
            return jsonify({
                'temp': data['current']['temperature'],
                'city': data['location']['name'],
                'condition': data['current']['weather_descriptions'][0] if data['current']['weather_descriptions'] else 'Clear',
                'humidity': data['current']['humidity'],
                'wind_speed': data['current']['wind_speed']
            })
        else:
            error_msg = data.get('error', {}).get('info', 'Unknown error')
            logger.error(f"Weather API error: {error_msg}")
            return jsonify({'error': error_msg}), 500
            
    except Exception as e:
        logger.error(f"Weather API error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/news')  # Endpoint for news headlines
def get_news():
    """Get latest news headlines"""
    try:
        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}"
        response = requests.get(url)
        return jsonify(response.json())
    except Exception as e:
        logger.error(f"News API error: {e}")
        return jsonify({'error': 'Failed to fetch news'}), 500

def get_empathetic_response(user_input, emotion):
    """Generate empathetic responses based on user emotion"""
    empathy_responses = {
        'sad': [
            "I'm sorry you're feeling down. Would you like to talk about it?",
            "It's okay to feel sad sometimes. I'm here to listen.",
            "Remember that difficult times are temporary. How can I help?"
        ],
        'angry': [
            "I understand you're feeling frustrated. Let's work through this together.",
            "Your feelings are valid. Would you like to discuss what's bothering you?",
            "Take a deep breath. I'm here to help you process these emotions."
        ]
    }
    return np.random.choice(empathy_responses.get(emotion, [str(chatbot.get_response(user_input))]))

def cleanup_old_audio_files():
    """Clean up audio files older than 1 hour"""
    try:
        current_time = datetime.datetime.now()
        for file in AUDIO_FOLDER.glob("*.mp3"):
            if current_time - datetime.datetime.fromtimestamp(file.stat().st_mtime) > datetime.timedelta(hours=1):
                file.unlink()
    except Exception as e:
        logger.error(f"Cleanup error: {e}")

def generate_audio(text: str):
    """Convert chatbot text response into speech using gTTS"""
    try:
        cleanup_old_audio_files()
        tts = gTTS(text=text, lang='en', slow=False)
        filename = f"audio_{uuid.uuid4()}.mp3"
        audio_path = AUDIO_FOLDER / filename
        tts.save(str(audio_path))
        logger.info(f"Generated TTS file: {filename}")
        return filename
    except Exception as e:
        logger.error(f"Failed to generate audio: {e}")
        return None

def allowed_file(filename):
    """Check if uploaded file has allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
