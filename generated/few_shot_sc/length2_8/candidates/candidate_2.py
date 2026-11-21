import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms source DataFrame with minute-level sensor data into a daily hourly summary.
    """
    df = source.copy()
    
    # 1. Parse the date column
    # Format is '%m/%d/%Y %H:%M'
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract components for grouping and target columns
    # dt_strata: '%m/%d/%y'
    df['dt_strata'] = df['datetime'].dt.strftime('%m/%d/%y')
    # dow: 1=Monday, ..., 7=Sunday
    df['dow'] = df['datetime'].dt.dayofweek + 1
    # hour: 0-23
    df['hour'] = df['datetime'].dt.hour
    
    # 3. Aggregate data by day and hour
    # Calculate the mean of cerc_logger_1 for each day and hour
    agg_df = df.groupby(['dt_strata', 'hour'])['cerc_logger_1'].mean().reset_index()
    
    # 4. Pivot the data to have hours as columns
    pivot_df = agg_df.pivot(index='dt_strata', columns='hour', values='cerc_logger_1')
    
    # 5. Clean up pivot dataframe
    pivot_df.reset_index(inplace=True)
    
    # 6. Rename hour columns to match target schema
    # Hour 0 -> pct_hourly_0100, ..., Hour 23 -> pct_hourly_2400
    rename_dict = {h: f'pct_hourly_{h+1:02d}00' for h in range(24)}
    pivot_df.rename(columns=rename_dict, inplace=True)
    
    # 7. Fill missing values with 0 (if an hour is missing for a day)
    # Select only the hourly columns to fill, avoiding dt_strata
    hourly_cols = [f'pct_hourly_{i:02d}00' for i in range(1, 25)]
    pivot_df[hourly_cols] = pivot_df[hourly_cols].fillna(0)
    
    # 8. Add the constant column pct_hourly_2500 = 0
    pivot_df['pct_hourly_2500'] = 0
    
    # 9. Add dow column
    # We need to map dt_strata to dow. We can create a mapping from the original df
    dow_map = df.drop_duplicates(subset=['dt_strata'])[['dt_strata', 'dow']]
    pivot_df = pivot_df.merge(dow_map, on='dt_strata', how='left')
    
    # 10. Ensure correct column order and types
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
    
    # Ensure dow is integer
    pivot_df['dow'] = pivot_df['dow'].astype(int)
    
    # Select and return
    return pivot_df[target_columns]