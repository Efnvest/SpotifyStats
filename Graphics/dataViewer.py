import pandas as pd
import json
import matplotlib.pyplot as plt



def viewHistory(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)


    df = pd.DataFrame(data)


    # Convert milliseconds to hours
    df["hours_played"] = df["ms_played"] / (1000 * 60 * 60)



    # Sort by year and month
    df = df.sort_values(by=["year", "month_num"])

    # Create a combined date column for plotting
    df["date"] = df["year"].astype(str) + "-" + df["month_num"].astype(str).str.zfill(2)

    # Plot the data
    plt.figure(figsize=(12, 6))
    plt.plot(df["date"], df["hours_played"], marker='o', label="Listening Hours")

    # Add labels to each point
    for i in range(len(df)):
        plt.text(df["date"].iloc[i], df["hours_played"].iloc[i], df["master_metadata_track_name"].iloc[i], fontsize=6,rotation=45,ha='center')


    # Format the plot
    plt.xticks(rotation=45, ha="right")  # Rotate x-axis labels for better readability
    plt.xlabel("Date (Year-Month)")
    plt.ylabel("Listening Hours")
    plt.title("Listening Trends Over Time")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.ylim(0, 175)


    # Show the plot
    plt.show()
