import requests
import discord
import threading
import time
import hashlib
import json
import sys


admin_file = ".admins"
open(admin_file, "a").close()
hashes_file = ".hashes"
open(hashes_file, "a").close()


admins = []
watching = {}

user, password = sys.argv[1:]

client = discord.Client()
client.login(user, password)


def watcher(client,channel):
    while True:
        print("Checking websites")
        for k,v in list(watching.items()):
            r = requests.get(k)
            hash = hashlib.sha224(r.text.encode("utf-8")).hexdigest()
            if hash != v:
                s=""
                s += "```\n"
                s += r.text
                s += "\n```"
                client.send_message(channel, "Webpage has updated! "+k+"\n"+s)
                print("ITS CHANGED: "+k)
                watching[k] = hash
                print(hash)

        f = open(admin_file, "w+")
        f.write(json.dumps(watching))
        f.close()
        f = open(hashes_file, "w+")
        f.write(json.dumps(watching))
        f.close()
        time.sleep(10)


@client.event
def on_message(message):
    msg = message.content.split(" ")

    if msg[0] == "!mods":
        client.send_message(message.channel, "@MrDetonia @nickforall @kolpet @nepeat") 

    if msg[0] == ".help":
        s = "I'm a watcherbot! Tell an admin too add the webpage with .add.  Curret admins: " + " ".join(admins)
        client.send_message(message.channel, s)
    if message.author.name not in admins:
        return

    if msg[0] == ".admin":
        client.send_message(message.channel, "Added admin "+msg[1])
        admins.append(msg[1])

    if msg[0] == ".add":
        client.send_message(message.channel, "Added webpage for watching: "+msg[1])
        r = requests.get(k)
        hash = hashlib.sha224(r.text.encode("utf-8")).hexdigest()
        watching[msg[1]] = hash


@client.event
def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    channel = client.servers[0].get_default_channel()
    t = threading.Thread(target=watcher, args=(client,channel))
    t.daemon = True
    t.start()
    print('-----k-')


try:
    admin_info = json.loads(open(admin_file,"r+").read())
except:
    admins = ["Foxboron", "nickforall", "Retsam19"]
else:
    admins = admin_info

try:
    hashes_info = json.loads(open(hashes_file,"r+").read())
except:
    # url => hash
    watching = {"http://104.131.44.161/": "d9efb9409d1c182e3f879740a08e93a9563c49ac5571b5a8818e8133"}
else:
    watching = hashes_info

while True:
    try:
        client.run()
    except:
        pass





