import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    df = source.copy()
    
    # Parse the datetime
    dt = pd.to_datetime(df['date'])
    
    # Extract date string for grouping and display
    df['date_only'] = dt.dt.strftime('%m/%d/%Y')
    
    # Extract hour for pivoting
    df['hour'] = dt.dt.hour
    
    # Define the mapping from hour integer to target column name
    # 0 -> 12:00 AM, 1 -> 1:00 AM, ..., 11 -> 11:00 AM
    # 12 -> 12:00 PM, 13 -> 1:00 PM, ..., 23 -> 11:00 PM
    hour_mapping = {}
    for h in range(24):
        if h == 0:
            label = "12:00 AM"
        elif h < 12:
            label = f"{h}:00 AM"
        elif h == 12:
            label = "12:00 PM"
        else:
            label = f"{h-12}:00 PM"
        hour_mapping[h] = label
    
    # Group by date and hour, then aggregate. 
    # Using mean to handle multiple entries per hour. 
    # If there's only one non-null entry, mean returns that value.
    agg_df = df.groupby(['date_only', 'hour'])['zone_016'].mean().reset_index()
    
    # Pivot the table
    pivot_df = agg_df.pivot(index='date_only', columns='hour', values='zone_016')
    
    # Rename columns according to the mapping
    pivot_df = pivot_df.rename(columns=hour_mapping)
    
    # Reset index to make 'date' a column again
    pivot_df = pivot_df.reset_index()
    pivot_df = pivot_df.rename(columns={'date_only': 'date'})
    
    # Define the exact target column order
    target_cols = ['date', '1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', '6:00 AM', '7:00 AM', '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM', '12:00 PM', '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', '6:00 PM', '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM', '12:00 AM']
    
    # Ensure all target columns exist, filling missing ones with NaN if necessary
    for col in target_cols:
        if col not in pivot_df.columns:
            pivot_df[col] = pd.NA
            
    # Return the dataframe with columns in the exact target order
    return pivot_df[target_cols]