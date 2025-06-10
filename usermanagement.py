#user_management
import os
import json
import time 
import querystuff as qs
from pathlib import Path
# check if files exist
def get_date() -> str:
    seconds = time.time()
    formatted_time = time.strftime("%Y-%m-%d", seconds)
    return formatted_time
def check_if_thing_even_exists() -> bool:
    path = '/users/'
    path_exists = os.path.exists(path)
    return path
def create_path():
    dir_path = Path("users")
    dir_path.mkdir(parents=True, exist_ok=True)
def create_user_list():
    with open("/users/userlist.json", 'w') as userlist:
        template = {"old_users": [], "new_users": []}
        json.dumps(template, userlist, indent=2)

def get_users() -> list:
    with open('/users/userlist.json', 'r') as nusers:
        users = nusers.json()
    return users

def get_new_users(user_list: list) -> list:
    nusers = []
    time_now = get_date()
    for user in user_list['new_users']:
        nusers.append(user)
        user_stuff = {"name": user, "updatedAt": time_now}
        user_list['old_users'].append(user_stuff)
    template = {"old_users": user_list['old_users'], "new_users": []}
    with open("users/userlist.json", 'w') as u:
        json.dumps(user_list, u, indent=2)
    return nusers

def ultimate_management():
    pathexists = check_if_thing_even_exists()
    if pathexists == True:
        user_list = get_users()
        new_users = get_new_users(user_list)
        for user in new_users:
            new_user = qs.final_thing(user)
            with open(f'/users/{new_user['data']['MediaListCollection']['user']['name']}.json', 'w') as f:
                json.dumps(new_user, f, indent=2)
    else:
        create_path()
        create_user_list()
        print("no users found")

# if not then create the path 

# keep track of when the user was last updated through a json file thats named user_list
# maybe just maybe also create an anime data base
# 