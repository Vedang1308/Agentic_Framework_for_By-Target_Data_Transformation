import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame with minute-level data into a target DataFrame
    with hourly aggregated data pivoted by time of day.
    """
    # 1. Parse the date column
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract date and hour
    df['date_only'] = df['datetime'].dt.date
    df['hour'] = df['datetime'].dt.hour
    
    # 3. Map hour to target column names (12-hour format)
    def hour_to_label(h):
        if h == 0:
            return '12:00 AM'
        elif h < 12:
            return f'{h}:00 AM'
        elif h == 12:
            return '12:00 PM'
        else:
            return f'{h-12}:00 PM'
            
    df['time_slot'] = df['hour'].apply(hour_to_label)
    
    # 4. Aggregate by date and time slot
    # We use mean() to aggregate minute-level data to hourly. 
    # If values are constant per hour, mean() returns that value.
    # If there are NaNs, mean() ignores them.
    grouped = df.groupby(['date_only', 'time_slot'])['zone_016'].mean()
    
    # 5. Pivot the data
    # The index will be date_only, columns will be time_slot, values will be zone_016
    pivoted = grouped.unstack(fill_value=np.nan)
    
    # 6. Format the date index to match target format '%m/%d/%Y'
    pivoted.index = pivoted.index.strftime('%m/%d/%Y')
    
    # 7. Reset index to make 'date' a column
    pivoted = pivoted.reset_index()
    pivoted.rename(columns={'index': 'date'}, inplace=True)
    
    # 8. Define the exact target column order
    target_columns = [
        'date', 
        '1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', '6:00 AM', 
        '7:00 AM', '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM', '12:00 PM', 
        '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', '6:00 PM', 
        '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM', '12:00 AM'
    ]
    
    # 9. Ensure all target columns exist (fill missing with NaN if necessary)
    for col in target_columns:
        if col not in pivoted.columns:
            pivoted[col] = np.nan
            
    # 10. Select and order columns
    result = pivoted[target_columns]
    
    return result