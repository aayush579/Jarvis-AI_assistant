from __future__ import print_function
import datetime
from pathlib import Path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar']

def _get_creds(cfg: dict) -> Credentials:
    token_path = Path("data/token.json")
    creds = None
    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            client_id = cfg.get("GOOGLE_CLIENT_ID")
            client_secret = cfg.get("GOOGLE_CLIENT_SECRET")
            if not client_id or not client_secret:
                raise RuntimeError("Set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET in config.json")
            flow = InstalledAppFlow.from_client_config({
                "installed": {
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": ["http://localhost"]
                }
            }, SCOPES)
            creds = flow.run_local_server(port=0)
        token_path.write_text(creds.to_json(), encoding="utf-8")
    return creds

def run(arg: str, cfg: dict) -> str:
    creds = _get_creds(cfg)
    service = build('calendar', 'v3', credentials=creds)

    if arg.lower().startswith("list"):
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=5, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])
        if not events:
            return "No upcoming events found."
        lines = []
        for e in events:
            start = e['start'].get('dateTime', e['start'].get('date', ''))
            lines.append(f"- {start} → {e.get('summary','(no title)')}")
        return "\n".join(lines)

    if arg.lower().startswith("add "):
        text = arg[4:].strip()
        parts = text.rsplit(" at ", 1)
        if len(parts) != 2:
            return "Usage: run gcal add <Title> at <YYYY-MM-DD HH:MM>"
        title, when = parts
        start = datetime.datetime.fromisoformat(when)
        end = start + datetime.timedelta(hours=1)
        event = {
            'summary': title,
            'start': {'dateTime': start.isoformat()},
            'end': {'dateTime': end.isoformat()},
        }
        event = service.events().insert(calendarId='primary', body=event).execute()
        return f"Created: {event.get('htmlLink','(no link)')}"
    return "Usage: run gcal list  |  run gcal add <Title> at <YYYY-MM-DD HH:MM>"
