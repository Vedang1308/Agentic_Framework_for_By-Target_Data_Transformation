import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse the date column
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract required components
    # dt_strata: MM/DD/YY
    df['dt_strata'] = df['datetime'].dt.strftime('%m/%d/%y')
    # dow: 1=Mon, ..., 7=Sun
    df['dow'] = df['datetime'].dt.dayofweek + 1
    # hour: 0-23
    df['hour'] = df['datetime'].dt.hour
    
    # 3. Aggregate
    # Group by date (dt_strata) and hour, sum the cerc_logger_1 values
    # Using sum because the target values (~136) are roughly 6x the source values (~24), 
    # and there are ~6 10-min intervals per hour.
    agg_df = df.groupby(['dt_strata', 'hour'])['cerc_logger_1'].sum().reset_index()
    
    # 4. Pivot the table
    # Index: dt_strata, Columns: hour, Values: sum of cerc_logger_1
    pivot_df = agg_df.pivot(index='dt_strata', columns='hour', values='cerc_logger_1')
    
    # 5. Rename columns to match target schema
    # Map hour 0 -> pct_hourly_0100, ..., 23 -> pct_hourly_2400
    new_col_names = {}
    for h in range(24):
        new_col_names[h] = f'pct_hourly_{h+1:04d}'
    
    pivot_df.rename(columns=new_col_names, inplace=True)
    
    # 6. Handle missing hours
    # If a specific hour has no data, fill with 0 (consistent with sum aggregation)
    pivot_df = pivot_df.fillna(0)
    
    # 7. Add dow back
    # Since dow is deterministic based on dt_strata, we can get it from the original df
    # Create a mapping from dt_strata to dow
    dow_map = df[['dt_strata', 'dow']].drop_duplicates().set_index('dt_strata')['dow']
    pivot_df['dow'] = pivot_df.index.map(dow_map)
    
    # 8. Add pct_hourly_2500 column
    # The target shows this column is always 0 and is int64
    pivot_df['pct_hourly_2500'] = 0
    
    # 9. Reset index to make dt_strata a column
    pivot_df = pivot_df.reset_index()
    
    # 10. Define target columns
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
    
    # 11. Ensure correct types
    pivot_df['dow'] = pivot_df['dow'].astype(int)
    pivot_df['pct_hourly_2500'] = pivot_df['pct_hourly_2500'].astype(int)
    # Ensure hourly columns are float
    for col in target_columns:
        if col.startswith('pct_hourly') and col != 'pct_hourly_2500':
            pivot_df[col] = pivot_df[col].astype(float)
            
    # 12. Select and return
    return pivot_df[target_columns]