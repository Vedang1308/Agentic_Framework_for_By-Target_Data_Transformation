import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    df = source.copy()
    
    # 1. Parse the date column
    df['dt'] = pd.to_datetime(df['date'])
    
    # 2. Extract date part and hour part
    df['date_only'] = df['dt'].dt.date
    df['hour'] = df['dt'].dt.hour
    
    # 3. Map hour to target column names
    # Hour 0 maps to '24:00', Hours 1-23 map to '1:00'-'23:00'
    def map_hour(h):
        if h == 0:
            return '24:00'
        else:
            return f'{h}:00'
            
    df['hour_label'] = df['hour'].apply(map_hour)
    
    # 4. Aggregate: Sum the values for each date and hour
    # The target values (876) correspond to 12 * 73, implying sum of 5-min intervals
    agg_df = df.groupby(['date_only', 'hour_label'])['zone_016_cooling_sp'].sum().reset_index()
    
    # 5. Pivot to wide format
    pivot_df = agg_df.pivot(index='date_only', columns='hour_label', values='zone_016_cooling_sp')
    
    # 6. Format the date index as 'cst'
    pivot_df.index = pd.to_datetime(pivot_df.index).strftime('%a %m/%d/%Y')
    pivot_df.index.name = 'cst'
    
    # 7. Reset index to make 'cst' a column
    pivot_df = pivot_df.reset_index()
    
    # 8. Define target columns in order
    target_columns = ['cst'] + [f'{i}:00' for i in range(1, 25)]
    
    # 9. Ensure all target columns exist (fill NaN with 0 if a day is missing an hour)
    for col in target_columns:
        if col not in pivot_df.columns:
            pivot_df[col] = 0
            
    # 10. Select and return
    return pivot_df[target_columns]