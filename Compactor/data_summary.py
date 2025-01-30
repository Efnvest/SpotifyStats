import json
import pandas as pd

# Load the streaming history JSON file
file_path = 'MyDataBroker/summary.json'
with open(file_path, 'r') as file:
    data = json.load(file)

# Convert to DataFrame
df = pd.DataFrame(data)

# Convert timestamp to datetime and extract useful time-related features
df['ts'] = pd.to_datetime(df['ts'])
df['date'] = df['ts'].dt.date
df['hour'] = df['ts'].dt.hour
df['year'] = df['ts'].dt.year
df['month'] = df['ts'].dt.month_name()

# Basic data cleaning: replace null values with appropriate defaults
df.fillna({'master_metadata_track_name': 'Unknown', 
           'master_metadata_album_artist_name': 'Unknown', 
           'master_metadata_album_album_name': 'Unknown', 
           'episode_name': 'Unknown',
           'episode_show_name': 'Unknown'}, inplace=True)

# Calculate total listening time in hours
total_listening_time_hours = df['ms_played'].sum() / (1000 * 60 * 60)

# Most played track or episode by total listening time
most_played = df.groupby('master_metadata_track_name')['ms_played'].sum().idxmax()
most_played_duration = df.groupby('master_metadata_track_name')['ms_played'].sum().max() / (1000 * 60)

# Most listened-to artist
most_listened_artist = df.groupby('master_metadata_album_artist_name')['ms_played'].sum().idxmax()

# Count of streams per platform
platform_usage = df['platform'].value_counts()

# Most skipped tracks
most_skipped_tracks = df[df['skipped'] == True]['master_metadata_track_name'].value_counts().head(5)

# Podcast vs music split (count and time spent)
podcast_plays = df[df['episode_name'] != 'Unknown'].shape[0]
music_plays = df[df['master_metadata_track_name'] != 'Unknown'].shape[0]

podcast_time = df[df['episode_name'] != 'Unknown']['ms_played'].sum() / (1000 * 60)
music_time = df[df['master_metadata_track_name'] != 'Unknown']['ms_played'].sum() / (1000 * 60)
# Calculate song skip rate
total_songs = df[df['master_metadata_track_name'] != 'Unknown'].shape[0]
skipped_songs = df[(df['master_metadata_track_name'] != 'Unknown') & (df['skipped'] == True)].shape[0]
skip_rate = (skipped_songs / total_songs) * 100 if total_songs > 0 else 0

# Hourly listening trends
hourly_trends = df.groupby('hour')['ms_played'].sum()

# Monthly listening trends
monthly_trends = df.groupby('month')['ms_played'].sum()

ip_addresses_used = df['ip_addr'].value_counts()

# Print insights
""" print(f"Total Listening Time (hours): {total_listening_time_hours:.2f}")
print(f"Most Played Track: {most_played} ({most_played_duration:.2f} minutes)")
print(f"Most Listened Artist: {most_listened_artist}")
print("\nPlatform Usage:")
print(platform_usage)
print("\nMost Skipped Tracks:")
print(most_skipped_tracks)
print("\nPodcast vs Music:")
print(f"Podcast Plays: {podcast_plays}, Music Plays: {music_plays}")
print(f"Podcast Listening Time: {podcast_time:.2f} minutes, Music Listening Time: {music_time:.2f} minutes")
print("\nHourly Listening Trends:")
print(hourly_trends)
print("\nMonthly Listening Trends:")
print(monthly_trends) """
print(f"\nSong Skip Rate: {skip_rate:.2f}%")
print("\nIpaddress used:")
print(ip_addresses_used)

