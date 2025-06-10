#Chatbot Web Application

## Overview
This project is a web-based chatbot application built with Flask. It integrates a conversational AI (ChatterBot), emotion-aware responses, text-to-speech, and additional features such as weather and news fetching. The application is designed to provide a user-friendly interface for chatting, shopping, and accessing real-time information.

## Main Features
- **Conversational Chatbot**: Uses ChatterBot with a SQLite backend for persistent, trainable conversations.
- **Emotion-Aware Responses**: Adjusts chatbot replies based on detected user emotion (e.g., empathetic responses for sadness or anger).
- **Text-to-Speech**: Converts chatbot responses to audio using Google Text-to-Speech (gTTS).
- **Weather Information**: Fetches current weather data using the Weatherstack API.
- **News Headlines**: Retrieves the latest news headlines via the NewsAPI.
- **Basic E-commerce Pages**: Includes placeholder pages for products, cart, checkout, login, and registration.
- **Audio File Management**: Automatically cleans up old audio files to save storage.

## Project Structure
- `app.py` — Main Flask application, API endpoints, and core logic.
- `requirements.txt` — Python dependencies for the project.
- `train.py`, `train_model.py`, `collect_data.py` — Scripts for training and managing the chatbot's data/models.
- `static/` — Static files (audio, uploads, etc.).
- `templates/` — HTML templates for web pages.
- `database.sqlite3` — SQLite database for ChatterBot storage.
- `smile_hand_model.h5` — (Optional) ML model file for emotion or gesture recognition.
- `app.log` — Application log file.

## Setup & Usage
1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Run the application:**
   ```bash
   python app.py
   ```
3. **Access the app:**
   Open your browser to `http://localhost:5000`

## Notes
- The project currently has compatibility issues with modern Python and ChatterBot/SQLAlchemy. See the codebase or README for troubleshooting.
- Some pages (products, cart, etc.) are placeholders and require further implementation.
- API keys for weather and news are hardcoded and may need to be replaced for production use.

#Thank You
