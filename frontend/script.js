function setVolume(value) {
  console.log(`Setting volume for Headphones to ${value}`);
}

function sendHashtags() {
  const hashtagInput = document.getElementById("hashtags").value;
  const hashtagsArray = hashtagInput
    .split(',')
    .map(tag => tag.trim())
    .filter(tag => tag !== "");

  const platformCheckboxes = document.querySelectorAll('input[name="platform"]:checked');
  const platforms = Array.from(platformCheckboxes).map(cb => cb.value);

  if (platforms.length === 0) {
    alert("Please select at least one platform!");
    return;
  }

  fetch('http://localhost:8000/scrape', {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      hashtags: hashtagsArray,
      platforms: platforms,
      type: "hashtags"
    })
  })
    .then(response => response.json())
    .then(data => {
      console.log("Hashtags response:", data);
      alert(`Hashtags sent to: ${platforms.join(", ")}\nHashtags: ${hashtagsArray.join(", ")}`);
    })
    .catch(error => {
      console.error("Error:", error);
      alert("Failed to send hashtags. Check console");
    });
}

function sendText() {
  const textInput = document.getElementById("textToPlay").value;

  if (!textInput.trim()) {
    alert("Please enter some text to play!");
    return;
  }

  fetch('http://localhost:8000/playtext', {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      text: textInput,
      type: "text"
    })
  })
    .then(response => response.json())
    .then(data => {
      console.log("Text response:", data);
      alert("Text submitted successfully!");
    })
    .catch(error => {
      console.error("Error:", error);
      alert("Failed to send text. Check console");
    });
}

const powerToggle = document.getElementById('powerToggle');
powerToggle.addEventListener('change', function () {
  if (this.checked) {
    console.log("System started");
    // Add start functionality here
  } else {
    console.log("System stopped");
    // Add stop functionality here
  }
});
