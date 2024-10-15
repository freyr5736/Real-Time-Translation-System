from flask import Flask, render_template, request, jsonify
from googletrans import Translator, LANGUAGES
import speech_recognition as sr
from gtts import gTTS
from gtts.lang import tts_langs  # Correct import for supported languages
import pygame
import os
import uuid
import time

# Initialize the Flask app (Flask is a web framework that lets you build web applications quickly)
app = Flask(__name__)

# Initialize the Translator object from googletrans to handle text translation
translator = Translator()

# Initialize the speech recognizer object from the SpeechRecognition library
recognizer = sr.Recognizer()

# Initialize Pygame's mixer to handle audio playback for text-to-speech
pygame.mixer.init()

# Retrieve supported languages for Google Text-to-Speech (gTTS) as a list of language codes
supported_tts_languages = tts_langs().keys()  # This method returns all supported languages for text-to-speech

# Route to render the main index page (this is the homepage for your web app)
@app.route('/')
def index():
    # Renders an HTML template called 'index.html', passing in the available languages for translation
    return render_template('index.html', languages=LANGUAGES)

# Route to handle text translation requests via a POST request
@app.route('/translate', methods=['POST'])
def translate_text():
    # Get JSON data from the request, extracting 'text', 'input_lang', and 'output_lang'
    data = request.json
    text = data.get('text', '')  # The text to be translated
    input_lang = data.get('input_lang', 'auto')  # Source language, default is 'auto' (automatic detection)
    output_lang = data.get('output_lang', 'en')  # Target language, default is English ('en')

    # If no text is provided, return an error response
    if not text:
        return jsonify({'translated_text': 'No text provided'}), 400

    # Detect the input language if 'auto' is selected, otherwise use the provided language
    if input_lang == 'auto':
        detected_lang = translator.detect(text).lang  # Automatically detect the language of the input text
    else:
        detected_lang = input_lang  # Use the provided input language

    try:
        # Perform the translation from detected/input language to the desired output language
        translation = translator.translate(text, src=detected_lang, dest=output_lang)
        # Return the translated text in JSON format
        return jsonify({'translated_text': translation.text})
    except Exception as e:
        # Handle any translation errors and log the exception
        print(f"Translation failed: {str(e)}")
        return jsonify({'translated_text': f"Translation failed: {str(e)}"}), 500

# Route to handle speech-to-text and translation
@app.route('/speech-to-translate', methods=['POST'])
def speech_to_translate():
    try:
        # Retrieve the target language for the translation from the form data (default is 'en' for English)
        target_language = request.form.get('target_language', 'en')
        print("Received a speech-to-text request")
        print(f"Target language for translation: {target_language}")

        # Start listening to the microphone input to capture audio
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)  # Adjust for background noise
            audio = recognizer.listen(source)  # Listen for speech and capture it

        # Recognize the speech using Google's speech recognition API
        speech_text = recognizer.recognize_google(audio)
        print(f"Recognized Speech: {speech_text}")

        # Try translating the recognized speech into the target language
        try:
            translation = translator.translate(speech_text, dest=target_language)
            translated_text = translation.text
            print(f"Translated Text: {translated_text}")
            # Return both the recognized speech and the translated text in JSON format
            return jsonify({'recognized_text': speech_text, 'translated_text': translated_text})
        except Exception as e:
            # Handle any translation errors and log the exception
            print(f"Translation failed: {str(e)}")
            return jsonify({'error': f"Translation failed: {str(e)}"}), 500

    except sr.UnknownValueError:
        # Handle the case where speech could not be understood
        return jsonify({'error': 'Could not understand the audio.'}), 400
    except sr.RequestError as e:
        # Handle API request errors
        return jsonify({'error': f'Could not request results; {e}'}), 500
    except Exception as e:
        # Catch any other unexpected errors
        print(f"Speech-to-text error: {str(e)}")
        return jsonify({'error': f"An error occurred: {str(e)}"}), 500

# Route to handle text-to-speech (TTS) requests
@app.route('/text-to-speech', methods=['POST'])
def text_to_speech():
    # Extract the text and language information from the request
    data = request.json
    text = data.get('text', '')  # The text to be converted into speech
    lang = data.get('lang', 'en')  # Language for the speech, default is English ('en')

    # If no text is provided, return an error response
    if not text:
        return jsonify({'error': 'No text provided'}), 400

    # Generate a unique filename for the MP3 file to store the speech audio
    file_path = f"{uuid.uuid4()}.mp3"

    try:
        # Ensure the specified language is supported by gTTS
        if lang not in supported_tts_languages:
            print(f"Language '{lang}' not supported for text-to-speech")
            return jsonify({'error': f"Language '{lang}' not supported for text-to-speech"}), 400

        # Stop any currently playing audio to avoid overlap
        if pygame.mixer.music.get_busy():
            print("Stopping currently playing audio...")
            pygame.mixer.music.stop()
            time.sleep(0.5)  # Wait for the mixer to release the file

        # Convert the provided text into speech using gTTS and save it as an MP3 file
        print(f"Converting text to speech with language: {lang}")
        tts = gTTS(text, lang=lang)
        tts.save(file_path)

        # Play the generated MP3 file using Pygame
        print(f"Playing MP3 file: {file_path}")
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()

        # Wait until the audio playback is finished
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)  # Wait in small intervals to check playback status

        # Attempt to delete the MP3 file after playback
        retry_count = 0
        max_retries = 5  # Number of times to try deleting the file if there are file access issues
        while os.path.exists(file_path) and retry_count < max_retries:
            try:
                print(f"Attempting to remove MP3 file after playback: {file_path}")
                os.remove(file_path)  # Delete the file
                print("File removed successfully.")
            except Exception as e:
                print(f"Retry {retry_count + 1}: Failed to remove MP3 file: {str(e)}")
                retry_count += 1
                time.sleep(1)  # Wait before retrying

        # If the file couldn't be deleted after multiple attempts, raise an error
        if retry_count == max_retries:
            print(f"Failed to remove MP3 file after {max_retries} retries.")
            raise Exception("Could not remove MP3 file.")

        # Return a success response after everything completes
        return jsonify({'success': True})
    except Exception as e:
        # Handle any errors that occur during text-to-speech processing
        print(f"Text-to-Speech failed: {str(e)}")
        return jsonify({'error': f"Text-to-Speech failed: {str(e)}"}), 500

# Main entry point to run the Flask application
if __name__ == '__main__':
    # Run the Flask app with debugging enabled (this allows you to see detailed error logs in development)
    app.run(debug=True)