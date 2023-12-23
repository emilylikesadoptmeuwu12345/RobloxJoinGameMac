#!/usr/local/bin/python3

import os
import requests
import argparse
import getpass
import json
import subprocess
import datetime
import time
user = getpass.getuser()
parser = argparse.ArgumentParser(description="A program to join a game on Roblox just using arguments")
cookie = ""

parser.add_argument("--gameid",type=int,help="Game ID to join",required=False)
parser.add_argument("--jobid",help="Job ID to join (must have the game id arg)",required=False)
args = parser.parse_args()
if not os.path.exists(f"/Users/{user}/.rbxcookie"):
    print("Please make the rbxcookie file first before executing and put your ROBLOSECURITY cookie inside the file")
    print(f"Execute this inside terminal to make it: nano /Users/{user}/.rbxcookie")
    exit()
with open(f"/Users/{user}/.rbxcookie","r") as f:
    cookie = f.read().strip()
print("Checking if cookie is valid..") # so that there will be an auth ticket to join a game
rbxuser = requests.get("https://users.roblox.com/v1/users/authenticated",headers={"Cookie": f".ROBLOSECURITY={cookie}"})
if rbxuser.status_code != 200:
    print(f"Did your ROBLOSECURITY cookie expire?. Status {rbxuser.status_code}")
    print(rbxuser.text)
    exit()

def launchGame(placeid : int,jobid=""):
    haha = f"&gameId={jobid}"
    if jobid == "":
        haha = ""
    print("Getting CSRF")
    csrf = requests.post("https://auth.roblox.com/v1/authentication-ticket",headers={"Cookie" : f".ROBLOSECURITY={cookie}"})
    if not "x-csrf-token" in csrf.headers:
        print("No CSRF Token given, exiting..")
        exit()
    print("Getting AUTH Ticket")
    ticket = requests.post("https://auth.roblox.com/v1/authentication-ticket",headers={"Cookie": f".ROBLOSECURITY={cookie}","Orgin": "https://www.roblox.com","Referer": "https://www.roblox.com","X-CSRF-TOKEN": csrf.headers["x-csrf-token"]})
    if ticket.status_code != 200:
        print(f"Error while getting AUTH Ticket. Status {ticket.status_code}")
        print(ticket.text)
        exit()
    final = f"roblox-player:1+launchmode:play+gameinfo:{ticket.headers['rbx-authentication-ticket']}+timestamp:{str(round(time.time() * 1000))}+placelauncherurl:https://assetgame.roblox.com/game/PlaceLauncher.ashx?request=RequestGameJob&browserTrackerId=147062882894&placeId={placeid}{haha}&isPlayTogetherGame=false+browsertrackerid:147062882894+robloxLocale:en_us+gameLocale:en_us+channel:"
    gamename = json.loads(requests.get(f"https://games.roblox.com/v1/games/multiget-place-details?placeIds={placeid}",headers={"Cookie": f".ROBLOSECURITY={cookie}"}).text)
    if len(gamename) == 0:
        print("Game ID invalid or error! exiting..")
        exit()
    subprocess.Popen(["open",final])
    print(f"Playing {gamename[0]['name']} by {gamename[0]['builder']}. Time is {datetime.datetime.now().strftime('%H:%M:%S')}")
print(f"Welcome {json.loads(rbxuser.text)['displayName']}!")
if args.gameid:
    if args.jobid:
        launchGame(args.gameid,args.jobid)
    else:
        launchGame(args.placeid)
