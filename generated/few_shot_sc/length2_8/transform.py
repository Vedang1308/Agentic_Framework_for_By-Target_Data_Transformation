import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms high-frequency (10-min) source data into daily hourly aggregated data.
    """
    df = source.copy()
    
    # 1. Parse the date column
    # Format is '%m/%d/%Y %H:%M' e.g., '7/28/2019 4:50'
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract features for grouping and target columns
    # dt_strata: formatted as '%m/%d/%y' (e.g., '01/14/19')
    df['dt_strata'] = df['datetime'].dt.strftime('%m/%d/%y')
    
    # dow: Day of week, Monday=1, Sunday=7
    # dt.weekday() returns Monday=0, Sunday=6. So we add 1.
    df['dow'] = df['datetime'].dt.weekday + 1
    
    # hour: 0-23
    df['hour'] = df['datetime'].dt.hour
    
    # 3. Aggregate to hourly averages
    # Group by date and hour, then take the mean of cerc_logger_1
    grouped = df.groupby(['dt_strata', 'hour'])['cerc_logger_1'].mean().reset_index()
    
    # 4. Pivot to wide format
    # Index: dt_strata, Columns: hour, Values: cerc_logger_1
    # Note: We need to keep 'dow' as well. Since 'dow' is constant for a given 'dt_strata',
    # we can group by 'dt_strata' for dow separately or merge it back.
    
    # Get dow per date
    dow_series = df.groupby('dt_strata')['dow'].first()
    
    # Pivot the hourly data
    pivot_df = grouped.pivot(index='dt_strata', columns='hour', values='cerc_logger_1')
    
    # Fill any missing hours with 0 (in case some hours have no data)
    pivot_df = pivot_df.fillna(0)
    
    # 5. Rename columns to match target schema
    # Source Hour 0 -> pct_hourly_0100
    # Source Hour 1 -> pct_hourly_0200
    # ...
    # Source Hour 23 -> pct_hourly_2400
    new_col_names = {}
    for h in range(24):
        new_col_names[h] = f'pct_hourly_{h+1:02d}00'
    
    pivot_df.rename(columns=new_col_names, inplace=True)
    
    # 6. Add dow column
    pivot_df['dow'] = dow_series
    
    # 7. Add pct_hourly_2500 column with 0
    pivot_df['pct_hourly_2500'] = 0
    
    # 8. Sort index if necessary (optional, but good for consistency)
    pivot_df = pivot_df.sort_index()
    
    # 9. Reset index to make dt_strata a column
    pivot_df = pivot_df.reset_index()
    
    # 10. Define target columns verbatim
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
    
    # Ensure dow is int
    pivot_df['dow'] = pivot_df['dow'].astype(int)
    
    # Select and return
    return pivot_df[target_columns]