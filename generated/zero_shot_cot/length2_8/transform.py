import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # 1. Parse the date column
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract dt_strata (MM/DD/YY)
    df['dt_strata'] = df['datetime'].dt.strftime('%m/%d/%y')
    
    # 3. Extract dow (Monday=1, ..., Sunday=7)
    # pandas dayofweek: Monday=0, ..., Sunday=6
    df['dow'] = df['datetime'].dt.dayofweek + 1
    
    # 4. Extract hour for grouping
    df['hour'] = df['datetime'].dt.hour
    
    # 5. Aggregate: Sum cerc_logger_1 for each dt_strata and hour
    # We group by dt_strata and hour, then sum the values
    agg_df = df.groupby(['dt_strata', 'hour'])['cerc_logger_1'].sum().reset_index()
    
    # 6. Pivot the data so hours become columns
    # The index will be dt_strata, columns will be hour, values will be the sum
    pivot_df = agg_df.pivot_table(index='dt_strata', columns='hour', values='cerc_logger_1', fill_value=0)
    
    # 7. Rename columns to match target format: pct_hourly_0100, ..., pct_hourly_2400
    # Hour 0 -> pct_hourly_0100
    # Hour 1 -> pct_hourly_0200
    # ...
    # Hour 23 -> pct_hourly_2400
    new_columns = {}
    for h in range(24):
        col_name = f'pct_hourly_{h+1:02d}00'
        new_columns[h] = col_name
    
    pivot_df.rename(columns=new_columns, inplace=True)
    
    # 8. Ensure all 24 hour columns exist, even if no data for that hour
    expected_hour_cols = [f'pct_hourly_{h+1:02d}00' for h in range(24)]
    for col in expected_hour_cols:
        if col not in pivot_df.columns:
            pivot_df[col] = 0
            
    # 9. Add pct_hourly_2500 column with 0
    pivot_df['pct_hourly_2500'] = 0
    
    # 10. Reset index to make dt_strata a column
    pivot_df.reset_index(inplace=True)
    
    # 11. Merge dow back into the pivot_df
    # We need to get the dow for each dt_strata. Since dt_strata is unique per day, 
    # we can just take the first occurrence or map it.
    # Create a mapping from dt_strata to dow
    dow_map = df[['dt_strata', 'dow']].drop_duplicates().set_index('dt_strata')['dow']
    pivot_df['dow'] = pivot_df['dt_strata'].map(dow_map)
    
    # 12. Define target columns
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
    
    # 13. Select and order columns
    result_df = pivot_df[target_columns]
    
    # 14. Ensure correct dtypes
    result_df['dow'] = result_df['dow'].astype(int)
    result_df['pct_hourly_2500'] = result_df['pct_hourly_2500'].astype(int)
    
    # Convert hourly columns to float
    for col in target_columns[2:26]: # Exclude dt_strata, dow, and pct_hourly_2500
        result_df[col] = result_df[col].astype(float)
        
    return result_df