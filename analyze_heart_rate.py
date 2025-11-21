import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

# Read the CSV file
df = pd.read_csv('data/my_activity_data=20251119143115.csv')

# Print column names to understand the structure
print("Column names:")
print(df.columns.tolist())
print("\nFirst few rows:")
print(df.head())

# Check if we have the required columns
if 'start_date_local' in df.columns and 'average_heartrate' in df.columns:
    # Filter for running activities only
    # Check if we have 'type' or 'sport_type' column
    if 'sport_type' in df.columns:
        df_filtered = df[(df['sport_type'] == 'Run') &
                          (df['average_heartrate'].notna()) &
                          (df['average_heartrate'] > 0)].copy()
    elif 'type' in df.columns:
        df_filtered = df[(df['type'] == 'Run') &
                          (df['average_heartrate'].notna()) &
                          (df['average_heartrate'] > 0)].copy()
    else:
        df_filtered = df[(df['average_heartrate'].notna()) &
                          (df['average_heartrate'] > 0)].copy()

    # Convert start_date_local to datetime
    df_filtered['date'] = pd.to_datetime(df_filtered['start_date_local'])

    # Filter for activities starting from July 1, 2024
    df_filtered = df_filtered[df_filtered['date'] >= '2024-07-01']

    # Sort by date in ascending order
    df_filtered = df_filtered.sort_values('date')

    print(f"\nAnalyzing {len(df_filtered)} activities")
    print(f"Average Heart Rate: {df_filtered['average_heartrate'].mean():.2f} bpm")
    print(f"Date range: {df_filtered['date'].min()} to {df_filtered['date'].max()}")

    # Create the plot
    plt.figure(figsize=(14, 6))
    plt.plot(df_filtered['date'],
             df_filtered['average_heartrate'],
             marker='o',
             linestyle='-',
             alpha=0.7,
             markersize=4,
             linewidth=1)

    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Average Heart Rate (bpm)', fontsize=12)
    plt.title('Average Heart Rate Over Time', fontsize=14)
    plt.grid(True, alpha=0.3)

    # Format x-axis to show dates nicely
    plt.gcf().autofmt_xdate()
    date_format = mdates.DateFormatter('%Y-%m-%d')
    plt.gca().xaxis.set_major_formatter(date_format)

    # Add a horizontal line for the mean
    mean_hr = df_filtered['average_heartrate'].mean()
    plt.axhline(y=mean_hr, color='r', linestyle='--', alpha=0.5,
                label=f'Mean: {mean_hr:.1f} bpm')

    plt.legend()
    plt.tight_layout()

    # Save the plot
    plt.savefig('data/heart_rate_analysis.png', dpi=300, bbox_inches='tight')
    print("\nChart saved to: data/heart_rate_analysis.png")

    plt.show()
else:
    print("\nRequired columns not found. Available columns:")
    print(df.columns.tolist())
