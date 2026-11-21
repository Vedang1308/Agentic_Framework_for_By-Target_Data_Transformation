import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse the date column
    df = source.copy()
    df['dt'] = pd.to_datetime(df['date'])
    
    # 2. Extract date, hour, and day of week
    df['date_only'] = df['dt'].dt.date
    df['hour'] = df['dt'].dt.hour
    df['dow'] = df['dt'].dt.dayofweek + 1  # Monday=1, Sunday=7
    
    # 3. Map hour to target column name
    # Based on analysis: Hour 0 -> pct_hourly_2400, Hour 1 -> pct_hourly_0100, ..., Hour 23 -> pct_hourly_2300
    def map_hour_to_col(h):
        if h == 0:
            return 'pct_hourly_2400'
        else:
            return f'pct_hourly_{h:02d}00'
            
    df['target_col'] = df['hour'].apply(map_hour_to_col)
    
    # 4. Aggregate values by date and target column
    # We sum the zone_016 values for each hour bucket
    agg_df = df.groupby(['date_only', 'target_col'])['zone_016'].sum().reset_index()
    
    # 5. Pivot to wide format
    # Index: date_only, Columns: target_col, Values: zone_016
    pivot_df = agg_df.pivot(index='date_only', columns='target_col', values='zone_016')
    
    # 6. Ensure all hourly columns exist and fill missing with 0
    all_hour_cols = [f'pct_hourly_{i:02d}00' for i in range(1, 24)] + ['pct_hourly_2400']
    for col in all_hour_cols:
        if col not in pivot_df.columns:
            pivot_df[col] = 0
            
    pivot_df = pivot_df.fillna(0)
    
    # 7. Format date to dt_strata
    pivot_df = pivot_df.reset_index()
    pivot_df['dt_strata'] = pd.to_datetime(pivot_df['date_only']).dt.strftime('%m/%d/%y')
    
    # 8. Get dow for each date
    # Since we grouped by date, we need to map the dow back. 
    # We can get the dow from the original df grouped by date_only
    dow_map = df.groupby('date_only')['dow'].first()
    pivot_df['dow'] = pivot_df['date_only'].map(dow_map)
    
    # 9. Add pct_hourly_2500 column
    pivot_df['pct_hourly_2500'] = 0
    
    # 10. Select and order columns
    target_cols = ['dt_strata', 'dow'] + all_hour_cols + ['pct_hourly_2500']
    
    # Sort by dt_strata to match typical output order (though not strictly required unless specified)
    # The sample shows 01/02/18 then 01/01/18. Let's just return as is or sort? 
    # Usually, deterministic order is preferred. Let's sort by date descending or ascending? 
    # The sample output has 01/02/18 first, then 01/01/18. This is descending date.
    pivot_df = pivot_df.sort_values('date_only', ascending=False)
    
    # Final selection
    result_df = pivot_df[target_cols]
    
    # Ensure correct dtypes for dow and pct_hourly_2500
    result_df['dow'] = result_df['dow'].astype(int)
    result_df['pct_hourly_2500'] = result_df['pct_hourly_2500'].astype(int)
    
    # Convert hourly columns to float
    for col in all_hour_cols:
        result_df[col] = result_df[col].astype(float)
        
    return result_df