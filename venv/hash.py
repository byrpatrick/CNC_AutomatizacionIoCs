import requests

class hash:
    def __init__(self, hashCode, defLstA = ["McAfee", "ESET-NOD32", "F-Secure", "Kaspersky"]):
        self.hashCode = hashCode
        self.lstAntiV = defLstA
        self.antiVDict = {antiV : "undetected" for antiV in self.lstAntiV}

    url = "https://www.virustotal.com/ui/search?"
    headers = {'accept': 'application/json, text/javascript, */*; q=0.01',
               'accept-encoding': "gzip, deflate",
               'accept-language': 'es-ES,es;q=0.9,en;q=0.8',
               "cache-control": "no-cache",
               "pragma": "no-cache",
               "referer": "https://www.virustotal.com/",
               "sec-fetch-dest": "empty",
               "sec-fetch-mode": "cors",
               "sec-fetch-site": "same-origin",
               "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"}

    def checkHash(self):
        params = {'query': self.hashCode}
        response = requests.get(hash.url, headers = hash.headers, params= params)
        result = response.json()
        try:
            resultad = result["data"][0]['attributes']['last_analysis_results']
            for antivirus in self.lstAntiV:
                self.antiVDict[antivirus] = resultad[antivirus]['category']
        except:
            print(self.hashCode + ": no response")

    def hashToDict(self):
        self.checkHash()
        return {"Hash" : self.hashCode,
                "Results" : self.antiVDict}


if __name__ == "__main__":
    hashObj = hash("3a97d9b6f17754dcd38ca7fc89caab04")
    print(hashObj.hashToDict())
    {'Hash': '3a97d9b6f17754dcd38ca7fc89caab04',
     'Results': {'McAfee': 'undetected', 'ESET-NOD32': 'undetected', 'F-Secure': 'undetected',
                 'Kaspersky': 'malicious'}}

    hashObj2 = hash("56f423c7a7fef041f3039319f2055509")
    print(hashObj2.hashToDict())


