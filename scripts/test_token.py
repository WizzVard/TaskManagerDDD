from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# Загружаем токен из файла token.pickle
import pickle
import os

TOKEN_PATH = 'token.pickle'

def check_token():
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, 'rb') as token_file:
            creds = pickle.load(token_file)

        # Проверяем, нужно ли обновить токен
        if creds and creds.expired and creds.refresh_token:
            print("Token expired. Attempting to refresh...")
            creds.refresh(Request())
            # Сохраняем обновленный токен
            with open(TOKEN_PATH, 'wb') as token_file:
                pickle.dump(creds, token_file)
            print("Token refreshed and saved.")
        elif not creds or not creds.valid:
            print("Token is invalid. Please reauthenticate.")
        else:
            print("Token is valid.")
    else:
        print(f"No token file found at {TOKEN_PATH}.")
        print("Please reauthenticate.")

if __name__ == "__main__":
    check_token()