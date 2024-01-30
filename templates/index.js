

async function sendRequest() {
    const question = document.getElementsByName("user_input")[0].value;
    const response = await fetch('/ask_gpt4/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            user_input: question
        })
    });
    const data = await response.json();

    if (response.status === 200) {
        if ("response" in data) {

            const answerElement = document.getElementById("answer");
            answerElement.innerHTML = ''; // Clear previous content

            // Apply PEP8 indentation to the GPT-4 response code
            const formattedCode = applyPEP8Indentation(data.response);

            // Create the code block with formatted code
            const preElement = document.createElement('pre');
            const codeElement = document.createElement('code');
            codeElement.classList.add('language-python');
            codeElement.innerHTML = formattedCode; // Use innerHTML to include indentation spans

            preElement.appendChild(codeElement);
            answerElement.appendChild(preElement);

            // Check if Highlight.js is available and highlight the code
            if (window.hljs) {
                hljs.highlightElement(codeElement);
            } else {
                console.error('Highlight.js is not loaded.');
            }

            // Show the rating buttons and set the current response ID
            document.getElementById("rating").style.display = 'block';
            document.getElementById("currentResponseId").value = new Date().toISOString();
        } else if ("error" in data) {
            document.getElementById("answer").innerHTML = `Error: ${data.error}`;
            document.getElementById("rating").style.display = 'none';
        } else {
            document.getElementById("answer").innerHTML = "Unknown error.";
            document.getElementById("rating").style.display = 'none';
        }
    } else {
        document.getElementById("answer").innerHTML = "Server error.";
        document.getElementById("rating").style.display = 'none';
    }
}



function applyPEP8Indentation(code) {
    // Split the code into lines
    const lines = code.split('\n');

    // Apply indentation rules
    return lines.map(line => {
        const indentLevel = line.search(/\S|$/) / 4;
        const indent = ' '.repeat(indentLevel * 4); // Create a string with a number of spaces
        return indent + line.trimStart();
    }).join('\n');
}



document.getElementById('thumbs-up').addEventListener('click', () => sendRating('up'));
document.getElementById('thumbs-down').addEventListener('click', () => sendRating('down'));


/**
 * Function to send the rating to the server after user presses the thumbs up or thumbs down button.
 * @param {string} rating
 */
function sendRating(rating) {
    const responseId = getCurrentResponseId();
    const feedbackElement = document.getElementById("feedback");

    fetch('/send_feedback/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({responseId: responseId, feedback: rating})
    })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Network response was not ok.');
            }
        })
        .then(data => {
            feedbackElement.innerHTML = `Feedback sent successfully: ${rating}`;
            feedbackElement.style.display = 'block';
        })
        .catch(error => {
            feedbackElement.innerHTML = `Error sending feedback: ${error}`;
            feedbackElement.style.display = 'block';
        });
}

function getCurrentResponseId() {
    return document.getElementById("currentResponseId").value;
}

/***************************Speech Recognition Starts here*******************/

function sendSpeechToServer(transcript) {
    fetch('/ask_gpt4', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({user_input: transcript, model: 'gpt-4'})
    })
    .then(response => response.json())
    .then(data => {
        if ("response" in data) {
            // Use processResponse to format and display the response
            processResponse(data.response);
        } else {
            // Handle any errors
            displayError(data.error || "An unknown error occurred.");
        }
    })
    .catch((error) => {
        displayError(`Error: ${error}`);
    });
}





function processResponse(response) {
    const answerElement = document.getElementById("answer");
    answerElement.innerHTML = ''; // Clear any previous content

    // Assume response is plain text. Modify as needed if response is HTML.
    const formattedResponse = applyPEP8Indentation(response);

    const preElement = document.createElement('pre');
    const codeElement = document.createElement('code');
    codeElement.classList.add('language-python');
    codeElement.textContent = formattedResponse; // Use textContent for plain text

    preElement.appendChild(codeElement);
    answerElement.appendChild(preElement);

    // Apply syntax highlighting
    if (window.hljs) {
        hljs.highlightElement(codeElement);
    }
}

function sendFeedback(rating) {
    // Example feedback data
    const feedbackData = {
        responseId: getCurrentResponseId(),  // Assuming you have a way to get the current response ID
        feedback: rating
    };

    fetch('/rate_response/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(feedbackData)
    })
    .then(response => response.json())
    .then(data => {
        console.log("Feedback sent successfully:", data);
    })
    .catch(error => {
        console.error("Error sending feedback:", error);
    });
}


/**
 * Function to decode HTML-encoded strings.
 * @param {string} input
 */
function htmlDecode(input) {
    var e = document.createElement('textarea');
    e.innerHTML = input;
    // handle case of empty input
    return e.childNodes.length === 0 ? "" : e.childNodes[0].nodeValue;
}


function displayError(message) {
    const answerElement = document.getElementById("answer");
    answerElement.textContent = message; // Use textContent for security
    // If you have an error-specific styling, apply it here
}


//global variable for speech recognition
let isRecording = false;

// Function to toggle speech recognition on and off
function toggleSpeechRecognition() {
    // Assuming you have a variable to track the state of recording
    if (isRecording) {
        stopSpeechRecognition();
        isRecording = false;
    } else {
        startSpeechRecognition();
        isRecording = true;
    }
}

// Function to display messages to the user
function displaySpeechMessage(message) {
    const speechMessagesDiv = document.getElementById('speech-messages');
    speechMessagesDiv.style.display = 'block';
    speechMessagesDiv.textContent = message;
}

// Global variable for speech recognition
let recognition;

if ('webkitSpeechRecognition' in window) {
    recognition = new webkitSpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'en-US';

    recognition.onstart = function () {
        displaySpeechMessage('Speech recognition service has started.');
    };

    recognition.onresult = function (event) {
        var transcript = event.results[0][0].transcript;
        displaySpeechMessage('Transcript: ' + transcript);
        sendSpeechToServer(transcript);
    };

    recognition.onerror = function (event) {
        displaySpeechMessage('Speech recognition error: ' + event.error);
    };

    recognition.onend = function () {
        displaySpeechMessage('Speech recognition service disconnected.');
    };
} else {
    alert('Your browser does not support speech recognition. Please try Chrome.');
}

// Function to start speech recognition
function startSpeechRecognition() {
    if (recognition) {
        recognition.start();
    }
}

// Function to stop speech recognition
function stopSpeechRecognition() {
    if (recognition) {
        recognition.stop();
    }
}


function startDictation() {
    if (window.hasOwnProperty('webkitSpeechRecognition')) {
        var recognition = new webkitSpeechRecognition();
        recognition.continuous = false; // The recognition will stop after capturing a single utterance
        recognition.interimResults = false; // We only want final results, not interim
        recognition.lang = "en-US"; // Set the language of the recognition
        recognition.start(); // Start the speech recognition

        recognition.onresult = function (e) {
            // This function is triggered when the speech is recognized
            document.getElementById('transcript').value = e.results[0][0].transcript;
            recognition.stop(); // Stop the recognition after capturing the speech
            document.getElementById('submit').click(); // Automatically click the submit button to send data to backend
        };

        recognition.onerror = function (e) {
            recognition.stop(); // Ensure to stop the recognition in case of an error
        }
    }
}


/**          Speech Recognition Ends here          **/


// DOMContentLoaded event listener
document.addEventListener('DOMContentLoaded', function () {
    // Attach event listener to the submit button
    const submitButton = document.getElementById('submit-button');
    if (submitButton) {
        submitButton.addEventListener('click', sendRequest);
    }

    // Attach event listeners for rating buttons
    const thumbsUpButton = document.getElementById('thumbs-up');
    const thumbsDownButton = document.getElementById('thumbs-down');
    if (thumbsUpButton && thumbsDownButton) {
        thumbsUpButton.addEventListener('click', () => sendRating('up'));
        thumbsDownButton.addEventListener('click', () => sendRating('down'));
    }
    // Attach event listener to the login button
    const loginButton = document.getElementById('login-github-btn');
    if (loginButton) {
        loginButton.addEventListener('click', function () {
            window.location.href = '/login/github';
        });
    }

    //authenticated message
    if (window.location.pathname === '/authenticated') {

        document.getElementById('logout-github-btn').style.display = 'block';
    }
    // Attach event listener to the logout button
    const logoutButton = document.getElementById('logout-github-btn');
    if (logoutButton) {
        logoutButton.addEventListener('click', function () {
            window.location.href = '/logout';
        });
    }


    // Attach event listener to the signup button
    document.getElementById('start-record-btn').addEventListener('click', startDictation);
    let startRecordBtn = document.getElementById('start-record-btn');
    if (startRecordBtn) {
        startRecordBtn.addEventListener('click', startSpeechRecognition);
    }


});