from ip2geotools.databases.noncommercial import DbIpCity
import pycountry
import requests
import dns
import dns.resolver

class domain():
    def __init__(self, url):
        self.url = url
        self.ip = ""
        self.location = ""
        self.reputation = ""
        self.category = ""

    def getIpAddress(self):
        try:
            self.ip = str(dns.resolver.resolve(self.url, 'A')[0])
        except:
            print("Can not resolve domain from:", self.url)
            self.ip = "Unknown"

    def getLocation(self):
        self.getIpAddress()
        try:
            response = DbIpCity.get(self.ip, api_key='free')
            self.location = pycountry.countries.get(alpha_2=response.country).name
        except:
            print("Can not get location of:", self.ip)
            self.location = "Unknown"

    url = 'https://talosintelligence.com/sb_api/remote_lookup'
    headers = {'accept': 'application/json, text/javascript, */*; q=0.01',
               'accept-encoding': "gzip, deflate",
               'accept-language': 'es-ES,es;q=0.9,en;q=0.8',
               "cache-control": "no-cache",
               "cookie": "__cfduid=de2347cf2dff531a8691cde4f2d09dba81602870231; cf_clearance=7aa4256378fa05cd6b4336279f5b1a7183acb345-1602870248-0-1za4dcf588zc42070cczeb5bed6e-150; _talos_website_session=NnhBKzA0anV1bS91WlpIa1FOTWJXK0hZd3IyZlIxejM2cGZZM1VOcldzRzlDSGVpcGNhbnJBaTArekZwaVc3YUIzQ2dYNHNDN0xCZXhnYXVIY3Vpbko2TExqTUZDTWFhT1YyMmRlSDJ5U2tsN2ltNWJ5RnBIWUV0QmZLcUV6dXJTSHlHQ3hTOFBjTWpOZ0VTOFpuZDhnUFRyR1NwOHUrZTlsQmdoVDQwdXpRcC8wUG5mNkFnQ2Fma3lPbkxRbXhEbGt0dFIxRnozVGVnWlBvOWlTVzJtc0k5bWlSVWJjVURoMWY5eVQ4cUZMaz0tLU1vekoweS9QZ0g3bnNDNmRDNzNadEE9PQ%3D%3D--fb72e04c29a0a1bad7c9bd24ce0b44e55a191d90",
               "pragma": "no-cache",
               "referer": "https://talosintelligence.com/reputation_center/lookup?search=",
               "sec-fetch-dest": "empty",
               "sec-fetch-mode": "cors",
               "sec-fetch-site": "same-origin",
               "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"}

    def getReputation(self):
        params = {"hostname": "SDSv3", "query_string": "/score/single/json?url=" + self.url}
        response_details = requests.get(url=domain.url, headers=domain.headers, params=params)
        # print(response_details.json())
        try:
            self.reputation = response_details.json()["threat_score"]
        except:
            print("Can not get reputation from: ", self.url)
            self.reputation = "Unknown"
        try:
            self.category = response_details.json()["threat_categories"]
        except:
            print("Can not get category from: ", self.url)
            self.category = "Unknown"

    def urlToDict(self):
        self.getLocation()
        self.getReputation()
        return {"URL" : self.url, "IP": self.ip, "Location": self.location, "Reputation" : self.reputation, "Category" : self.category}


if __name__ == "__main__":
    urlObj = domain("google.com")
    print(urlObj.urlToDict())

    urlObj2 = domain("coronavirus-sochi.ru")
    print(urlObj2.urlToDict())