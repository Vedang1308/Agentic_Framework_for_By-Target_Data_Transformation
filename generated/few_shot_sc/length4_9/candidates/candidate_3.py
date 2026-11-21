import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    df = source.copy()
    
    # 1. Parse the date column
    # Source format: '1/2/2018 0:11' -> '%m/%d/%Y %H:%M'
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract date for grouping (YYYY-MM-DD is good for sorting/grouping)
    df['date_key'] = df['datetime'].dt.strftime('%Y-%m-%d')
    
    # 3. Extract hour and map to target column names
    hour_map = {
        0: '12:00 AM',
        1: '1:00 AM', 2: '2:00 AM', 3: '3:00 AM', 4: '4:00 AM', 5: '5:00 AM',
        6: '6:00 AM', 7: '7:00 AM', 8: '8:00 AM', 9: '9:00 AM', 10: '10:00 AM',
        11: '11:00 AM',
        12: '12:00 PM',
        13: '1:00 PM', 14: '2:00 PM', 15: '3:00 PM', 16: '4:00 PM', 17: '5:00 PM',
        18: '6:00 PM', 19: '7:00 PM', 20: '8:00 PM', 21: '9:00 PM', 22: '10:00 PM',
        23: '11:00 PM'
    }
    
    df['hour_label'] = df['datetime'].dt.hour.map(hour_map)
    
    # 4. Aggregate data
    # Group by date and hour label, taking the mean of zone_016
    # Using mean handles NaNs appropriately (ignores them) and averages multiple entries
    aggregated = df.groupby(['date_key', 'hour_label'])['zone_016'].mean().reset_index()
    
    # 5. Pivot the table
    # Index: date_key, Columns: hour_label, Values: zone_016
    pivoted = aggregated.pivot(index='date_key', columns='hour_label', values='zone_016')
    
    # 6. Reset index to make date_key a column
    pivoted = pivoted.reset_index()
    
    # 7. Format the date column to MM/DD/YYYY
    pivoted['date'] = pd.to_datetime(pivoted['date_key'], format='%Y-%m-%d').dt.strftime('%m/%d/%Y')
    
    # 8. Define the exact target columns order
    target_columns = [
        'date', 
        '1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', '6:00 AM', '7:00 AM', 
        '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM', '12:00 PM', '1:00 PM', '2:00 PM', 
        '3:00 PM', '4:00 PM', '5:00 PM', '6:00 PM', '7:00 PM', '8:00 PM', '9:00 PM', 
        '10:00 PM', '11:00 PM', '12:00 AM'
    ]
    
    # 9. Ensure all target columns exist (fill missing with NaN if necessary)
    for col in target_columns:
        if col not in pivoted.columns and col != 'date':
            pivoted[col] = np.nan
            
    # 10. Select and order columns
    result = pivoted[target_columns]
    
    return result