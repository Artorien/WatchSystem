
# Watch Humans

An automated social media scraping and output system for art.

This project is part of a larger system commissioned by artist **Marten Winters** and developed by **Group C (Eyewitnesses)**. It will be displayed at **Arcadia 2025**.

The project is divided into two development periods:

- **Period 3** (Current Status)
- **Period 4** (Upcoming Work)

This README reflects the state of the project at the end of **Period 3**.

---

## Current Status (Period 3)

### Implemented Features

#### Frontend UI
- Basic hardware controls (no hardware connection yet)
- Input field for hashtags to scrape

#### Backend Scraping
- Supports **Twitter (X)** and **Instagram**
- Scraped content is stored in a database

---

## Pending Features (For Period 4)

- Hardware integration (connection to UI controls)
- Text-to-Speech (TTS) functionality
- Additional platform support:
  - **Facebook** (coming soon)

---

## Dependencies

- [VSCode](https://code.visualstudio.com/) (recommended IDE)
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- Live Server VSCode plugin: `ritwickdey.LiveServer`

---

## How to Run the System

### 1. Start the Container

```bash
docker-compose up --build
```

### 2. Shut Down the Container

```bash
docker-compose down
```

### 3. Open the Frontend UI

- Open the `frontend` folder in **VSCode**
- Click **"Go Live"** (bottom-right corner)
- The app will open in your browser

---

## Development Timeline

| Period   | Focus                                         |
|----------|-----------------------------------------------|
| Period 3 | Basic UI, scraping (X/Instagram), DB storage  |
| Period 4 | Hardware control, TTS, Facebook scraping      |
