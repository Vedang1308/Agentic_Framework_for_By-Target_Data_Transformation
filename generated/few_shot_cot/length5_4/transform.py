import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the date column to datetime
    df['datetime'] = pd.to_datetime(df['date'])
    
    # 2. Extract the date string in the target format '%m/%d/%Y'
    df['date'] = df['datetime'].dt.strftime('%m/%d/%Y')
    
    # 3. Extract the hour and map it to 1-24 (Hour 0 -> 1, Hour 23 -> 24)
    df['hour_idx'] = df['datetime'].dt.hour + 1
    
    # 4. Group by date and hour, and aggregate the zone_016 values.
    # Using mean as the aggregation function.
    df_agg = df.groupby(['date', 'hour_idx'])['zone_016'].mean().reset_index()
    
    # 5. Pivot the data so that each hour becomes a column
    df_pivot = df_agg.pivot(index='date', columns='hour_idx', values='zone_016')
    
    # 6. Rename the columns to value1, value2, ..., value24
    # The columns are currently integers 1-24.
    df_pivot.columns = [f'value{c}' for c in df_pivot.columns]
    
    # 7. Reset index to make 'date' a column again
    df_pivot = df_pivot.reset_index()
    
    # 8. Ensure all 24 value columns exist, filling missing ones with NaN
    target_value_cols = [f'value{i}' for i in range(1, 25)]
    for col in target_value_cols:
        if col not in df_pivot.columns:
            df_pivot[col] = float('nan')
            
    # 9. Select and order the columns as required
    target_columns = ['date'] + target_value_cols
    return df_pivot[target_columns]