from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from twilio.rest import Client
import datetime

# Set up Google API credentials
creds = Credentials.from_authorized_user_info(info) # info contains your credentials

# Set up Twilio credentials
account_sid = 'your_account_sid'
auth_token = 'your_auth_token'
whatsapp_client = Client(account_sid, auth_token)

# Set up Google Calendar API service
service = build('calendar', 'v3', credentials=creds)

# Get today's date and time
now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time zone

# Call the Calendar API
events_result = service.events().list(calendarId='primary', timeMin=now,
                                      maxResults=10, singleEvents=True,
                                      orderBy='startTime').execute()
events = events_result.get('items', [])

# Create message body with event details
if not events:
    message_body = "No upcoming events found"
else:
    message_body = "Upcoming events:\n"
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        start_time = datetime.datetime.fromisoformat(start).strftime('%I:%M %p')
        message_body += f"{event['summary']} at {start_time}\n"

# Send message on WhatsApp using Twilio API
whatsapp_message = whatsapp_client.messages.create(
    body=message_body,
    from_='whatsapp:+14155238886',  # Twilio Sandbox number
    to='whatsapp:<your_phone_number>'
)

print(whatsapp_message.sid)
