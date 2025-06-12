import requests
import asyncio
import usermanagement as um
import os
import json
import update_db
import handle_main_io as hmio






def standerdize(thy_swapper):
  different_lists = thy_swapper['data']['MediaListCollection']['lists']
  temp = []
  for list_name in different_lists:
    temp = different_lists['entries']
    break
  # print(temp)
  new_list = []
  mean = thy_swapper['data']['MediaListCollection']['user']['statistics']['anime']['meanScore'];
  SD = thy_swapper['data']['MediaListCollection']['user']['statistics']['anime']['standardDeviation'];
  if temp[4]['score'] > 11 or temp[11]['score'] > 11:
    formatscore = 1
  else:
    formatscore = 10
  for anime in temp:
     if anime['score'] == 0:
        continue
     else: 
      new_score = ((anime['score'] * formatscore) - mean) / SD
      new_entry = {"score": new_score, "id": anime['media']['id']}
      new_list.append(new_entry)
  return new_list

def matchlists(listofmainuser, listofotherperson):
    matched_anime = []
    # //console.log(listofmainuser[34])
    for anime in listofmainuser:
      for other_anime in listofotherperson:
        if other_anime['id'] == anime['id']:
          anime = { "id": anime['id'], "useroneSD": anime['score'], "usertwoSD": other_anime['score']}
          matched_anime.append(anime)
          break
    return matched_anime

def compafinddifferences(formatted_list):
  differenceofscores = []
  for anime in formatted_list:
    difference = abs(anime['useroneSD'] - anime['usertwoSD'])
    differenceofscores.append(difference)
  # console.log(differenceofscores);
  return differenceofscores

def calculatefinalstandarddeviationmean(bunchonumbers):
  sum = 0
  for difference in bunchonumbers:
    sum += difference
  finalanswer = sum / len(bunchonumbers)
  return finalanswer

all_comparisions = []


if os.path.exists("anime.db"):
  nusers = um.ultimate_management()
else:
  for i in range(0,2):
    nusers = um.ultimate_management()

existing_swappers = hmio.handle_some_input()
swappers_info = {}
def get_user_info(swappers_in_db_already):
  for swapper in swappers_in_db_already:
    with open(f'users/{swapper}.json', 'r') as u:
       temp = json.load(u)
    swappers_info[temp['data']['MediaListCollection']['user']['name']] = temp



 
def calculate_new_people(nusers):
  get_user_info(existing_swappers)
  for new_user in nusers:
    with open(f'users/{new_user.lower()}.json', 'r') as f:
      u_info = json.load(f)
    standerdized_swapper_list = standerdize(u_info)
    swapper_compatibility = {new_user: []}
    update_db.process_list(standerdized_swapper_list)
    swappers_info[u_info['data']['MediaListCollection']['user']['name']] = u_info
    print(swappers_info)
    for other_swapper in swappers_info:
        if other_swapper.lower() == new_user.lower():
          continue
        other_swapper_list = swappers_info[other_swapper]
        other_swapper_sd_list = standerdize(other_swapper_list)
        matched_list = matchlists(standerdized_swapper_list, other_swapper_sd_list)
        compared_lists = compafinddifferences(matched_list)
        compatibility = calculatefinalstandarddeviationmean(compared_lists)
        format_compatibility = { "name": other_swapper, "rating": compatibility, "entries_shared": len(matched_list) }
        hmio.handle_output(new_user, other_swapper,  compatibility, len(matched_list))
        swapper_compatibility[new_user].append(format_compatibility)
        all_comparisions.append(swapper_compatibility)
  with open("results.json", "w") as f:
    json.dump(all_comparisions, f, indent=2)
calculate_new_people(nusers)