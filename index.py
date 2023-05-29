from django.shortcuts import redirect
from django.http import JsonResponse
from django.views import View
from google.auth.transport import requests
from google.oauth2 import id_token
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery


# Google Calendar Integration Views

class GoogleCalendarInitView(View):
    def get(self, request):
        # Step 1: Start OAuth process and prompt user for credentials
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            'path/to/client_secrets.json',
            scopes=['https://www.googleapis.com/auth/calendar.events.readonly']
        )
        flow.redirect_uri = 'http://your-domain.com/rest/v1/calendar/redirect/'

        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true'
        )

        return redirect(authorization_url)


class GoogleCalendarRedirectView(View):
    def get(self, request):
        # Step 2: Handle redirect request from Google with code for token
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            'path/to/client_secrets.json',
            scopes=['https://www.googleapis.com/auth/calendar.events.readonly']
        )
        flow.redirect_uri = 'http://your-domain.com/rest/v1/calendar/redirect/'

        authorization_response = request.build_absolute_uri()
        flow.fetch_token(authorization_response=authorization_response)

        # Get access token from code
        credentials = flow.credentials
        access_token = credentials.token
        refresh_token = credentials.refresh_token

        # Use access token to get list of events in user's calendar
        service = googleapiclient.discovery.build('calendar', 'v3', credentials=credentials)
        events = service.events().list(calendarId='primary').execute()

        # Return the list of events as JSON response
        return JsonResponse(events)


# Note: Please make sure to replace 'http://your-domain.com' with your actual domain.

