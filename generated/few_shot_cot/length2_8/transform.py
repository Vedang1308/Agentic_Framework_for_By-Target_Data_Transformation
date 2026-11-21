import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    df = source.copy()
    
    # 1. Parse date
    df['datetime'] = pd.to_datetime(df['date'])
    
    # 2. Extract date string for dt_strata (MM/DD/YY)
    df['dt_strata'] = df['datetime'].dt.strftime('%m/%d/%y')
    
    # 3. Extract Day of Week (1=Mon, ..., 7=Sun)
    df['dow'] = df['datetime'].dt.dayofweek + 1
    
    # 4. Extract Hour Bucket (1-24)
    # Hour 0 (00:00-00:59) -> 1
    # Hour 23 (23:00-23:59) -> 24
    df['hour_bucket'] = df['datetime'].dt.hour + 1
    
    # 5. Aggregate: Sum cerc_logger_1 for each date and hour
    # We group by dt_strata and hour_bucket
    agg_df = df.groupby(['dt_strata', 'hour_bucket'])['cerc_logger_1'].sum().reset_index()
    
    # 6. Pivot to wide format
    # Index: dt_strata, Columns: hour_bucket, Values: cerc_logger_1
    pivot_df = agg_df.pivot(index='dt_strata', columns='hour_bucket', values='cerc_logger_1')
    
    # 7. Rename columns to match target schema
    # Ensure all hours 1-24 are present, fill missing with 0
    all_hours = range(1, 25)
    pivot_df = pivot_df.reindex(columns=all_hours, fill_value=0)
    
    # Rename columns: 1 -> pct_hourly_0100, etc.
    rename_dict = {h: f'pct_hourly_{h:02d}00' for h in all_hours}
    pivot_df = pivot_df.rename(columns=rename_dict)
    
    # 8. Add pct_hourly_2500 column with 0
    pivot_df['pct_hourly_2500'] = 0
    
    # 9. Reset index to make dt_strata a column
    pivot_df = pivot_df.reset_index()
    
    # 10. Merge dow back? 
    # The pivot_df only has dt_strata. We need dow.
    # Since dt_strata is unique per day, we can get dow from the original df or calculate it from dt_strata.
    # It's safer to calculate dow from dt_strata to ensure alignment.
    # Parse dt_strata back to datetime to get dow
    pivot_df['dow'] = pd.to_datetime(pivot_df['dt_strata'], format='%m/%d/%y').dt.dayofweek + 1
    
    # 11. Define target columns
    target_columns = ['dt_strata', 'dow'] + [f'pct_hourly_{i:02d}00' for i in range(1, 26)]
    
    # 12. Return final dataframe
    return pivot_df[target_columns]