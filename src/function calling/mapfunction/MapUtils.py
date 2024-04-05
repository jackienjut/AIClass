import requests

class MapUtils:
    amap_key = "6d672e6194caa3b639fccf2caf06c342"

    def get_location_coordinate(self,location, city):
        url = f"https://restapi.amap.com/v3/geocode/geo?address={location}&city={city}&key={self.amap_key}"
        response = requests.get(url)
        data = response.json()
        if data["status"] == "1":
            return data["geocodes"][0]["location"]
        else:
            return None

    def search_nearby_poi(self,longitude, latitude, keyword):
        url = f"https://restapi.amap.com/v3/place/around?key={self.amap_key}&location={longitude},{latitude}&keywords={keyword}&radius=1000&offset=20&page=1&extensions=all"
        response = requests.get(url)
        data = response.json()
        if data["status"] == "1":
            return data["pois"]
        else:
            return None