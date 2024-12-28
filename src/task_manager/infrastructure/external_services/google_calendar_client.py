from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from datetime import timedelta


class GoogleCalendarClient:
    def __init__(self, credentials: Credentials):
        self.service = build('calendar', 'v3', credentials=credentials)

    def create_event(self, task):
        event = {
            'summary': task.title,
            'description': task.description,
            'start': {
                'dateTime': task.deadline.isoformat(),
                'timeZone': 'UTC',
            },
            'end': {
                'dateTime': (task.deadline + timedelta(hours=1)).isoformat(),
                'timezone': 'UTC',
            },
        }
        self.service.events().insert(calendarId='primary', body=event).execute()

    def update_event(self, task):
        event_id = task.google_calendar_event_id
        if not event_id:
            return
        
        event = {
            'summary': task.title,
            'description': task.description,
            'start': {
                'dateTime': task.deadline.isoformat(),
                'timeZone': 'UTC',
            },
            'end': {
                'dateTime': (task.deadline + timedelta(hours=1)).isoformat(),
                'timeZone': 'UTC',
            },
        }
        self.service.events().update(calendarId='primary', eventId=event_id, body=event).execute()

    def delete_event(self, task):
        event_id = task.google_calendar_event_id
        if not event_id:
            return
        
        self.service.events().delete(calendarId='primary', eventId=event_id).execute()