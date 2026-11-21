import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse the date column
    df = source.copy()
    df['dt'] = pd.to_datetime(df['date'])
    
    # 2. Extract date string for grouping and final output
    df['date_only'] = df['dt'].dt.strftime('%m/%d/%Y')
    
    # 3. Extract hour and map to 1-24 scale
    # 0 -> 24, 1 -> 1, ..., 23 -> 23
    df['hour_num'] = df['dt'].dt.hour
    df['hour_col'] = df['hour_num'].apply(lambda h: 24 if h == 0 else h)
    
    # 4. Group by date and hour, and aggregate the value
    # Using mean to handle potential multiple entries per hour (e.g., 5-min intervals)
    # If an hour is missing, it will not appear in the groupby result, leading to NaN after unstack
    agg_df = df.groupby(['date_only', 'hour_col'])['zone_016_cooling_sp'].mean().reset_index()
    
    # 5. Pivot the table to have hours as columns
    pivot_df = agg_df.pivot(index='date_only', columns='hour_col', values='zone_016_cooling_sp')
    
    # 6. Rename columns to 'Hour 1', 'Hour 2', ..., 'Hour 24'
    pivot_df.columns = [f'Hour {int(col)}' for col in pivot_df.columns]
    
    # 7. Reset index to make date a column
    pivot_df = pivot_df.reset_index()
    pivot_df = pivot_df.rename(columns={'date_only': 'date'})
    
    # 8. Ensure all hour columns 1-24 are present, even if empty (NaN)
    target_hour_cols = [f'Hour {i}' for i in range(1, 25)]
    for col in target_hour_cols:
        if col not in pivot_df.columns:
            pivot_df[col] = float('nan')
            
    # 9. Select and order columns verbatim
    target_columns = ['date'] + target_hour_cols
    return pivot_df[target_columns]