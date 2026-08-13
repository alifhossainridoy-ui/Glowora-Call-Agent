# Jarvis Cosmetics AI Assistant

Bengali-language voice assistant (Kivy + Python, Android APK) for running a
cosmetics/beauty shop: order management, WhatsApp/call automation, product
recommendations, skin analysis, and daily reports.

## Project layout

```
app/          Kivy UI + entry point (main.py, jarvis.kv, buildozer.spec)
core/         Intent recognition, conversation context, emotion detection
voice/        STT (Vosk/Google/Whisper) and TTS (gTTS/Coqui/Piper) engines
cosmetics/    Product catalog, recommendations, skin/ingredient logic
automation/   WhatsApp, phone dialer, SMS, accessibility-service helpers (own device only)
business/     Orders, customers, inventory sync, reports, follow-ups
web/          Website API client / scraper for pulling orders
ai_models/    Optional offline (TinyLlama) and online (Gemini) LLM fallbacks
data/         business_config.json, products.json, SQLite DBs (generated), voice cache
assets/       icons, sounds, fonts (add your own binary assets here)
tests/        unittest suites
```

## Setup

```bash
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

Edit `data/business_config.json` with your shop's real name, phone, and
website. Edit `data/products.json` (or extend `cosmetics/product_database.py`)
with your actual catalog.

Optional online AI fallback:

```bash
set GEMINI_API_KEY=your-api-key
```

## Run on desktop (for development)

```bash
cd app
python main.py
```

## Run tests

```bash
python -m unittest discover tests
```

## Build the Android APK

```bash
pip install buildozer
cp app/buildozer.spec .
buildozer -v android debug
adb install bin/jarviscosmetics-2.0.0-arm64-v8a_debug.apk
```

Then on the phone: Settings > Accessibility > enable "Jarvis Cosmetics AI",
and log into WhatsApp normally — Jarvis drives the phone's own WhatsApp app
via Android Intents, no WhatsApp API/token needed.

## Security notes

All phone automation (`automation/`) uses argument-list `subprocess.run([...])`
calls rather than shell-interpolated strings, so phone numbers or message
text typed/spoken by a customer can't inject extra ADB/shell commands.
WhatsApp automation opens a chat with the message pre-filled — it does not
auto-tap Send, so you always get a final look before anything goes out.
