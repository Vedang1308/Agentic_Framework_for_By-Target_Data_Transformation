import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the datetime column
    df['datetime'] = pd.to_datetime(df['date'])
    
    # 2. Extract date string and hour
    df['date_str'] = df['datetime'].dt.strftime('%m/%d/%Y')
    df['hour'] = df['datetime'].dt.hour
    
    # 3. Map hour (0-23) to target column names
    def hour_to_label(h):
        if h == 0:
            return '12:00 AM'
        elif 1 <= h <= 11:
            return f'{h}:00 AM'
        elif h == 12:
            return '12:00 PM'
        else:
            return f'{h-12}:00 PM'
            
    df['hour_label'] = df['hour'].apply(hour_to_label)
    
    # 4. Pivot the table
    # We group by date_str and hour_label, aggregating the values.
    # Using 'mean' is safe for setpoints that might be repeated every 5 mins.
    pivot_df = df.pivot_table(
        index='date_str', 
        columns='hour_label', 
        values='zone_016_cooling_sp', 
        aggfunc='mean'
    )
    
    # 5. Define the exact target column order
    target_hours = [
        '1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', '6:00 AM', '7:00 AM', '8:00 AM', 
        '9:00 AM', '10:00 AM', '11:00 AM', '12:00 PM', '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', 
        '5:00 PM', '6:00 PM', '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM', '12:00 AM'
    ]
    
    # Reindex to ensure all columns exist and are in the correct order
    pivot_df = pivot_df.reindex(columns=target_hours)
    
    # Reset index to bring 'date_str' back as a column
    pivot_df = pivot_df.reset_index()
    
    # Rename 'date_str' to 'date' to match target schema
    pivot_df = pivot_df.rename(columns={'date_str': 'date'})
    
    # 6. Select and return the final columns
    target_columns = ['date'] + target_hours
    return pivot_df[target_columns]