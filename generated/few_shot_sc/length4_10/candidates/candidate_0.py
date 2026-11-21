import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the date column
    df['datetime'] = pd.to_datetime(df['date'])
    
    # 2. Extract date and hour for grouping
    df['dt_date'] = df['datetime'].dt.date
    df['dt_hour'] = df['datetime'].dt.hour
    
    # 3. Aggregate by date and hour
    # Using mean to handle potential minor variations or multiple entries per hour
    # If values are constant, mean == first == last
    agg_df = df.groupby(['dt_date', 'dt_hour'])['zone_016_cooling_sp'].mean().reset_index()
    
    # 4. Pivot/Unstack to get hours as columns
    pivoted = agg_df.pivot_table(index='dt_date', columns='dt_hour', values='zone_016_cooling_sp')
    
    # 5. Define mapping from 24-hour hour (0-23) to target column names
    hour_map = {}
    for h in range(24):
        if h == 0:
            hour_map[h] = '12:00 AM'
        elif h < 12:
            hour_map[h] = f'{h}:00 AM'
        elif h == 12:
            hour_map[h] = '12:00 PM'
        else:
            hour_map[h] = f'{h-12}:00 PM'
            
    # 6. Rename columns
    pivoted.rename(columns=hour_map, inplace=True)
    
    # 7. Reset index to make date a column
    pivoted.reset_index(inplace=True)
    
    # 8. Format the date column as MM/DD/YYYY
    pivoted['date'] = pd.to_datetime(pivoted['dt_date']).dt.strftime('%m/%d/%Y')
    
    # 9. Define target columns in the exact required order
    target_columns = [
        'date', '1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', '6:00 AM', 
        '7:00 AM', '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM', '12:00 PM', 
        '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', '6:00 PM', 
        '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM', '12:00 AM'
    ]
    
    # 10. Select and return columns in the correct order
    return pivoted[target_columns]