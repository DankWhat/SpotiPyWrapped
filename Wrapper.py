import http.client
import base64
import json
import webbrowser

class SpotifyClient:
    """
    A simple Python wrapper for the Spotify API.

    Attributes:
        client_id (str): The client ID obtained from the Spotify Developer Dashboard.
        client_secret (str): The client secret obtained from the Spotify Developer Dashboard.
        access_token (str): The access token obtained for authentication with the Spotify API.
    """

    def __init__(self, client_id, client_secret):
        """
        Initializes the SpotifyClient with client credentials.

        Args:
            client_id (str): The client ID obtained from the Spotify Developer Dashboard.
            client_secret (str): The client secret obtained from the Spotify Developer Dashboard.
        """
        self.client_id = "a5679a94e0f849f68d3ecfd3bfc47249"
        self.client_secret = "3f2e462beca54cbb979407227295e354"
        self.access_token = None


    def _get_access_token(self):
        """
        Retrieves the access token required for authentication with the Spotify API.
        """
        client_credentials = f"{self.client_id}:{self.client_secret}"
        encoded_credentials = base64.b64encode(client_credentials.encode()).decode()
        headers = {
            'Authorization': f'Basic {encoded_credentials}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        conn = http.client.HTTPSConnection("accounts.spotify.com")
        payload = "grant_type=client_credentials"
        conn.request("POST", "/api/token", payload, headers)
        res = conn.getresponse()
        data = res.read()
        response = json.loads(data)
        self.access_token = response['access_token']

    def _make_request(self, method, endpoint, params=None):
        """
        Makes a request to the Spotify API.

        Args:
            method (str): The HTTP method for the request (e.g., "GET", "POST").
            endpoint (str): The endpoint of the API to request.
            params (dict): Additional parameters for the request (optional).

        Returns:
            dict: The JSON response from the API.
        """
        if not self.access_token:
            self._get_access_token()
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }
        conn = http.client.HTTPSConnection("api.spotify.com")
        conn.request(method, endpoint, headers=headers)
        res = conn.getresponse()
        data = res.read()
        return json.loads(data.decode())

    def get_track(self, track_id):
        """
        Retrieves information about a track from the Spotify API.

        Args:
            track_id (str): The ID of the track to retrieve information for.

        Returns:
            dict: Information about the track.
        """
        endpoint = f"/v1/tracks/{track_id}"
        return self._make_request("GET", endpoint)


# Example usage
client = SpotifyClient(client_id='a5679a94e0f849f68d3ecfd3bfc47249', client_secret='3f2e462beca54cbb979407227295e354')
track_info = client.get_track('7GX5flRQZVHRAGd6B4TmDO')

# Extract relevant information
track_name = track_info['name']
artist_name = track_info['artists'][0]['name']
album_name = track_info['album']['name']
preview_url = track_info['preview_url']

# Print basic track information
print(f"Track Name: {track_name}")
print(f"Artist: {artist_name}")
print(f"Album: {album_name}")

# Open preview URL in the default web browser
if preview_url:
    print("Preview URL:", preview_url)
    webbrowser.open(preview_url)
else:
    print("No preview available for this track.")