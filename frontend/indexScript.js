const API_ROOT = 'http://127.0.0.1:5000';
const JS_ROOT = 'http://localhost:3000';

// Volume changing
document.getElementById('volume')?.addEventListener('input', function () {
  const value = parseInt(this.value, 10);
  fetch(`${JS_ROOT}/volume`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ value })
  })
    .then(res => {
      if (!res.ok) throw new Error('Failed to set volume');
      return res.json();
    })
    .then(() => {
      console.log('Volume set to', value);
    })
    .catch(err => {
      console.error('Error setting volume:', err);
    });
});

function sendRequestToScrape() {
  let platforms = [];

  const twitter     = document.getElementById("twitter");
  const facebook    = document.getElementById("facebook");
  const instagram   = document.getElementById("instagram");
  const powerToggle = document.getElementById("powerToggle");
  let wasStarted    = false;

  function onCheckboxChange(ev) {
    const val = ev.target.value;
    if (ev.target.checked) {
      if (!platforms.includes(val)) platforms.push(val);
    } else {
      platforms = platforms.filter(item => item !== val);
    }
    console.log("Platforms now:", platforms);
  }

  twitter.addEventListener("change",   onCheckboxChange);
  facebook.addEventListener("change",  onCheckboxChange);
  instagram.addEventListener("change", onCheckboxChange);

  function onPowerToggleChange() {
    if (powerToggle.checked) {
      wasStarted = true;
      fetch(`${API_ROOT}/scrape`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ platforms })
      })
        .then(response => {
          if (!response.ok) throw new Error('Failed to start scraping');
          console.log("Scraping started successfully");
        })
        .catch(err => {
          console.error(err);
          alert("Error starting scraping");
        });
    } else {
      if (!wasStarted) {
        console.warn("Toggle turned OFF before ever starting.");
        return;
      }
      fetch(`${API_ROOT}/stop-automation`, { method: "POST" })
        .then(response => {
          if (!response.ok) throw new Error('Failed to stop scraping');
          alert("Scraping stopped successfully");
        })
        .catch(err => {
          console.error(err);
          alert("Error stopping scraping");
        });
    }
  }

  powerToggle.addEventListener("change", onPowerToggleChange);
}

function sendText() {
  const textarea = document.getElementById('textToPlay');
  const text = textarea.value.trim();
  if (!text) {
    alert('Please enter some text.');
    return;
  }
  fetch(`${JS_ROOT}/intro_captions`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text })
  })
  .then(() => {
    textarea.value = "";
  })
    .catch(error => {
      console.error('Error adding intro caption:', error);
      alert('Failed to submit intro caption');
    });
}

function sendHashtags() {
  const input = document.getElementById("hashtags").value;
  const hashtags = input
    .split(',')
    .map(tag => tag.trim())
    .filter(tag => tag.length > 0);

  const invalid = hashtags.find(tag => tag.includes(' '));
  if (invalid) {
    alert(`Invalid hashtag "${invalid}". Hashtags cannot contain spaces.`);
    return;
  }
  fetch(`${JS_ROOT}/hashtags`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ hashtags })
  })
  .then(() => {
    document.getElementById("hashtags").value = "";
  })
    .catch(error => {
      console.error('Error sending hashtags:', error);
    });
}

function setupFilteringToggle() {
  const filteringToggle = document.getElementById("filteringToggle");
  filteringToggle.addEventListener("change", () => {
    const url = filteringToggle.checked
      ? `${API_ROOT}/filtering_on`
      : `${API_ROOT}/filtering_off`;

    fetch(url, { method: "POST" })
      .then(res => {
        if (!res.ok) throw new Error('Failed to change filtering');
        return res.json();
      })
      .then(data => {
        console.log("Filtering state is now", data.filtering);
      })
      .catch(err => {
        console.error(err);
        alert("Error changing filtering state");
      });
  });
}

document.addEventListener("DOMContentLoaded", () => {
  sendRequestToScrape();
  setupFilteringToggle();

  document.getElementById('textToPlay')?.nextElementSibling?.addEventListener('click', sendText);
  document.getElementById('hashtags')?.nextElementSibling?.addEventListener('click', sendHashtags);
});
