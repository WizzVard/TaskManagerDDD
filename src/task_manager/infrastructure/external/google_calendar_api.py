from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os.path
import pickle
from datetime import datetime

class GoogleCalendarAPI:
    """Низкоуровневый класс для работы с Google Calendar API"""
    
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    CREDENTIALS_FILE = 'credentials.json'
    TOKEN_FILE = 'token.pickle'

    def __init__(self):
        self.service = self._get_calendar_service()

    def _get_calendar_service(self):
        creds = None
        if os.path.exists(self.TOKEN_FILE):
            with open(self.TOKEN_FILE, 'rb') as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.CREDENTIALS_FILE, self.SCOPES
                )
                creds = flow.run_local_server(port=0)

            with open(self.TOKEN_FILE, 'wb') as token:
                pickle.dump(creds, token)

        return build('calendar', 'v3', credentials=creds)

    def create_calendar_event(self, event_data: dict) -> dict:
        """Создает событие в календаре"""
        return self.service.events().insert(calendarId='primary', body=event_data).execute()

    def update_calendar_event(self, event_id: str, event_data: dict) -> dict:
        """Обновляет событие в календаре"""
        return self.service.events().update(
            calendarId='primary',
            eventId=event_id,
            body=event_data
        ).execute()

    def delete_calendar_event(self, event_id: str) -> None:
        """Удаляет событие из календаря"""
        self.service.events().delete(
            calendarId='primary',
            eventId=event_id
        ).execute() 