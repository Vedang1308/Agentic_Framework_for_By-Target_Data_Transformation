import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the date column
    df['dt'] = pd.to_datetime(df['date'])
    
    # 2. Extract date string for grouping and final output
    df['date_str'] = df['dt'].dt.strftime('%m/%d/%Y')
    
    # 3. Extract hour and map to 1-24 scale
    # Source hour 0 (00:xx) -> Target Hour 1
    # Source hour 23 (23:xx) -> Target Hour 24
    df['hour_idx'] = df['dt'].dt.hour + 1
    
    # 4. Group by date and hour, aggregate the value
    # Using mean as a safe aggregation for constant setpoints. 
    # If multiple values exist for an hour, mean averages them.
    # If only one exists, it returns that value.
    agg_df = df.groupby(['date_str', 'hour_idx'])['zone_016_cooling_sp'].mean().reset_index()
    
    # 5. Pivot the table
    # index: date_str, columns: hour_idx, values: zone_016_cooling_sp
    pivoted = agg_df.pivot(index='date_str', columns='hour_idx', values='zone_016_cooling_sp')
    
    # 6. Rename columns to match target schema 'Hour 1', 'Hour 2', ...
    pivoted.columns = [f'Hour {int(col)}' for col in pivoted.columns]
    
    # 7. Reset index to make 'date_str' a column again
    pivoted = pivoted.reset_index().rename(columns={'date_str': 'date'})
    
    # 8. Define target columns
    target_columns = ['date'] + [f'Hour {i}' for i in range(1, 25)]
    
    # 9. Ensure all target columns exist, filling missing ones with NaN if necessary
    for col in target_columns:
        if col not in pivoted.columns:
            pivoted[col] = float('nan')
            
    # 10. Select and return only the target columns in the correct order
    return pivoted[target_columns]