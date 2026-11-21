import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # 1. Parse datetime
    # Source format: '1/2/2018 0:11' -> %m/%d/%Y %H:%M
    source = source.copy()
    source['datetime'] = pd.to_datetime(source['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract date and hour
    source['date_obj'] = source['datetime'].dt.normalize() # Just the date
    source['hour'] = source['datetime'].dt.hour
    
    # 3. Map hour to target column name
    # 0 -> 12:00 AM
    # 1 -> 1:00 AM
    # ...
    # 11 -> 11:00 AM
    # 12 -> 12:00 PM
    # 13 -> 1:00 PM
    # ...
    # 23 -> 11:00 PM
    
    def map_hour_to_col(h):
        if h == 0:
            return '12:00 AM'
        elif h == 12:
            return '12:00 PM'
        elif h > 12:
            return f'{h - 12}:00 PM'
        else:
            return f'{h}:00 AM'
            
    source['time_slot'] = source['hour'].apply(map_hour_to_col)
    
    # 4. Aggregate
    # Group by date and time_slot, take mean of zone_016
    # Using mean handles NaNs appropriately (ignores them)
    grouped = source.groupby(['date_obj', 'time_slot'])['zone_016'].mean()
    
    # 5. Pivot
    # Unpivot so time_slots become columns
    pivoted = grouped.unstack(level='time_slot')
    
    # 6. Define target columns order
    target_columns = [
        '1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', '6:00 AM', 
        '7:00 AM', '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM', '12:00 PM', 
        '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', '6:00 PM', 
        '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM', '12:00 AM'
    ]
    
    # Ensure all target columns exist in the dataframe, filling missing with NaN
    pivoted = pivoted.reindex(columns=target_columns)
    
    # 7. Reset index and format date
    df = pivoted.reset_index()
    
    # Format date to '%m/%d/%Y'
    # date_obj is a Timestamp, convert to string
    df['date'] = df['date_obj'].dt.strftime('%m/%d/%Y')
    
    # Drop the temporary date_obj column if it exists (it's now in index or dropped)
    if 'date_obj' in df.columns:
        df = df.drop(columns=['date_obj'])
    
    # 8. Sort order
    # The sample shows 01/02/2018 then 01/01/2018 (Descending date)
    # Let's sort by date descending to match the sample pattern
    df = df.sort_values(by='date', ascending=False).reset_index(drop=True)
    
    # 9. Select final columns
    # The first column in target is 'date', followed by the time slots
    final_columns = ['date'] + target_columns
    
    # Ensure we only return the specified columns
    df = df[final_columns]
    
    return df