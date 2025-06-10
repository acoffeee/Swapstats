#user_management
import os
import json
import time 
import querystuff as qs
from pathlib import Path
# check if files exist
import datetime
def get_date() -> str:
    now = datetime.datetime.now()
    today = now.date()
    return today

def check_if_thing_even_exists() -> bool:
    path = 'users'
    path_exists = os.path.exists(path)
    return path_exists
def create_path():
    dir_path = Path("users")
    dir_path.mkdir(parents=True, exist_ok=True)
def create_user_list():
    people = []
    print("type \"no\" if you dont want to add anyone")
    while True:
        ask = input("add user (loops if you want multiple): ")
        if ask.lower() == "no":
            break
        else:
            people.append(ask)
    with open("users/userlist.json", 'w') as userlist:
        template = {"old_users": [], "new_users": people}
        json.dump(template, userlist, indent=2)

def get_users() -> list:
    with open('users/userlist.json', 'r') as nusers:
        users = json.load(nusers)
    return users

def get_new_users(user_list: list) -> list:
    nusers = []
    date = get_date()
    time_now = f'{date.year}-{date.month}-{date.day}'
    for user in user_list['new_users']:
        nusers.append(user)
        user_stuff = {"name": user, "updatedAt": time_now}
        user_list['old_users'].append(user_stuff)
    template = {"old_users": user_list['old_users'], "new_users": []}
    with open("users/userlist.json", 'w') as u:
        json.dump(template, u, indent=2)
    return nusers

def ultimate_management():
    pathexists = check_if_thing_even_exists()
    if pathexists == True:
        user_list = get_users()
        new_users = get_new_users(user_list)
        for user in new_users:
            new_user = qs.final_thing(user)
            with open(f"users/{new_user['data']['MediaListCollection']['user']['name']}.json", 'w') as f:
                json.dump(new_user, f, indent=2)
    else:
        create_path()
        create_user_list()
        print("no users found")

# if not then create the path 

# keep track of when the user was last updated through a json file thats named user_list
# maybe just maybe also create an anime data base
# 