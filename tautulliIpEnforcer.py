from TautulliApiHandler import TautulliApiHandler
import datetime

### USER DEFINED VARIBALES FOR YOUR INSTALLATION ###
def GetTautInfo():
    tautulliIp   = "172.17.0.20"                        # IP Address of Tautulli
    tautulliPort = 8181                                 # Port of Tautulli
    tautulliApi  = "bf2b943c2fed4fb28d8151b7147cdd66"   # API Key for Tautulli
    # Message to display to a user of a blacklisted IP
    blackListMsg = "PLEX IP ENFORCER - THIS IP ADDRESS IS BLACKLISTED"
    concurrentMsg = "PLEX IP ENFORCER - EXCESSIVE ACCOUNT SHARING IS PROHIBITED. PLEASE CONSIDER PURCHASING YOUR OWN ACCOUNT"

    return tautulliIp, tautulliPort, tautulliApi, blackListMsg, concurrentMsg

def EnforceIpBans(tActivitySessions, tapi, blackListMsg):
    try:
        f = open("banned_ips.txt", "r")
        bannedIps = f.read().splitlines() # Use this rather than readlines so we remove the newline character
        f.close()

        for session in tActivitySessions:
            if(session["ip_address"] in bannedIps or session["ip_address_public"] in bannedIps):
                msg = "BANNED IP: " + session["user"] + " is using the banned IP of " + session["ip_address"] + " / " + session["ip_address_public"]
                print(msg)
                print("Terminating session")
                EnforcementLogger(msg)
                tapi.TerminateSession(session["session_key"], blackListMsg)
    except:
        print("There was an error running the EnforceIpBans Function")
        pass

def GetConcSettings():
    try:
        f = open("concurrent_ip_limit.txt", "r")
        lines = f.read().splitlines() # Use this rather than readlines so we remove the newline character
        f.close()
        concSettings = {}
        for line in lines:
            splitSettings = line.split(";")
            concSettings[splitSettings[0].lower()] = splitSettings[1]

        return concSettings
    except:
        pass

def EnforceConcurrent(tActivitySessions, tapi, concurrentMsg):
    try:
        concSettings = GetConcSettings()

        dataByUser = {}
        # Loop through each session and add to a dictionary where key is the username
        for session in tActivitySessions:
            if(session["user"] in dataByUser):
                # User is already in the dictionary so append to that users array
                dataByUser[session["user"]].append(session)
            else:
                # User isnt in dictionary so add key data pair with username as key and an ampty array as data
                dataByUser[session["user"]] = []
                dataByUser[session["user"]].append(session) # Append that session to the array of that user

        # By this point we have a dictionary of current users with their apropriate sessions
        for user in dataByUser:
            # Loop through each user to work on only their sessions at a time
            ipList = []
            for session in dataByUser[user]:
                if(not session["ip_address"] in ipList):
                    ipList.append(session["ip_address"])
                if(not session["ip_address_public"] in ipList):
                    ipList.append(session["ip_address_public"])
            
            #print(user + " has " + str(len(ipList)) + " unique IPs currently running")
            if user.lower() in concSettings:
                if(len(ipList) > int(concSettings[user.lower()])):
                    msg = "CONCURRENT IP ABUSE: " + user + " has " + str(len(ipList)) + " unique IPs currently running but is limited to " + concSettings[user.lower()]
                    print(msg)
                    print("Terminating sessions")
                    EnforcementLogger(msg)
                    for session in dataByUser[user]:
                        tapi.TerminateSession(session["session_key"], concurrentMsg)
    except:
        pass

def EnforcementLogger(message):
    try:
        now = datetime.datetime.now()
        preStringDate = now.strftime("%Y-%m-%d %H:%M:%S")
        f = open("enforce_log.txt", "a")
        f.write(preStringDate + ": " + message + "\n")
        f.close()

    except:
        print("There was a problem logging the error")
        pass

def Main():
    print("\nStarting Tautulli IP Enforcer")
    tIP, tPORT, tAPIKEY, blackListMsg, concurrentMsg = GetTautInfo()
    tapi = TautulliApiHandler(tIP, tPORT, tAPIKEY)
    tActivityData = tapi.GetActivity()
    if(int(tActivityData["stream_count"]) > 0):
        print("There are currently " + str(tActivityData["stream_count"]) + " streams active")

        EnforceIpBans(tActivityData["sessions"], tapi, blackListMsg) # Check and Enforce IP bans

        print()

        EnforceConcurrent(tActivityData["sessions"], tapi, concurrentMsg) # Check and Enforce Concurrent Limits

    else:
        print("No streams found")
    

        

Main()