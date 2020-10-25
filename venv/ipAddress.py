from ip2geotools.databases.noncommercial import DbIpCity
import pycountry
import requests

class ipAddress:
    def __init__(self, ip):
        self.ip = ip
        self.location = ""
        self.emailReputation = ""
        self.webReputation = ""

    def getLocation(self):
        try:
            response = DbIpCity.get(self.ip, api_key='free')
            self.location = pycountry.countries.get(alpha_2=response.country).name
        except:
            print("Can not get location of:", self.ip)
            self.location = "Unknown"

    url = 'https://talosintelligence.com/sb_api/query_lookup'
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
        params_details = {'query': '/api/v2/details/ip/', 'query_entry': self.ip, 'offset': '0', 'order': 'ip asc'}
        response_details = requests.get(url=ipAddress.url, headers=ipAddress.headers, params=params_details)
        # print(response_details.json())
        try:
            self.emailReputation = response_details.json()["email_score_name"]
        except:
            print("Can not get email reputation from: ", self.ip)
            self.emailReputation = "Unknown"
        try:
            self.webReputation = response_details.json()["web_score_name"]
        except:
            print("Can not get web reputation from: ", self.ip)
            self.webReputation = "Unknown"

    def ipToDict(self):
        self.getLocation()
        self.getReputation()
        return {"IP": self.ip, "Location": self.location, "Email Reputation" : self.emailReputation, "Web Reputation" : self.webReputation}


if __name__ == "__main__":
    ipObj = ipAddress("8.8.8.8")
    print(ipObj.ipToDict())