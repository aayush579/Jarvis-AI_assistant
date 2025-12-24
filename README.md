# Jarvis-AI (Full Build: Console + Plugins + Memory + GUI scaffold)

## Quickstart
1) Create a Python venv (recommended) and install deps:
```bash
pip install -r requirements.txt
```
2) Add your API keys in `config.json`.
3) Run (console):
```bash
python jarvis.py
```
4) (Optional GUI) Inside `gui/`:
```bash
npm install
npm start
```

## API Keys (edit `config.json`)
- `OPENAI_API_KEY` → for GPT responses
- `WEATHER_API_KEY` → from OpenWeatherMap
- `NEWS_API_KEY` → from NewsAPI
- `GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET` → for Google Calendar OAuth

## Packaging as .exe (Windows)
```bash
pip install pyinstaller
pyinstaller --onefile --noconsole jarvis.py
```
Output is in `dist/`.
