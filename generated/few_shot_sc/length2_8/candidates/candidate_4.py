import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the date column
    # Format in source is '%m/%d/%Y %H:%M' e.g., '7/28/2019 4:50'
    df['datetime'] = pd.to_datetime(df['date'])
    
    # 2. Extract components for grouping and target columns
    # dt_strata format is '%m/%d/%y' (2-digit year) based on sample '01/14/19'
    df['dt_strata'] = df['datetime'].dt.strftime('%m/%d/%y')
    
    # dow: Monday=1, Sunday=7. pandas dayofweek: Monday=0...Sunday=6
    df['dow'] = df['datetime'].dt.dayofweek + 1
    
    # Extract hour (0-23) for bucketing
    df['hour'] = df['datetime'].dt.hour
    
    # 3. Aggregate cerc_logger_1 by date and hour
    # We group by the original date string (or datetime) and hour, then take mean
    # Using 'dt_strata' and 'hour' might be safer if multiple dates map to same string, 
    # but dt_strata is unique per day here. Let's group by 'dt_strata' and 'hour'.
    # Note: 'dt_strata' is derived from datetime, so it's consistent.
    
    agg_df = df.groupby(['dt_strata', 'hour'])['cerc_logger_1'].mean().reset_index()
    
    # 4. Pivot the aggregated data to wide format
    # Index: dt_strata, Columns: hour (0-23), Values: mean of cerc_logger_1
    pivot_df = agg_df.pivot(index='dt_strata', columns='hour', values='cerc_logger_1')
    
    # 5. Rename columns to match target schema: pct_hourly_0100 ... pct_hourly_2400
    # Hour 0 (midnight) -> pct_hourly_0100
    # Hour 23 (11pm) -> pct_hourly_2400
    rename_map = {h: f'pct_hourly_{h+1:02d}00' for h in range(24)}
    pivot_df = pivot_df.rename(columns=rename_map)
    
    # 6. Add pct_hourly_2500 column filled with 0
    pivot_df['pct_hourly_2500'] = 0
    
    # 7. Reset index to make dt_strata a column
    pivot_df = pivot_df.reset_index()
    
    # 8. Merge with dow
    # We need to get dow for each dt_strata. 
    # Since dt_strata is unique per day, we can merge on dt_strata.
    # First, create a unique mapping from dt_strata to dow from the original df
    dow_map = df[['dt_strata', 'dow']].drop_duplicates()
    
    result_df = pivot_df.merge(dow_map, on='dt_strata', how='left')
    
    # 9. Define target columns in exact order
    target_cols = ['dt_strata', 'dow'] + [f'pct_hourly_{i:02d}00' for i in range(1, 25)]
    
    # 10. Select and return
    return result_df[target_cols]