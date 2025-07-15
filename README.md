# telegram_php_translator_bot

This is a Telegram bot that translates human-readable content in `index.php` files into any language using the OpenAI API, while preserving all HTML, PHP, and JavaScript code.

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
├── Procfile                   # For Heroku deployment
└── README.md                  # Project description and usage instructions
```

## 🔧 Features

- Accepts `.php` files via Telegram
- Parses content into chunks and translates only user-visible text
- Preserves PHP, HTML, JavaScript and CSS structure
- Uses GPT-4 for translation
- Reassembles and returns a new file via Telegram

## 🧠 Technologies

- Python
- python-telegram-bot
- OpenAI API
- aiohttp
- asyncio

## 🚀 Getting Started

1. Set environment variables in `.env`:

```
BOT_TOKEN=your_telegram_token
APP_URL=https://your-app-name.herokuapp.com
OPENAI_API_KEY=your_openai_key
```

2. Install dependencies:

```
pip install -r requirements.txt
```

3. Run the bot:

```
python bot.py
```

4. Or deploy to Heroku using `Procfile`.

## 📎 Example Usage

1. Send an `index.php` file to the bot
2. Type the language to translate to (e.g. `German`)
3. Bot responds with a translated file preserving structure

## 📬 Contact

For freelance inquiries or custom bots, feel free to reach out.
