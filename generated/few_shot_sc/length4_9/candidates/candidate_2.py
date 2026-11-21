import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse the date column
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'])
    
    # 2. Extract date part for grouping and formatting
    # Target date format is MM/DD/YYYY
    df['date_str'] = df['datetime'].dt.strftime('%m/%d/%Y')
    
    # 3. Extract hour (0-23)
    df['hour'] = df['datetime'].dt.hour
    
    # 4. Map hour (0-23) to target column names (12-hour format with AM/PM)
    def map_hour_to_col(h):
        if h == 0:
            return '12:00 AM'
        elif h < 12:
            return f'{h}:00 AM'
        elif h == 12:
            return '12:00 PM'
        else:
            return f'{h-12}:00 PM'
            
    df['hour_label'] = df['hour'].apply(map_hour_to_col)
    
    # 5. Group by date and hour_label, aggregate zone_016
    # We use mean to aggregate minute-level data to hour-level
    grouped = df.groupby(['date_str', 'hour_label'])['zone_016'].mean().unstack(fill_value=np.nan)
    
    # 6. Reset index to make date a column
    grouped = grouped.reset_index()
    
    # 7. Define target columns
    target_columns = [
        'date', '1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', '6:00 AM', 
        '7:00 AM', '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM', '12:00 PM', 
        '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', '6:00 PM', 
        '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM', '12:00 AM'
    ]
    
    # 8. Rename the date column
    grouped = grouped.rename(columns={'date_str': 'date'})
    
    # 9. Ensure all target columns exist (some hours might be missing if no data)
    # Fill missing columns with NaN
    for col in target_columns[1:]: # Skip 'date'
        if col not in grouped.columns:
            grouped[col] = np.nan
            
    # 10. Sort by date descending to match the sample order (01/02 before 01/01)
    # The sample shows 01/02 then 01/01.
    grouped = grouped.sort_values(by='date', ascending=False).reset_index(drop=True)
    
    # 11. Select and return target columns
    return grouped[target_columns]