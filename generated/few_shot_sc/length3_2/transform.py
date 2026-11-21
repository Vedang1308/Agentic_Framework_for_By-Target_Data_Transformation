import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms source DataFrame with timestamped sensor readings into a daily 
    hourly summary DataFrame with columns 'date', 'Hour 1', ..., 'Hour 24'.
    """
    df = source.copy()
    
    # 1. Parse the date column to datetime
    df['datetime'] = pd.to_datetime(df['date'])
    
    # 2. Extract date and hour components
    # Target date format is MM/DD/YYYY
    df['date_only'] = df['datetime'].dt.strftime('%m/%d/%Y')
    # Source hour is 0-23. Target 'Hour 1' corresponds to source hour 0 (midnight).
    df['hour_idx'] = df['datetime'].dt.hour
    
    # 3. Group by date and hour, and aggregate the sensor value
    # We use mean to average the readings within each hour bucket for each day
    grouped = df.groupby(['date_only', 'hour_idx'])['cerc_logger_1'].mean()
    
    # 4. Unstack to pivot hours into columns
    # This creates a DataFrame with index='date_only' and columns=0..23
    pivoted = grouped.unstack(level='hour_idx')
    
    # 5. Rename columns from integers (0-23) to 'Hour 1'-'Hour 24'
    rename_map = {i: f'Hour {i + 1}' for i in range(24)}
    pivoted = pivoted.rename(columns=rename_map)
    
    # 6. Reset index to make 'date_only' a column
    pivoted = pivoted.reset_index()
    
    # 7. Rename 'date_only' to 'date' to match target schema
    pivoted = pivoted.rename(columns={'date_only': 'date'})
    
    # 8. Define target columns in the exact required order
    target_columns = ['date'] + [f'Hour {i}' for i in range(1, 25)]
    
    # 9. Select and return the final DataFrame
    # Note: If some hours are missing for a day, they will be NaN. 
    # The problem statement implies a dense grid, but we ensure column presence.
    return pivoted[target_columns]