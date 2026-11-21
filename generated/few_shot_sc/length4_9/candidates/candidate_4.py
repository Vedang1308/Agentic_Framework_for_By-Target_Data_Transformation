import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse datetime
    df['dt'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract date string in target format
    df['date_str'] = df['dt'].dt.strftime('%m/%d/%Y')
    
    # 3. Extract hour and map to target column names
    hour = df['dt'].dt.hour
    
    def map_hour_to_label(h):
        if h == 0:
            return '12:00 AM'
        elif h < 12:
            return f'{h}:00 AM'
        elif h == 12:
            return '12:00 PM'
        else:
            return f'{h - 12}:00 PM'
            
    df['hour_label'] = hour.apply(map_hour_to_label)
    
    # 4. Aggregate
    # We group by date and hour label, then take the mean of zone_016
    # Using mean handles multiple minutes per hour. 
    # If an hour has no data, it won't appear in the groupby result.
    agg_df = df.groupby(['date_str', 'hour_label'])['zone_016'].mean().reset_index()
    
    # 5. Pivot to wide format
    # Rows: date_str, Columns: hour_label, Values: zone_016
    pivot_df = agg_df.pivot(index='date_str', columns='hour_label', values='zone_016')
    
    # 6. Define target columns in specific order
    target_cols = [
        '1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', '6:00 AM', 
        '7:00 AM', '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM', '12:00 PM', 
        '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', '6:00 PM', 
        '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM', '12:00 AM'
    ]
    
    # 7. Ensure all target columns exist (fill missing with NaN)
    for col in target_cols:
        if col not in pivot_df.columns:
            pivot_df[col] = np.nan
            
    # 8. Reset index to make date a column
    pivot_df = pivot_df.reset_index()
    pivot_df.rename(columns={'date_str': 'date'}, inplace=True)
    
    # 9. Select and return columns in exact target order
    # The target schema lists 'date' first, then the hours.
    final_cols = ['date'] + target_cols
    
    # Reorder columns to match target schema exactly
    result_df = pivot_df[final_cols]
    
    return result_df