// Wait until the entire DOM (Document Object Model) is fully loaded before running the script
document.addEventListener('DOMContentLoaded', () => {
    // Select HTML elements by their IDs to interact with them later
    const textInput = document.getElementById('text-input'); // Text input for user text
    const translatedText = document.getElementById('translated-text'); // Display area for translated text
    const inputLangSelect = document.getElementById('input-language-select'); // Dropdown for selecting input language
    const outputLangSelect = document.getElementById('output-language-select'); // Dropdown for selecting output language
    const swapButton = document.getElementById('swap-btn'); // Button to swap input and output languages
    const micButton = document.getElementById('mic-btn'); // Button to start speech recognition
    const resetButton = document.getElementById('reset-btn'); // Button to reset inputs (not used in code)
    const speakerButton = document.getElementById('speaker-btn'); // Button to play the translated text as speech

    // Variable to manage the debounce timer
    let debounceTimer;

    // List of languages that do not support Text-to-Speech (TTS) functionality
    const languagesWithoutTTS = [
        'ku', // Kurdish
        'la', // Latin
        'ml', // Malayalam
        'ne', // Nepali
        'si', // Sinhala
        'sr', // Serbian
        'sw', // Swahili
        'xh', // Xhosa
        'yi'  // Yiddish
    ];
    
    // Function to handle text translation
    const translateText = async () => {
        // Get user input, input language, and output language
        const text = textInput.value.trim(); // Trim whitespace from input text
        const inputLang = inputLangSelect.value; // Selected input language
        const outputLang = outputLangSelect.value; // Selected output language

        // If the input text is empty, clear the translated text area and exit the function
        if (text === '') {
            translatedText.value = '';
            return;
        }

        // Log the translation process for debugging purposes
        console.log(`Translating: "${text}" from "${inputLang}" to "${outputLang}"`);

        try {
            // Send a POST request to the server for translation
            const response = await fetch('/translate', {
                method: 'POST', // Specify the HTTP method
                headers: {
                    'Content-Type': 'application/json', // Set the content type to JSON
                },
                body: JSON.stringify({
                    text: text, // Text to translate
                    input_lang: inputLang, // Input language
                    output_lang: outputLang, // Output language
                }),
            });

            // Check if the response from the server is not OK (e.g., error)
            if (!response.ok) {
                const errorData = await response.json(); // Parse the error response
                console.error('Error response:', errorData); // Log the error for debugging
                translatedText.value = 'Error: ' + (errorData.translated_text || 'Translation Error'); // Display error message
                return; // Exit the function
            }

            // Parse the successful response
            const data = await response.json();
            // If translated text is available, display it; otherwise, show an error
            if (data.translated_text) {
                translatedText.value = data.translated_text; // Set the translated text
                console.log('Translated Text:', data.translated_text); // Log the translated text
            } else {
                translatedText.value = 'Translation Error'; // Handle case when translation fails
            }
        } catch (error) {
            // Log any error that occurs during the fetch operation
            console.error('Error:', error);
            translatedText.value = 'Error: ' + error.message; // Display the error message
        }
    };

    // Debounce function to limit the rate of translation requests
    const debounce = (func, delay) => {
        return () => {
            clearTimeout(debounceTimer); // Clear any previous timer
            debounceTimer = setTimeout(func, delay); // Set a new timer for the function call
        };
    };

    // Add an event listener to the text input to trigger translation on input with debounce
    textInput.addEventListener('input', debounce(translateText, 500));

    // Add an event listener to the swap button to switch input and output languages
    swapButton.addEventListener('click', () => {
        const tempLang = inputLangSelect.value; // Store the current input language temporarily
        inputLangSelect.value = outputLangSelect.value; // Set input language to output language
        outputLangSelect.value = tempLang; // Set output language to the original input language

        // If the input text is not empty, trigger translation
        if (textInput.value.trim() !== '') {
            translateText();
        }
    });

    // Add an event listener to the mic button to handle speech recognition
    micButton.addEventListener('click', async () => {
        micButton.classList.add('active'); // Add an active class for visual feedback
        try {
            // Send a request to start speech recognition for translation
            const response = await fetch('/speech-to-translate', {
                method: 'POST',
                body: new URLSearchParams({
                    target_language: outputLangSelect.value, // Send the target language for recognition
                }),
            });

            const data = await response.json();
            // If recognized text is available, set it in the input field and trigger translation
            if (data.recognized_text) {
                textInput.value = data.recognized_text; // Set recognized text to input
                translateText(); // Trigger translation
            } else if (data.error) {
                console.error('Speech-to-text error:', data.error); // Log any speech recognition error
            }
        } catch (error) {
            console.error('Speech-to-text fetch error:', error); // Log fetch errors
        } finally {
            micButton.classList.remove('active'); // Remove active class when done
        }
    });

    // Add an event listener to the output language selection to trigger translation on change
    outputLangSelect.addEventListener('change', () => {
        translateText(); // Trigger translation when the output language changes
    });

    // Function to play the translated text using Text-to-Speech
    const playTextToSpeech = () => {
        const translatedTextValue = translatedText.value; // Get the translated text
        const outputLang = outputLangSelect.value; // Get the output language

        // Check if there's text to speak
        if (!translatedTextValue) {
            console.error('No text to speak'); // Log an error if there's no text
            return; // Exit the function
        }

        // Check if TTS is available for the selected output language
        if (languagesWithoutTTS.includes(outputLang)) {
            alert('Text-to-speech is not available for this language.'); // Alert the user if TTS is unavailable
            return; // Exit the function
        }

        // Create a new SpeechSynthesisUtterance for TTS
        const utterance = new SpeechSynthesisUtterance(translatedTextValue);
        utterance.lang = outputLang; // Set the language for the utterance

        // Change the color of the speaker button to yellow while speaking
        speakerButton.style.backgroundColor = 'yellow';

        // Reset the button color back to its original state after speech ends
        utterance.onend = () => {
            speakerButton.style.backgroundColor = ''; // Reset button color
        };

        // Start speaking the text
        window.speechSynthesis.speak(utterance);
    };

    // Add event listener to speaker button to play text-to-speech when clicked
    speakerButton.addEventListener('click', playTextToSpeech);
});
