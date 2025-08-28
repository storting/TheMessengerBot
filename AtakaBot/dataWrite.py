from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import codecs

# Если изменить доступ к данным, обновить этот список разрешений
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def main():
    creds = None
    
    # Файл токенов хранится локально и используется повторно
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
    # Если токены устарели или отсутствуют
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
            
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('sheets', 'v4', credentials=creds)

    # ID таблицы (из URL Гугл-документа)
    SAMPLE_SPREADSHEET_ID = '116w9l5Uwar_ve0J5J92UG4ByaQZsjvJr8fLq8wGsJMo'
    
    # Диапазон чтения (например, лист A1:C10)
    SAMPLE_RANGE_NAME = 'Лист1!A2:N3177'

    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    file = codecs.open("dataBase", "w", "utf-8")

    if not values:
        print('No data found.')
    else:
        for row in values:
            if len(row) > 13 and row[13]:  
                filtered_row = row[:9] + row[11:]
                print(filtered_row)
                file.write(str(filtered_row)+"\n")
                    

if __name__ == '__main__':
    main()