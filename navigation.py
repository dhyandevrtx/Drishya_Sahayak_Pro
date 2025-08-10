import requests
from geopy.geocoders import Nominatim
from config import Config
class Navigation:
    """
    Handles GPS-related functionalities.
    """
    def __init__(self):
        if not Config.GEOPY_USER_AGENT:
            raise ValueError("Geopy user agent is not configured in .env file.")
        self.geolocator = Nominatim(user_agent=Config.GEOPY_USER_AGENT)

    def get_current_location(self):
        """
        Gets the current location based on IP address.
        Note: This is an approximation. For real-world use, a hardware GPS module is better.
        """
        try:
            # Get location from IP
            response = requests.get("https://ipinfo.io/json", timeout=5)
            data = response.json()
            lat_lon = data["loc"]
            
            # Geocode to get a human-readable address
            location = self.geolocator.reverse(lat_lon, exactly_one=True, timeout=10)
            
            if location:
                address = location.address
                # Simplify the address
                address_parts = address.split(',')
                simplified_address = f"{address_parts[0].strip()}, {address_parts[1].strip()}"
                return f"You are near {simplified_address}"
            else:
                return "Could not determine a precise address."
                
        except Exception as e:
            print(f"Error fetching location: {e}")
            return "Unable to retrieve current location."
