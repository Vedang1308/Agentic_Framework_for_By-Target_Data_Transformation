import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse the date column
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'])
    
    # 2. Extract date string for target 'dt_strata' (format MM/DD/YY)
    df['dt_strata'] = df['datetime'].dt.strftime('%m/%d/%y')
    
    # 3. Calculate Day of Week (1=Monday, ..., 7=Sunday)
    df['dow'] = df['datetime'].dt.dayofweek + 1
    
    # 4. Extract hour for grouping
    df['hour'] = df['datetime'].dt.hour
    
    # 5. Aggregate zone_016 by date and hour
    # We sum the values for each hour within each day
    agg_df = df.groupby(['dt_strata', 'dow', 'hour'])['zone_016'].sum().reset_index()
    
    # 6. Map hours to target column names
    # Mapping: 
    # Hour 0 (00:00-00:59) -> pct_hourly_2400
    # Hour 1 (01:00-01:59) -> pct_hourly_0100
    # ...
    # Hour 23 (23:00-23:59) -> pct_hourly_2300
    def get_col_name(h):
        if h == 0:
            return 'pct_hourly_2400'
        else:
            return f'pct_hourly_{h:02d}00'
            
    agg_df['target_col'] = agg_df['hour'].apply(get_col_name)
    
    # 7. Pivot to wide format
    # Rows: dt_strata (dow is consistent per dt_strata)
    # Columns: target_col
    # Values: zone_016
    pivot_df = agg_df.pivot_table(index='dt_strata', columns='target_col', values='zone_016', fill_value=0)
    
    # 8. Reset index and restore dow
    pivot_df = pivot_df.reset_index()
    
    # Merge dow back in (since pivot dropped it, but it's unique per dt_strata)
    # We can just take the first dow for each dt_strata from the original grouped data or simply recalculate if needed.
    # Easier: Create a mapping from dt_strata to dow from the aggregated data
    dow_map = agg_df[['dt_strata', 'dow']].drop_duplicates().set_index('dt_strata')['dow']
    pivot_df['dow'] = pivot_df['dt_strata'].map(dow_map)
    
    # 9. Ensure all target columns exist and are in correct order
    target_hourly_cols = [f'pct_hourly_{i:02d}00' for i in range(1, 25)] + ['pct_hourly_2500']
    
    # Add pct_hourly_2500 as 0 if not present (it shouldn't be from pivot)
    if 'pct_hourly_2500' not in pivot_df.columns:
        pivot_df['pct_hourly_2500'] = 0
        
    # Select and order columns
    final_cols = ['dt_strata', 'dow'] + target_hourly_cols
    
    # Ensure all hourly columns are present, filling missing ones with 0
    for col in target_hourly_cols:
        if col not in pivot_df.columns:
            pivot_df[col] = 0
            
    result_df = pivot_df[final_cols]
    
    # Sort by dt_strata to match sample order (optional but good practice)
    result_df = result_df.sort_values('dt_strata').reset_index(drop=True)
    
    return result_df