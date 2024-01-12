/*async function sendRequest() {
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

            // Apply PEP8 indentation to the GPT-3 response code
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
        } else if ("error" in data) {
            document.getElementById("answer").innerHTML = `Error: ${data.error}`;
        } else {
            document.getElementById("answer").innerHTML = "Unknown error.";
        }
    } else {
        document.getElementById("answer").innerHTML = "Server error.";
    }
}

function applyPEP8Indentation(code) {
    code = code.replace(/```python\n/g, '').replace(/```/g, '');
    // Split the code into lines
    const lines = code.split('\n');

    // Apply indentation rules
    return lines.map(line => {
        // Count the leading spaces (assuming 4 spaces per indentation level for PEP 8)
        const indentLevel = line.search(/\S|$/) / 4;

        // Replace every 4 spaces with a specific amount of padding
        let indent = '';
        for (let i = 0; i < indentLevel; i++) {
            indent += '<span class="indent">&nbsp;</span>';
        }

        // Remove the leading spaces and replace them with the indentation span
        return indent + line.trimStart();
    }).join('\n');
}

// Helper function to escape HTML characters
function escapeHTML(html) {
    return html
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}*/

/*document.getElementById('thumbs-up').addEventListener('click', () => sendRating('up'));
document.getElementById('thumbs-down').addEventListener('click', () => sendRating('down'));*/


/*async function sendRequest() {
  const question = document.getElementsByName("user_input")[0].value;
  const response = await fetch('/ask_gpt4/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ user_input: question })
  });
  const data = await response.json();

  if (response.status === 200) {
    if ("response" in data) {
      const answerBox = document.createElement("code");
      answerBox.classList.add("d-block", "p-3", "bg-success", "text-white");
      answerBox.innerHTML = data.response.replace(/\n/g, "<br>");
      const answerElement = document.getElementById("answer");
      while (answerElement.firstChild) {
        answerElement.removeChild(answerElement.firstChild);
      }
      answerElement.appendChild(answerBox);
    } else if ("error" in data) {
      document.getElementById("answer").innerHTML = `Error: ${data.error}`;
    } else {
      document.getElementById("answer").innerHTML = "Unknown error.";
    }
  } else {
    document.getElementById("answer").innerHTML = "Server error.";
  }
}*/


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

    code = code.replace(/```python\n/g, '').replace(/```/g, '');
    // Split the code into lines
    const lines = code.split('\n');

    // Apply indentation rules
    return lines.map(line => {
        // Count the leading spaces (assuming 4 spaces per indentation level for PEP 8)
        const indentLevel = line.search(/\S|$/) / 4;

        // Replace every 4 spaces with a specific amount of padding
        let indent = '';
        for (let i = 0; i < indentLevel; i++) {
            indent += '<span class="indent">&nbsp;</span>';
        }

        // Remove the leading spaces and replace them with the indentation span
        return indent + line.trimStart();
    }).join('\n');
}

document.getElementById('thumbs-up').addEventListener('click', () => sendRating('up'));
document.getElementById('thumbs-down').addEventListener('click', () => sendRating('down'));


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
});
