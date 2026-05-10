# AvtoBot — Telegram Vehicle Calculator Bot

Telegram bot that calculates:
- License plate price (via Selenium scraping)
- Vehicle tax (based on engine volume in Kazakhstan)

---

## Features

### Plate Number Checker
- Validates format (e.g. 123BDA)
- Uses Selenium to fetch price from external website
- Returns real-time pricing

### Tax Calculator
- Based on engine volume (0.1 – 10.0 L)
- Uses official MRP-based tax rules (Kazakhstan 2026)

---

## Tech Stack

- Python 3.9+
- python-telegram-bot
- Selenium
- Chrome WebDriver

---

## Setup Instructions

### 1. Clone repository
```bash
git clone https://github.com/dsbrzhn/Avtobot.git
cd Avtobot
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate   
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Run bot
```bash
python main.py
```
