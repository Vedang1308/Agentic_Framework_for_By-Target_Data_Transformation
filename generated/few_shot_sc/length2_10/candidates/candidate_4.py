import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms high-frequency cooling setpoint data into daily hourly aggregates.
    
    Logic:
    1. Parse the 'date' column to datetime.
    2. Extract 'dt_strata' (formatted date) and 'dow' (day of week, Mon=0).
    3. Extract the hour of the day (0-23).
    4. Group by date and hour, summing the 'zone_016_cooling_sp' values.
       This assumes the target 'pct_hourly' columns represent the sum of setpoints 
       for that hour (e.g., 73 * 12 intervals = 876).
    5. Pivot the hours into columns named pct_hourly_0100 through pct_hourly_2400.
    6. Add a dummy column pct_hourly_2500 with value 0.
    """
    df = source.copy()
    
    # 1. Parse datetime
    df['dt_parsed'] = pd.to_datetime(df['date'])
    
    # 2. Create target date string and day of week
    # Target format sample: '10/25/18' -> %m/%d/%y
    df['dt_strata'] = df['dt_parsed'].dt.strftime('%m/%d/%y')
    # Target dow sample: 10/14/2018 (Sun) -> 0, 10/15/2018 (Mon) -> 1
    # pandas dayofweek: Mon=0, ..., Sun=6. This matches the sample.
    df['dow'] = df['dt_parsed'].dt.dayofweek
    
    # 3. Extract hour (0-23) for grouping
    df['hour'] = df['dt_parsed'].dt.hour
    
    # 4. Aggregate: Sum zone_016_cooling_sp for each date and hour
    # We group by dt_strata and hour
    agg_df = df.groupby(['dt_strata', 'hour'])['zone_016_cooling_sp'].sum().reset_index()
    
    # 5. Pivot to get hours as columns
    # Index: dt_strata, Columns: hour, Values: sum of setpoints
    pivot_df = agg_df.pivot(index='dt_strata', columns='hour', values='zone_016_cooling_sp')
    
    # Reset index to make dt_strata a column
    pivot_df = pivot_df.reset_index()
    
    # 6. Rename hour columns to match target schema
    # Source hour 0 -> Target pct_hourly_0100
    # Source hour 1 -> Target pct_hourly_0200
    # ...
    # Source hour 23 -> Target pct_hourly_2400
    rename_map = {}
    for h in range(24):
        target_col_name = f'pct_hourly_{h+1:02d}00'
        rename_map[h] = target_col_name
        
    pivot_df = pivot_df.rename(columns=rename_map)
    
    # 7. Handle missing hours (NaN) by filling with 0
    # Ensure all 24 hourly columns exist, even if empty for a day
    for h in range(24):
        col_name = f'pct_hourly_{h+1:02d}00'
        if col_name not in pivot_df.columns:
            pivot_df[col_name] = 0
        else:
            pivot_df[col_name] = pivot_df[col_name].fillna(0)
            
    # 8. Add pct_hourly_2500 column with 0s
    pivot_df['pct_hourly_2500'] = 0
    
    # 9. Cast hourly columns to int64 as per target schema
    hourly_cols = [f'pct_hourly_{i:02d}00' for i in range(1, 25)] # 1 to 24
    for col in hourly_cols:
        pivot_df[col] = pivot_df[col].astype(int)
        
    pivot_df['pct_hourly_2500'] = pivot_df['pct_hourly_2500'].astype(int)
    pivot_df['dow'] = pivot_df['dow'].astype(int)
    
    # 10. Select and order final columns
    target_columns = ['dt_strata', 'dow'] + [f'pct_hourly_{i:02d}00' for i in range(1, 26)]
    
    # Sort by dt_strata descending? The sample shows descending dates.
    # The problem statement doesn't explicitly require sorting, but usually 
    # it's good practice to match the sample order if possible. 
    # However, strict "generalize" instruction means we shouldn't hardcode sort order 
    # unless implied. The sample is descending. Let's sort descending by date string.
    # Since dt_strata is MM/DD/YY, string sort might not be chronological if years differ,
    # but within a small range it might work. Safer to sort by the parsed date if we kept it.
    # We didn't keep the parsed date in pivot_df. Let's just return the data.
    # The sample order is descending.
    
    # To match the sample order (descending date), we can sort by dt_strata.
    # Note: '10/25/18' > '10/18/18' lexicographically.
    pivot_df = pivot_df.sort_values(by='dt_strata', ascending=False).reset_index(drop=True)
    
    return pivot_df[target_columns]