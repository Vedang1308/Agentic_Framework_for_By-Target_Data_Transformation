import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the date column
    # The source format is '%m/%d/%Y %H:%M'
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract the date string for grouping/indexing
    df['date_str'] = df['datetime'].dt.strftime('%m/%d/%Y')
    
    # 3. Extract the hour (0-23)
    df['hour_24'] = df['datetime'].dt.hour
    
    # 4. Map 24-hour format to 12-hour AM/PM format strings
    def map_hour_to_label(h):
        if h == 0:
            return '12:00 AM'
        elif 1 <= h <= 11:
            return f'{h}:00 AM'
        elif h == 12:
            return '12:00 PM'
        else: # 13-23
            return f'{h-12}:00 PM'
            
    df['hour_label'] = df['hour_24'].apply(map_hour_to_label)
    
    # 5. Pivot the data
    # We group by date_str and hour_label, aggregating the zone_016_cooling_sp values.
    # Using 'mean' to handle multiple entries per hour (e.g., every 5 mins).
    # If a specific hour has no data for a date, it will be NaN.
    pivot_df = df.pivot_table(
        index='date_str', 
        columns='hour_label', 
        values='zone_016_cooling_sp', 
        aggfunc='mean'
    )
    
    # 6. Define the target column order
    # The target columns are in chronological order starting from 1:00 AM
    target_hour_cols = [
        '1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', '6:00 AM', 
        '7:00 AM', '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM', '12:00 PM', 
        '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', '6:00 PM', 
        '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM', '12:00 AM'
    ]
    
    # 7. Ensure all target columns exist in the pivot result
    # If some hours are completely missing from the dataset, add them as NaN columns
    for col in target_hour_cols:
        if col not in pivot_df.columns:
            pivot_df[col] = np.nan
            
    # 8. Reset index to make 'date_str' a column named 'date'
    pivot_df = pivot_df.reset_index()
    pivot_df = pivot_df.rename(columns={'date_str': 'date'})
    
    # 9. Select and order the final columns
    target_columns = ['date'] + target_hour_cols
    result_df = pivot_df[target_columns]
    
    return result_df