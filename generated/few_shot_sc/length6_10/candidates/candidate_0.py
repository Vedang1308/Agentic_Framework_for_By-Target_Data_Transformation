import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse datetime
    df['datetime'] = pd.to_datetime(df['date'])
    
    # 2. Extract date string for grouping and hour for pivoting
    # Target date format is %m/%d/%Y
    df['date_str'] = df['datetime'].dt.strftime('%m/%d/%Y')
    
    # Map hours: 0 (12 AM) -> 1, 1 (1 AM) -> 2, ..., 23 (11 PM) -> 24
    df['hour_idx'] = df['datetime'].dt.hour + 1
    
    # 3. Aggregate data per date and hour
    # Using mean as a standard aggregation for continuous values
    agg_df = df.groupby(['date_str', 'hour_idx'])['zone_016_cooling_sp'].mean().reset_index()
    
    # 4. Pivot to wide format
    pivot_df = agg_df.pivot(index='date_str', columns='hour_idx', values='zone_016_cooling_sp')
    
    # 5. Rename columns to 'Hr 1', 'Hr 2', ..., 'Hr 24'
    pivot_df.columns = [f'Hr {int(col)}' for col in pivot_df.columns]
    
    # 6. Ensure all 24 hour columns exist, filling missing ones with NaN
    target_hour_cols = [f'Hr {i}' for i in range(1, 25)]
    pivot_df = pivot_df.reindex(columns=target_hour_cols)
    
    # 7. Reset index to make 'date_str' a column named 'Date'
    pivot_df.index.name = 'Date'
    pivot_df = pivot_df.reset_index()
    
    # 8. Select and order columns verbatim
    target_columns = ['Date'] + target_hour_cols
    return pivot_df[target_columns]