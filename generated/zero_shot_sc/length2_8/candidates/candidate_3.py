import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse datetime
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract features
    df['hour'] = df['datetime'].dt.hour
    # Day of week: 1=Mon, ..., 7=Sun
    df['dow'] = df['datetime'].dt.dayofweek + 1
    # Date strata format MM/DD/YY
    df['dt_strata'] = df['datetime'].dt.strftime('%m/%d/%y')
    
    # 3. Aggregate by date and hour
    # Sum the logger values for each hour of each day
    agg_df = df.groupby(['dt_strata', 'hour'])['cerc_logger_1'].sum().reset_index()
    
    # 4. Pivot to get hours as columns
    pivoted = agg_df.pivot(index='dt_strata', columns='hour', values='cerc_logger_1')
    
    # 5. Rename columns to match target schema
    # Hour 0 -> pct_hourly_0100, Hour 1 -> pct_hourly_0200, ..., Hour 23 -> pct_hourly_2400
    new_cols = {}
    for h in range(24):
        new_cols[h] = f'pct_hourly_{h+1:04d}00'
    
    pivoted = pivoted.rename(columns=new_cols)
    
    # Add the 25th column which is always 0
    pivoted['pct_hourly_2500'] = 0
    
    # 6. Merge DOW back
    # Get DOW for each date strata
    dow_df = df.groupby('dt_strata')['dow'].first().reset_index()
    pivoted = pivoted.join(dow_df.set_index('dt_strata')['dow'])
    
    # 7. Reset index to make dt_strata a column
    pivoted = pivoted.reset_index()
    
    # 8. Define target columns
    target_columns = [
        'dt_strata', 'dow',
        'pct_hourly_0100', 'pct_hourly_0200', 'pct_hourly_0300', 'pct_hourly_0400',
        'pct_hourly_0500', 'pct_hourly_0600', 'pct_hourly_0700', 'pct_hourly_0800',
        'pct_hourly_0900', 'pct_hourly_1000', 'pct_hourly_1100', 'pct_hourly_1200',
        'pct_hourly_1300', 'pct_hourly_1400', 'pct_hourly_1500', 'pct_hourly_1600',
        'pct_hourly_1700', 'pct_hourly_1800', 'pct_hourly_1900', 'pct_hourly_2000',
        'pct_hourly_2100', 'pct_hourly_2200', 'pct_hourly_2300', 'pct_hourly_2400',
        'pct_hourly_2500'
    ]
    
    # Ensure all columns exist (some hours might be missing if data is sparse, fill with 0)
    for col in target_columns[2:]: # Skip dt_strata and dow
        if col not in pivoted.columns:
            pivoted[col] = 0
            
    # Sort by dt_strata to ensure deterministic order (optional but good practice)
    pivoted = pivoted.sort_values('dt_strata').reset_index(drop=True)
    
    return pivoted[target_columns]