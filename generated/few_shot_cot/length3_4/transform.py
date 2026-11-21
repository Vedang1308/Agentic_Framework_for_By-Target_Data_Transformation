import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the datetime column
    df['date_dt'] = pd.to_datetime(df['date'])
    
    # 2. Extract date string in target format '%m/%d/%Y'
    df['date'] = df['date_dt'].dt.strftime('%m/%d/%Y')
    
    # 3. Extract hour and map to 1-24 scale
    # Source hour 0 (00:00-00:59) -> Hour 1
    # Source hour 23 (23:00-23:59) -> Hour 24
    df['hour_num'] = df['date_dt'].dt.hour + 1
    df['hour_label'] = 'Hour ' + df['hour_num'].astype(str)
    
    # 4. Aggregate by date and hour
    # Using mean to handle multiple entries per hour. 
    # If values are constant, mean equals the value.
    agg_df = df.groupby(['date', 'hour_label'])['zone_016_cooling_sp'].mean().reset_index()
    
    # 5. Pivot to wide format
    pivot_df = agg_df.pivot(index='date', columns='hour_label', values='zone_016_cooling_sp')
    
    # 6. Ensure all Hour 1..24 columns exist
    target_hour_cols = [f'Hour {i}' for i in range(1, 25)]
    for col in target_hour_cols:
        if col not in pivot_df.columns:
            pivot_df[col] = pd.NA
            
    # 7. Reorder columns and reset index
    pivot_df = pivot_df[target_hour_cols]
    pivot_df = pivot_df.reset_index()
    
    # 8. Define final target columns
    target_columns = ['date'] + target_hour_cols
    
    return pivot_df[target_columns]