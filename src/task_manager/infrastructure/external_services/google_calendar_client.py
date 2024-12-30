from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os.path
import pickle


class GoogleCalendarClient:
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    CREDENTIALS_FILE = 'credentials.json'
    TOKEN_FILE = 'token.pickle'

    def __init__(self):
        self.service = self._get_calendar_service()

    def _get_calendar_service(self):
        creds = None
        # Load saved credentials
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

            # Save the credentials for the next run
            with open(self.TOKEN_FILE, 'wb') as token:
                pickle.dump(creds, token)

        return build('calendar', 'v3', credentials=creds)
    
    async def create_event(self, task):
        """Create an event in the Google Calendar on the basis of the task"""
        event = {
            'summary': task.title,
            'description': task.description,
            'start': {
                'dateTime': task.deadline.isoformat() if task.deadline else 
                (datetime.now() + timedelta(days=1)).isoformat(),
                'timeZone': 'UTC',
            },
            'end': {
                'dateTime': task.deadline.isoformat() if task.deadline else 
                (datetime.now() + timedelta(days=1)).isoformat(),
                'timeZone': 'UTC',
            },
            'reminders': {
                'useDefault': True
            }
            
        }

        try: 
            event = self.service.events().insert(calendarId='primary', body=event).execute()
            print(f'Event created: {event.get("htmlLink")}')
            return event['id']
        except Exception as e:
            print(f'Error creating event: {e}')
            return None
        
    async def update_event(self, task):
        """Update an event in the Google Calendar"""
        if not task.calendar_event_id:
            return await self.create_event(task)
        
        event = {
            'summary': task.title,
            'description': task.description,
            'start': {
                'dateTime': task.deadline.isoformat(), 
                'timeZone': 'UTC'
            },
            'end': {
                'dateTime': (task.deadline + timedelta(hours=1)).isoformat(),
                'timeZone': 'UTC'
            }
        }

        try:
            self.service.events().update(
                calendarId='primary',
                eventId=task.calendar_event_id,
                body=event
            ).execute()
        except Exception as e:
            print(f'Error updating event: {e}')

    
    async def delete_event(self, task):
        """Delete an event from the Google Calendar"""
        if task.calendar_event_id:
            try:
                self.service.events().delete(
                    calendarId='primary',
                    eventId=task.calendar_event_id
                ).execute()
            except Exception as e:
                print(f'Error deleting event: {e}')

    def _get_event_id(self, task_id):
        # TODO: Implement the logic to get the event id from the task id
        return None
