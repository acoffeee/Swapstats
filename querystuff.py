#  query stuff.py
import requests
import asyncio
import animedatabase 
def query_swapper(user) -> dict:
    url = 'https://graphql.anilist.co'
    query =  '''
    query($userName: String){
                    MediaListCollection(userName: $userName, type: ANIME,status: COMPLETED, sort: FINISHED_ON ){
                        user{
                            name
                            statistics{
                                anime{
                                count
                                meanScore
                                standardDeviation
                                }
                            }
                        }
                        lists{
                        name
                            entries{
                                score
                                media{
                                    title{
                                        english
                                        romaji
                                        native
                                    }
                                    id
                                    tags{
                                    name
                                    rank
                                    }
                                    format
                                    season
                                    seasonYear
                                    episodes
                                    duration
                                    genres
                                    studios{
                                        edges{
                                            isMain
                                            node{
                                                name
                                            }
                                        }
                                    }
                                    staff{
                                        edges{
                                        role
                                            node{
                                                name{
                                                    full
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
        '''
    shtuff = {'userName': user}
    response = requests.post(url, json={'query': query, 'variables': shtuff})
    swapper_info = response.json()
    print(swapper_info)
    return swapper_info

def filter_completed_list(swapper_info: dict) -> dict:
    swapper_info['data']['MediaListCollection']['lists'] = swapper_info['data']['MediaListCollection']['lists'][0]
    for i in range(0,len(swapper_info['data']['MediaListCollection']['lists']['entries'])):
      anime = swapper_info['data']['MediaListCollection']['lists']['entries'][i]
      swapper_info['data']['MediaListCollection']['lists']['entries'][i] = {"score": anime['score'], "media": {"id": anime['media']['id']}}
      animedatabase.final_thing(anime)
    return swapper_info


async def query_swapper_with_error_handdling(swapper: str) -> dict:
    try:
      info = query_swapper(swapper)
      return info
    except:
      # print(info)
      if info['errors'][0]['message'] == "User not found":
        print("user doesnt exist")
      else: 
        for i in range(0,60):
          # print(f'rate limit rip, left: {60 - i}')
          await asyncio.sleep(1)
        await query_swapper_with_error_handdling(swapper)


def final_thing(swapper: str) -> dict:
    swapper_info = asyncio.run(query_swapper_with_error_handdling(swapper))
    filtered_swapper = filter_completed_list(swapper_info)
    return filtered_swapper
def main():
   return
if __name__=='__main__':
   main()
