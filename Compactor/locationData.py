import json
import pandas as pd
import requests
import time


# Fetches locationsdata via 
def fetchLocationData(local_file_path):
    with open(local_file_path, 'r') as file:
        data = json.load(file)

    df = pd.DataFrame(data)
    #do the same but for city region and country, mabye use a dict insted of list. 
    loc_list = []
    city_lsit = []
    region = []
    country = []

    #cycling through json file - fetching 'ip' info and appending them to different lists. 
    for i in range(len(df)):
        #Limit strain on ipinfo.io servers, when processing larger datasets. 
        time.sleep(0.1)

        ip = (df['ip_addr'].iloc[i])
        url = (f'https://ipinfo.io/{ip}')
        http_request = requests.get(url)
        if (http_request.status_code == 200):
            locations_json = http_request.json()
            loc_list.append(locations_json.get('loc'))
            city_lsit.append(locations_json.get('city'))
            region.append(locations_json.get('region'))
            country.append(locations_json.get('country'))

        elif (http_request.status_code == 429):
            print('Free limit of 50,000 requests exceeded for ipinfo.io, cooldown 1 month')
            break
        else:
            print('Failed to fetch data')

    df['loc'] = loc_list
    df['city'] = city_lsit
    df['region'] = region
    df['country'] = country
    file.close()

    # Saving to json file as one large dict
    with open(local_file_path, 'w') as out_file:
        json.dump(df.to_dict(orient='records'), out_file, indent=4)

    print(f"Summary saved to {'MyDataBroker/miniIp.json'}")




