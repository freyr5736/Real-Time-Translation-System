import speech_recognition as sr  # Import the speech recognition library
from googletrans import Translator  # Import the Google Translator
from gtts import gTTS  # Import Google Text-to-Speech
from playsound import playsound  # Import playsound for playing the audio
import os  # Import os for file handling (removing the audio file)

# List of available language codes for Google Translate
language_codes = {
    'Afrikaans': 'af', 'Albanian': 'sq', 'Amharic': 'am', 'Arabic': 'ar',
    'Armenian': 'hy', 'Azerbaijani': 'az', 'Basque': 'eu', 'Belarusian': 'be',
    'Bengali': 'bn', 'Bosnian': 'bs', 'Bulgarian': 'bg', 'Catalan': 'ca',
    'Cebuano': 'ceb', 'Chinese (Simplified)': 'zh-CN', 'Chinese (Traditional)': 'zh-TW',
    'Corsican': 'co', 'Croatian': 'hr', 'Czech': 'cs', 'Danish': 'da',
    'Dutch': 'nl', 'English': 'en', 'Esperanto': 'eo', 'Estonian': 'et',
    'Filipino': 'tl', 'Finnish': 'fi', 'French': 'fr', 'Frisian': 'fy',
    'Galician': 'gl', 'Georgian': 'ka', 'German': 'de', 'Greek': 'el',
    'Gujarati': 'gu', 'Haitian Creole': 'ht', 'Hausa': 'ha', 'Hawaiian': 'haw',
    'Hebrew': 'he', 'Hindi': 'hi', 'Hmong': 'hmn', 'Hungarian': 'hu',
    'Icelandic': 'is', 'Igbo': 'ig', 'Indonesian': 'id', 'Irish': 'ga',
    'Italian': 'it', 'Japanese': 'ja', 'Javanese': 'jw', 'Kannada': 'kn',
    'Kazakh': 'kk', 'Khmer': 'km', 'Korean': 'ko', 'Kurdish (Kurmanji)': 'ku',
    'Kyrgyz': 'ky', 'Lao': 'lo', 'Latin': 'la', 'Latvian': 'lv',
    'Lithuanian': 'lt', 'Luxembourgish': 'lb', 'Macedonian': 'mk', 'Malagasy': 'mg',
    'Malay': 'ms', 'Malayalam': 'ml', 'Maltese': 'mt', 'Maori': 'mi',
    'Marathi': 'mr', 'Mongolian': 'mn', 'Myanmar (Burmese)': 'my', 'Nepali': 'ne',
    'Norwegian': 'no', 'Pashto': 'ps', 'Persian': 'fa', 'Polish': 'pl',
    'Portuguese': 'pt', 'Punjabi': 'pa', 'Romanian': 'ro', 'Russian': 'ru',
    'Samoan': 'sm', 'Scots Gaelic': 'gd', 'Serbian': 'sr', 'Sesotho': 'st',
    'Shona': 'sn', 'Sindhi': 'sd', 'Sinhala': 'si', 'Slovak': 'sk',
    'Slovenian': 'sl', 'Somali': 'so', 'Spanish': 'es', 'Sundanese': 'su',
    'Swahili': 'sw', 'Swedish': 'sv', 'Tajik': 'tg', 'Tamil': 'ta',
    'Telugu': 'te', 'Thai': 'th', 'Turkish': 'tr', 'Ukrainian': 'uk',
    'Urdu': 'ur', 'Uzbek': 'uz', 'Vietnamese': 'vi', 'Welsh': 'cy',
    'Xhosa': 'xh', 'Yiddish': 'yi', 'Yoruba': 'yo', 'Zulu': 'zu'
}

# Display the language codes to the user
print("Available languages for translation:")
for language, code in language_codes.items():
    print(f"{language}: '{code}'")

# Prompt the user to select the target language (the language to translate into)
target_language = input("Enter the language code you want to translate to (e.g., 'fr' for French, 'es' for Spanish): ").strip()

# Instantiate the recognizer and translator objects
r = sr.Recognizer()  # Create a Recognizer object for speech recognition
translator = Translator()  # Create a Translator object for translating text

while True:
    # Use the microphone as the audio source
    with sr.Microphone() as source:
        print("Speak Now")
        audio = r.listen(source)  # Listen to the user's speech and store it in the audio variable
        
        try:
            # Recognize speech using Google Speech Recognition, automatically detecting the language
            speech_text = r.recognize_google(audio)  # Convert the audio to text without specifying source language
            print(f"You said:", speech_text)
            
            # Check if the user wants to end the translation loop
            if speech_text.lower() == "exit":  # Convert speech to lowercase to handle variations
                break  # Exit the loop if the user says "exit"
            
            # Translate the recognized text to the chosen language
            translate_text = translator.translate(speech_text, dest=target_language).text  # Translate the text
            print(f"Translated to {target_language}:", translate_text)
            
        except sr.UnknownValueError:
            # Handle case where speech is unintelligible
            print("Could not understand the audio.")
            translate_text = None  # Set translate_text to None if recognition fails
        except sr.RequestError as e:
            # Handle case where there is a problem with the API request
            print(f"Could not request results; {e}")
            translate_text = None  # Set translate_text to None if API request fails
        except Exception as e:
            # Handle any other exceptions
            print(f"An error occurred: {e}")
            translate_text = None  # Set translate_text to None if any other error occurs

        if translate_text:  # Ensure translation was successful before proceeding
            # Convert the translated text to speech
            voice = gTTS(translate_text, lang=target_language)  # Generate speech from the translated text
            voice.save("voice.mp3")  # Save the speech to an MP3 file
            
            # Play the generated speech
            playsound("voice.mp3")  # Play the MP3 file
            os.remove("voice.mp3")  # Remove the MP3 file after playing to avoid clutter
        else:
            print("Translation failed, no audio will be played.")  # Inform the user if translation failed
