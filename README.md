# Telegram GPT PHP Translator Bot

[![Python](https://img.shields.io/badge/Python-3.12-blue)](https://www.python.org/)
[![aiogram](https://img.shields.io/badge/aiogram-3.x-00A8E8)](https://docs.aiogram.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Poetry](https://img.shields.io/badge/Poetry-managed-informational)](https://python-poetry.org/)

A Telegram bot that translates **index.php** landing pages with **OpenAI** while preserving HTML/PHP structure.
Built with **Python**, **Aiogram**, **BeautifulSoup**, and **Poetry**.

---

## ✨ Features

- Upload an `index.php` file directly to the bot
- Choose target language for translation
- High‑quality localization with OpenAI (gpt‑4.1)
- Preserves HTML/PHP and overall structure
- Single‑message **progress bar** in Telegram
- Auto‑loop: prompts for the next file after completion
- **One‑click deploy** to **Render** or **Heroku**

---

## 🧰 Requirements

- Python **3.12**
- Poetry **1.6+**
- Telegram Bot Token
- OpenAI API key

---

## 🚀 Quickstart (Local, with Poetry)

```bash
git clone https://github.com/<your-username>/telegram-gpt-php-translator-bot.git
cd telegram-gpt_php_translator_bot
poetry install --no-interaction --no-ansi
# Create .env in repo root
cat > .env << 'EOF'
BOT_TOKEN=your_telegram_bot_token
OPENAI_API_KEY=your_openai_api_key
# Optional if you later switch to webhooks
WEBHOOK_URL=
WEBHOOK_SECRET=
EOF

poetry run python -m telegram_gpt_php_translator_bot.main
```

> The package uses the **src/** layout; code lives in `src/telegram_gpt_php_translator_bot` and is installed via Poetry.

---

## ☁ One‑Click Deployment

### Render

Add the **Deploy to Render** button to your repo (already included below). Render will read `render.yaml` and guide you to set secrets.

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

### Heroku

Click the **Deploy to Heroku** button. Heroku reads `app.json`, provisions a **worker** dyno, and prompts for required config vars.

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

> Notes for Heroku:
>
> - Poetry is supported natively by the Python buildpack when the repo contains `pyproject.toml` **and** `poetry.lock` (no `requirements.txt`).
> - The Python version is pinned via `.python-version` (3.12).
> - Process type is a **worker** (`Procfile`).

---

## 🔧 Configuration

Environment variables (via `.env` in development or platform config in production):

- `BOT_TOKEN` — Telegram bot token from **@BotFather**
- `OPENAI_API_KEY` — OpenAI API key
- `WEBHOOK_URL` _(optional)_ — public HTTPS endpoint if you switch to webhooks
- `WEBHOOK_SECRET` _(optional)_ — secret for webhook verification

---

## 🗂 Project Structure

```
src/
  telegram_gpt_php_translator_bot/
    __init__.py
    main.py                   # entry point
    config.py                 # pydantic-settings (.env)
    states.py                 # FSM
    handlers/
      start_handler.py
      translate_handler.py
      lang_input_handler.py
    services/
      parser_service.py       # bs4/lxml extraction + reapply translations
      openai_service.py       # chunking + Chat Completions
      progress_service.py     # single-message progress UI
```

---

## 🧪 Development

```bash
poetry run ruff check .
poetry run black .
```

You can enable `pre-commit` to run quality checks automatically.

---

## 🛠 Troubleshooting

- **Message is not modified**: progress UI edits are debounced; errors are handled and surfaced in the progress message.
- **No response from OpenAI**: check `OPENAI_API_KEY`, quota, and model availability.
- **Heroku build fails**: ensure `poetry.lock` is committed and `.python-version` matches a supported version.
