# telegram_php_translator_bot

This is a Telegram bot that translates human-readable content in `index.php` files into any language using the OpenAI API, while preserving all HTML, PHP, and JavaScript code.

---

## 🚀 Deploy in one click

<a href="https://heroku.com/deploy?template=https://github.com/Aullum/telegram-gpt-php-translator-bot">
  <img src="https://img.shields.io/badge/Heroku-430098?logo=heroku&logoColor=white&style=for-the-badge" alt="Heroku" style="height: 35px;"/>
</a>
&nbsp;&nbsp;&nbsp;&nbsp;
<a href="https://render.com/deploy?repo=https://github.com/Aullum/telegram-gpt-php-translator-bot">
  <img src="https://img.shields.io/badge/Render-000000?logo=render&logoColor=white&style=for-the-badge" alt="Render" style="height: 35px;"/>
</a>

---

## 📁 Project Structure

```
project/
├── bot.py                     # Entry point: initializes and runs the bot
├── handlers/
│   ├── commands.py            # /start and /restart command handlers
│   ├── documents.py           # Handler for index.php file uploads
│   └── language.py            # Handler for language input and translation
├── services/
│   ├── translator.py          # Translation logic with OpenAI API
│   └── chunker.py             # File splitting and reassembly logic
├── utils/
│   └── validators.py          # Validation utilities for translated content
├── webhook/
│   └── server.py              # aiohttp webhook handler
├── .env                       # Bot token, OpenAI key, and config vars
├── requirements.txt           # Python dependencies
├── Dockerfile                 # For Docker deployment
├── docker-compose.yml         # For local development with Docker
├── .dockerignore              # Files to exclude from Docker build context
├── app.json                   # For Heroku Deploy Button
└── README.md                  # Project description and usage instructions
```

---

## 🔧 Features

- Accepts `.php` files via Telegram
- Parses content into chunks and translates only user-visible text
- Preserves PHP, HTML, JavaScript and CSS structure
- Uses GPT-4 for translation
- Reassembles and returns a new file via Telegram

---

## 🧠 Technologies

- Python 3.12
- python-telegram-bot
- OpenAI API
- aiohttp
- asyncio
- Docker

---

## 🚀 Getting Started (Locally or in Docker)

### 1. Set environment variables in `.env`:

```
BOT_TOKEN=your_telegram_token
OPENAI_API_KEY=your_openai_key
# APP_URL=https://your-public-url.com   # Leave empty for polling mode
```

### 2. Install dependencies:

```
pip install -r requirements.txt
```

### 3. Run the bot locally:

```bash
python bot.py
```

- The bot will automatically switch between polling and webhook based on whether `APP_URL` is set in `.env`.

---

## 🐳 Running with Docker

You can run the bot in an isolated environment using Docker.

### 1. Build and run using docker-compose:

```bash
docker-compose up --build
```

Make sure you have a valid `.env` file in the root directory with:

```
BOT_TOKEN=your_telegram_token
OPENAI_API_KEY=your_openai_key
# APP_URL=https://your-public-url.com  # or leave empty to use polling
```

### 2. If testing webhook locally, you can use [ngrok](https://ngrok.com/):

```bash
ngrok http 5000
```

Update `.env`:

```
APP_URL=https://your-ngrok-url.ngrok.io
```

Now Telegram can deliver webhook updates to your local server.

---

## 📎 Example Usage

1. Send an `index.php` file to the bot
2. Type the language to translate to (e.g. `German`)
3. Bot responds with a translated file preserving structure

---

## 📬 Contact

For freelance inquiries or custom bots, feel free to reach out.

---
