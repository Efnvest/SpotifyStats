import json
import pandas as pd
import os

# Compacter used for extracting the just the information needed from the data set.
# compilying into one json file. streaming_summary.json

def streamingHistory(folder_path):
    json_files = [f for f in os.listdir(folder_path) if f.endswith('.json')]
    df_list = []
    for json_file in json_files:
        with open(os.path.join(folder_path, json_file), 'r') as file:
            data = json.load(file)
            df_list.append(pd.DataFrame(data))

    df = pd.concat(df_list, ignore_index=True)

    # Convert timestamp to datetime
    #TODO: dont use timestap, use 'official_timestamp'
    df['ts'] = pd.to_datetime(df['ts'])
    df["month_num"] = df['ts'].dt.month
    df['year'] = df['ts'].dt.year

    # Basic data cleaning: replace null values with appropriate defaults
    #df.fillna({'master_metadata_track_name': 'Unknown', 
    #           'master_metadata_album_artist_name': 'Unknown', 
    #           'master_metadata_album_album_name': 'Unknown', 
    #           'episode_name': 'Unknown',
    #           'episode_show_name': 'Unknown'}, inplace=True)

    # Ignores any Unknown track - same as noe podcast make it to the top
    df = df[df['master_metadata_track_name'] != None]

    # Data groups
    monthly_trends = df.groupby(['year', 'month_num']).agg({'ms_played': 'sum'}).reset_index()

    most_used_ip = df.groupby(['year', 'month_num', 'ip_addr']).size().reset_index(name='count')
    most_used_ip = most_used_ip.loc[most_used_ip.groupby(['year', 'month_num'])['count'].idxmax()]

    most_listen_song = df.groupby(['year', 'month_num', 'master_metadata_track_name'])['ms_played'].sum().reset_index(name='count')
    most_listen_song = most_listen_song.loc[most_listen_song.groupby(['year', 'month_num'])['count'].idxmax()]

    # Merge the two groups into one df
    monthly_summary = monthly_trends.merge(most_used_ip[['year', 'month_num', 'ip_addr']], on=['year', 'month_num'])
    monthly_summary = monthly_summary.merge(most_listen_song[['year', 'month_num', 'master_metadata_track_name']], on=['year', 'month_num'])

    # Convert to desired JSON format
    summary = monthly_summary.to_dict(orient='records')

    # Save summary to a JSON file
    summary_file = 'Compactor/streaming_summary.json'

    with open(summary_file, 'w') as out_file:
        json.dump(summary, out_file, indent=4)

    print(f"Summary saved to {summary_file}")


