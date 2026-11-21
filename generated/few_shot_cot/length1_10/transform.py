import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    df = source.copy()
    
    # 1. Parse datetime
    df['dt'] = pd.to_datetime(df['date'])
    
    # 2. Extract date key for grouping and hour for bucketing
    # Normalize to midnight for grouping by day
    df['date_key'] = df['dt'].dt.normalize()
    
    # Map pandas hour (0-23) to target hour labels (1-24)
    # Hour 0 (00:00-00:59) -> '1:00'
    # Hour 23 (23:00-23:59) -> '24:00'
    df['hour_label'] = df['dt'].dt.hour + 1
    df['hour_col'] = df['hour_label'].astype(str) + ':00'
    
    # 3. Aggregate
    # Based on sample analysis: 12 rows of 73 sum to 876. Aggregation is SUM.
    agg_df = df.groupby(['date_key', 'hour_col'])['zone_016_cooling_sp'].sum().reset_index()
    
    # 4. Pivot to wide format
    pivot_df = agg_df.pivot(index='date_key', columns='hour_col', values='zone_016_cooling_sp')
    
    # 5. Handle missing hours (fill with 0)
    pivot_df = pivot_df.fillna(0)
    
    # 6. Format date column 'cst'
    pivot_df['cst'] = pivot_df.index.strftime('%a %m/%d/%Y')
    
    # 7. Reset index and clean up
    pivot_df = pivot_df.reset_index(drop=True)
    pivot_df = pivot_df.rename_axis(None, axis=1)
    
    # 8. Define target columns
    target_cols = ['cst'] + [f'{i}:00' for i in range(1, 25)]
    
    # 9. Select and return
    return pivot_df[target_cols]