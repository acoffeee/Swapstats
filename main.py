import requests
import asyncio
import usermanagement as um
import os
import json
import update_db
um.ultimate_management()
swappers_info = {}
def get_user_info() -> dict:
  for user in os.listdir('users'):
    if user == 'userlist.json':
      continue
    else:
      # print(str(user))
      with open(f'users/{user}', 'r') as u:
        temp = json.load(u)
        swappers_info[temp['data']['MediaListCollection']['user']['name']] = temp
get_user_info()



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
for swapper in swappers_info:
  standerdized_swapper_list = standerdize(swappers_info[swapper])
  swapper_compatibility = {swapper: []}
  update_db.process_list(standerdized_swapper_list)
  print("stuff")
  for other_swapper in swappers_info:
    if other_swapper == swapper:
      continue
    else:
      other_swapper_list = swappers_info[other_swapper]
      other_swapper_sd_list = standerdize(other_swapper_list)
      matched_list = matchlists(standerdized_swapper_list, other_swapper_sd_list)
      compared_lists = compafinddifferences(matched_list)
      compatibility = calculatefinalstandarddeviationmean(compared_lists)
      format_compatibility = { "name": other_swapper, "rating": compatibility, "entries_shared": len(matched_list) }
      swapper_compatibility[swapper].append(format_compatibility)
    all_comparisions.append(swapper_compatibility)
with open("results.json", "w") as f:
  json.dump(all_comparisions, f, indent=2)