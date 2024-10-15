
---

# Real-Time Translation System

**Real-Time Translation System** is a Flask-based web application that allows real-time speech-to-speech translation. The application takes audio input, converts it to text, translates the text into a target language, and plays back the translated speech. It also incorporates JavaScript for interactive elements on the front-end, enhancing user experience.

## Features

- **Real-Time Speech Recognition**: Captures user speech and converts it into text using the `SpeechRecognition` library.
- **Language Translation**: Translates recognized text into a target language using `Google Translate API`.
- **Text-to-Speech (TTS)**: Converts the translated text into speech using `gTTS` (Google Text-to-Speech).
- **Multi-Language Support**: Users can choose from a wide variety of input and output languages.
- **JavaScript Integration**: Utilizes JavaScript for front-end interaction such as triggering audio recording and handling translation requests dynamically.

## Technologies Used

- **Flask**: Python framework used for developing the web application.
- **Google Translate API**: Used for translating recognized speech into different languages.
- **SpeechRecognition**: Handles speech-to-text functionality.
- **gTTS (Google Text-to-Speech)**: Converts the translated text into spoken audio.
- **Pygame**: Used for playing back the generated audio from `gTTS`.
- **JavaScript**: Enhances user interaction on the web interface.
- **HTML/CSS**: Used for structuring and styling the front-end.

## Directory Structure

```
Real-Time-Translation-System/
│
├── flagged/                       # Folder for storing flagged data
├── flask_project/                  # Main project folder
├── static/
│   ├── script.js                   # JavaScript for front-end interactions
│   └── style.css                   # CSS file for styling the webpage
├── templates/
│   ├── home.html                   # HTML file for the main interface
│   └── index.html                  # Alternate HTML file (if applicable)
├── venv/                           # Python virtual environment folder
├── README.md                       # Project documentation
├── speech_to_text.py               # Python file handling speech recognition
├── tempCodeRunnerFile.py           # Temporary code file (IDE specific)
├── text.py                         # Handles text processing
└── translation.py                  # Handles the translation logic
```

## Installation

### Prerequisites

- Python 3.x
- pip
- Flask
- Googletrans
- SpeechRecognition
- gTTS
- Pygame

### Installation Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/freyr5736/Real-Time-Translation-System.git
   ```
   Navigate to the project directory:
   ```bash
   cd Real-Time-Translation-System
   ```

2. **Set Up Virtual Environment (Optional)**:
   It’s recommended to use a virtual environment to manage dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   Install the necessary Python libraries by running:
   ```bash
   pip install Flask googletrans==4.0.0-rc1 SpeechRecognition gTTS pygame
   ```

4. **Run the Application**:
   Start the Flask application:
   ```bash
   python app.py
   ```

5. **Access the Web Interface**:
   Open a browser and navigate to `http://127.0.0.1:5000/` to interact with the web application.

## JavaScript Integration

The `script.js` file located in the `static` folder handles client-side functionality such as triggering audio recordings, sending requests to the Flask backend, and dynamically updating the translation results.

### Example JavaScript Functionality:
- **Triggering Audio Input**: Captures audio input and sends it to the server for translation.
- **Handling Responses**: Dynamically displays translation results and plays back audio using the web interface.

## Usage

1. **Audio Input**: Press the "Record" button on the webpage to record your speech.
2. **Select Languages**: Choose the input and output languages from the provided dropdown menus.
3. **Translation**: Click the "Translate" button to get the speech translated.
4. **Output**: The application will play the translated speech using the gTTS library.

## Example Workflow

1. Speak into the microphone.
2. The application recognizes the speech and translates it into the chosen language.
3. The translated text is converted back into speech.
4. The translated speech is played back using Pygame.

