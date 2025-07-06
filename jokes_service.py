import requests
from config import JOKES_API_URL, JOKES_API_KEY

class JokesService:
    """Servicio que he creado para interactuar con la API de chistes."""

    def __init__(self):
        self.api_url = JOKES_API_URL
        self.api_key = JOKES_API_KEY
        self.headers = {}

        # Configuro las cabeceras si se proporciona una clave API
        if self.api_key:
            self.headers['Authorization'] = f'Bearer {self.api_key}'

    def get_random_joke(self):
        """
        Obtengo un chiste aleatorio desde la API.

        Returns:
            dict: Un objeto de chiste o None si la petición falló
        """
        try:
            response = requests.get(f"{self.api_url}/random", headers=self.headers)
            response.raise_for_status()  # Lanzo una excepción para errores HTTP
            return response.json()
        except requests.RequestException as e:
            print(f"Error al obtener el chiste: {e}")
            return {"error": "En estos momentos hay un elefante pisoteando nuestros servidores, inténtalo más tarde y si persiste contacta con el administrador para espantarlos."}

    def get_random_joke_by_type(self, type_slug):
        """
        Obtengo un chiste aleatorio de un tipo específico.

        Args:
            type_slug (str): El tipo de chiste a obtener

        Returns:
            dict: Un objeto de chiste o None si la petición falló
        """
        try:
            response = requests.get(f"{self.api_url}/type/{type_slug}/content/random", headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error al obtener chiste de tipo {type_slug}: {e}")
            return {"error": "En estos momentos hay un elefante pisoteando nuestros servidores, inténtalo más tarde y si persiste contacta con el administrador para espantarlos."}

    def get_random_joke_by_group(self, group_slug):
        """
        Obtengo un chiste aleatorio de un grupo específico.

        Args:
            group_slug (str): El grupo de chistes del que obtener

        Returns:
            dict: Un objeto de chiste o None si la petición falló
        """
        try:
            response = requests.get(f"{self.api_url}/group/{group_slug}/content/random", headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error al obtener chiste del grupo {group_slug}: {e}")
            return {"error": "En estos momentos hay un elefante pisoteando nuestros servidores, inténtalo más tarde y si persiste contacta con el administrador para espantarlos."}

    def get_joke_by_id(self, joke_id):
        """
        Obtengo un chiste específico por su ID.

        Args:
            joke_id (str): El ID del chiste a obtener

        Returns:
            dict: Un objeto de chiste o None si la petición falló
        """
        try:
            response = requests.get(f"{self.api_url}/{joke_id}", headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error al obtener el chiste {joke_id}: {e}")
            return None

    def search_jokes(self, query, limit=5):
        """
        Busco chistes que contengan la cadena de consulta.

        Args:
            query (str): La consulta de búsqueda
            limit (int): Número máximo de chistes a devolver

        Returns:
            list: Una lista de objetos de chiste o lista vacía si la petición falló
        """
        try:
            params = {'q': query, 'limit': limit}
            response = requests.get(f"{self.api_url}/search", params=params, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error al buscar chistes: {e}")
            return []
