import requests
from config import JOKES_API_URL, JOKES_API_KEY

class JokesService:
    """Service for interacting with the jokes API."""

    def __init__(self):
        self.api_url = JOKES_API_URL
        self.api_key = JOKES_API_KEY
        self.headers = {}

        # Set up headers if API key is provided
        if self.api_key:
            self.headers['Authorization'] = f'Bearer {self.api_key}'

    def get_random_joke(self):
        """
        Fetch a random joke from the API.

        Returns:
            dict: A joke object or None if the request failed
        """
        try:
            response = requests.get(f"{self.api_url}/random", headers=self.headers)
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching joke: {e}")
            return {"error": "En estos momentos hay un elefante pisoteando nuestros servidores, inténtalo más tarde y si persiste contacta con el administrador para espantarlos."}

    def get_random_joke_by_type(self, type_slug):
        """
        Fetch a random joke of a specific type.

        Args:
            type_slug (str): The type of joke to fetch

        Returns:
            dict: A joke object or None if the request failed
        """
        try:
            response = requests.get(f"{self.api_url}/type/{type_slug}/content/random", headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching joke of type {type_slug}: {e}")
            return {"error": "En estos momentos hay un elefante pisoteando nuestros servidores, inténtalo más tarde y si persiste contacta con el administrador para espantarlos."}

    def get_random_joke_by_group(self, group_slug):
        """
        Fetch a random joke from a specific group.

        Args:
            group_slug (str): The group of jokes to fetch from

        Returns:
            dict: A joke object or None if the request failed
        """
        try:
            response = requests.get(f"{self.api_url}/group/{group_slug}/content/random", headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching joke from group {group_slug}: {e}")
            return {"error": "En estos momentos hay un elefante pisoteando nuestros servidores, inténtalo más tarde y si persiste contacta con el administrador para espantarlos."}

    def get_joke_by_id(self, joke_id):
        """
        Fetch a specific joke by ID.

        Args:
            joke_id (str): The ID of the joke to fetch

        Returns:
            dict: A joke object or None if the request failed
        """
        try:
            response = requests.get(f"{self.api_url}/{joke_id}", headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching joke {joke_id}: {e}")
            return None

    def search_jokes(self, query, limit=5):
        """
        Search for jokes containing the query string.

        Args:
            query (str): The search query
            limit (int): Maximum number of jokes to return

        Returns:
            list: A list of joke objects or empty list if the request failed
        """
        try:
            params = {'q': query, 'limit': limit}
            response = requests.get(f"{self.api_url}/search", params=params, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error searching jokes: {e}")
            return []