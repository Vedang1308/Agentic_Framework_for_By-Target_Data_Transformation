import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the datetime column
    df['dt'] = pd.to_datetime(df['date'])
    
    # 2. Extract date string for grouping and hour for pivoting
    # Target Date format is %m/%d/%Y
    df['Date'] = df['dt'].dt.strftime('%m/%d/%Y')
    
    # Target columns are Hr 1 (hour 0) to Hr 24 (hour 23)
    df['hour_label'] = 'Hr ' + (df['dt'].dt.hour + 1).astype(str)
    
    # 3. Aggregate and Pivot
    # We group by Date and hour_label, then take the mean of the value column
    # Using mean handles cases where there are multiple entries per hour
    pivot_df = df.groupby(['Date', 'hour_label'])['zone_016_cooling_sp'].mean().reset_index()
    
    # Pivot the table
    # index: Date, columns: hour_label, values: zone_016_cooling_sp
    pivoted = pivot_df.pivot(index='Date', columns='hour_label', values='zone_016_cooling_sp')
    
    # 4. Ensure all 24 hour columns exist and are in correct order
    target_hour_cols = [f'Hr {i}' for i in range(1, 25)]
    
    # Reindex columns to ensure order and presence of all hours (missing become NaN)
    pivoted = pivoted.reindex(columns=target_hour_cols)
    
    # Reset index to make Date a column again
    pivoted = pivoted.reset_index()
    
    # 5. Select and order final columns
    target_columns = ['Date'] + target_hour_cols
    result = pivoted[target_columns]
    
    return result