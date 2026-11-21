import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame from long format (datetime, value) 
    to wide format (date, 24 hourly columns).
    """
    # 1. Parse the date column
    df = source.copy()
    df['parsed_date'] = pd.to_datetime(df['date'])
    
    # 2. Extract date string and hour
    df['date_only'] = df['parsed_date'].dt.strftime('%m/%d/%Y')
    df['hour_int'] = df['parsed_date'].dt.hour
    
    # 3. Map hour integers to the specific target column names
    hour_map = {
        0: '12:00 AM', 1: '1:00 AM', 2: '2:00 AM', 3: '3:00 AM',
        4: '4:00 AM', 5: '5:00 AM', 6: '6:00 AM', 7: '7:00 AM',
        8: '8:00 AM', 9: '9:00 AM', 10: '10:00 AM', 11: '11:00 AM',
        12: '12:00 PM', 13: '1:00 PM', 14: '2:00 PM', 15: '3:00 PM',
        16: '4:00 PM', 17: '5:00 PM', 18: '6:00 PM', 19: '7:00 PM',
        20: '8:00 PM', 21: '9:00 PM', 22: '10:00 PM', 23: '11:00 PM'
    }
    
    df['hour_label'] = df['hour_int'].map(hour_map)
    
    # 4. Aggregate and Pivot
    # Group by date and hour_label, then aggregate the value.
    # Using mean() to handle multiple rows per hour (e.g., 5-min intervals).
    # If a day/hour combination has no data, it will remain NaN in the pivot.
    pivot_df = df.groupby(['date_only', 'hour_label'])['zone_016_cooling_sp'].mean().unstack(fill_value=np.nan)
    
    # 5. Reset index to make 'date_only' a column
    pivot_df = pivot_df.reset_index()
    pivot_df = pivot_df.rename(columns={'date_only': 'date'})
    
    # 6. Define the exact target column order
    target_columns = [
        'date', '1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', '6:00 AM', 
        '7:00 AM', '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM', '12:00 PM', 
        '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', '6:00 PM', 
        '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM', '12:00 AM'
    ]
    
    # 7. Ensure all target columns exist (some might be missing if no data for those hours)
    # and reorder them.
    for col in target_columns:
        if col not in pivot_df.columns:
            pivot_df[col] = np.nan
            
    return pivot_df[target_columns]