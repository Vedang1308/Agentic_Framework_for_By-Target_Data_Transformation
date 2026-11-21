import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the date column
    # Format in source: '%m/%d/%Y %H:%M'
    df['datetime'] = pd.to_datetime(df['date'])
    
    # 2. Extract date string for grouping and final output
    df['date_str'] = df['datetime'].dt.strftime('%m/%d/%Y')
    
    # 3. Extract hour for grouping (0-23)
    df['hour'] = df['datetime'].dt.hour
    
    # 4. Aggregate data by date and hour
    # We use mean() to average minute-level data into hourly data. 
    # skipna=True is default.
    grouped = df.groupby(['date_str', 'hour'])['zone_016'].mean().reset_index()
    
    # 5. Pivot the table to have hours as columns
    # index: date_str, columns: hour, values: zone_016
    pivoted = grouped.pivot(index='date_str', columns='hour', values='zone_016')
    
    # 6. Rename hour columns to value1, value2, ..., value24
    # Hour 0 -> value1, Hour 1 -> value2, ..., Hour 23 -> value24
    rename_map = {h: f'value{h+1}' for h in range(24)}
    pivoted = pivoted.rename(columns=rename_map)
    
    # 7. Reset index to make 'date_str' a column
    pivoted = pivoted.reset_index()
    
    # 8. Rename 'date_str' to 'date' to match target schema
    pivoted = pivoted.rename(columns={'date_str': 'date'})
    
    # 9. Define target columns in order
    target_columns = ['date'] + [f'value{i}' for i in range(1, 25)]
    
    # 10. Ensure all value columns exist (fill missing with NaN if necessary)
    for col in target_columns:
        if col not in pivoted.columns:
            pivoted[col] = float('nan')
            
    # 11. Return the DataFrame with exact target columns
    return pivoted[target_columns]