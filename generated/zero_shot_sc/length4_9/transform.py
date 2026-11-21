import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms source DataFrame with 'date' and 'zone_016' into a wide format
    with daily averages for each hour of the day.
    """
    
    # 1. Parse the date column
    source = source.copy()
    source['dt'] = pd.to_datetime(source['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract date and hour components
    source['date_only'] = source['dt'].dt.date
    source['hour'] = source['dt'].dt.hour
    
    # 3. Define the mapping from hour integer to target column name
    hour_to_col = {
        0: '12:00 AM', 1: '1:00 AM', 2: '2:00 AM', 3: '3:00 AM', 
        4: '4:00 AM', 5: '5:00 AM', 6: '6:00 AM', 7: '7:00 AM', 
        8: '8:00 AM', 9: '9:00 AM', 10: '10:00 AM', 11: '11:00 AM', 
        12: '12:00 PM', 13: '1:00 PM', 14: '2:00 PM', 15: '3:00 PM', 
        16: '4:00 PM', 17: '5:00 PM', 18: '6:00 PM', 19: '7:00 PM', 
        20: '8:00 PM', 21: '9:00 PM', 22: '10:00 PM', 23: '11:00 PM'
    }
    
    # 4. Aggregate: Group by date and hour, calculate mean of zone_016
    # Using mean is standard for sensor data aggregation over time bins.
    agg_df = source.groupby(['date_only', 'hour'])['zone_016'].mean().reset_index()
    
    # 5. Pivot the data to wide format
    # Index: date_only, Columns: hour, Values: zone_016
    pivot_df = agg_df.pivot(index='date_only', columns='hour', values='zone_016')
    
    # 6. Rename columns using the mapping
    pivot_df.rename(columns=hour_to_col, inplace=True)
    
    # 7. Reset index to make date a column
    pivot_df.reset_index(inplace=True)
    
    # 8. Format the date column to %m/%d/%Y
    pivot_df['date'] = pivot_df['date_only'].apply(lambda x: x.strftime('%m/%d/%Y'))
    
    # 9. Define the exact target columns order
    target_columns = [
        'date', '1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', 
        '6:00 AM', '7:00 AM', '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM', 
        '12:00 PM', '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', 
        '6:00 PM', '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM', 
        '12:00 AM'
    ]
    
    # 10. Ensure all target columns exist (fill missing hours with NaN)
    for col in target_columns:
        if col != 'date' and col not in pivot_df.columns:
            pivot_df[col] = np.nan
            
    # 11. Select and order columns
    result_df = pivot_df[target_columns]
    
    # 12. Sort by date for consistency (optional but good practice)
    result_df = result_df.sort_values('date').reset_index(drop=True)
    
    return result_df