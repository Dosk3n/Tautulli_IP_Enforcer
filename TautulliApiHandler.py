import requests, json

class TautulliApiHandler:

    def __init__(self, ipaddr, port, apikey):
        self.ipaddr = ipaddr
        self.port = str(port)
        self.apikey = apikey

    def GetActivity(self):
        try:
            url = "http://" + self.ipaddr + ":" + self.port + "/api/v2?apikey=" + self.apikey + "&cmd=get_activity"
            r = requests.get(url)

            if r.status_code == 200:
                if(r.json()["response"]["result"] == "success"):
                    return r.json()["response"]["data"]
                else:
                    return False

            else:
                return False
        except:
            return False

    def TerminateSession(self, sessionKey, message = "SESSION TERMINATED"):
        try:
            url = "http://" + self.ipaddr + ":" + str(self.port) + "/api/v2?apikey=" + self.apikey + "&cmd=terminate_session&session_key=" + str(sessionKey) + "&message=" + message
            r = requests.get(url)

            if r.status_code == 200:
                if(r.json()["response"]["result"] == "success"):
                    return True
                else:
                    return False

            else:
                return False
        except:
            return False