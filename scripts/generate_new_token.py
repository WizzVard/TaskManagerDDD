from google_auth_oauthlib.flow import InstalledAppFlow
import pickle

SCOPES = ['https://www.googleapis.com/auth/calendar']

def generate_new_token():
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)

    with open('token.pickle', 'wb') as token_file:
        pickle.dump(creds, token_file)
    print("New token saved to token.pickle")

if __name__ == "__main__":
    generate_new_token()