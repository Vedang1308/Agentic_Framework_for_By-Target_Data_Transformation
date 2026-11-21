import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms high-frequency time-series data into hourly binned data.
    Groups by date, aggregates values by hour, and pivots to wide format.
    """
    df = source.copy()
    
    # 1. Parse the date column
    # Format: %m/%d/%Y %H:%M
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract date string for grouping and hour for binning
    df['date'] = df['datetime'].dt.strftime('%m/%d/%Y')
    df['hour'] = df['datetime'].dt.hour
    
    # 3. Aggregate by date and hour
    # Using 'first' to get the value for that hour. If no data, it will be NaN.
    # This handles the sparse data where some hours might be missing.
    grouped = df.groupby(['date', 'hour'])['zone_016_cooling_sp'].first()
    
    # 4. Pivot/Unstack to get hours as columns
    # The index will be 'date', columns will be 'hour' (0-23)
    pivoted = grouped.unstack('hour')
    
    # 5. Define the mapping from hour integer to target column name
    # 0 -> 12:00 AM, 1 -> 1:00 AM, ..., 11 -> 11:00 AM, 
    # 12 -> 12:00 PM, 13 -> 1:00 PM, ..., 23 -> 11:00 PM
    hour_to_col = {}
    for h in range(1, 12):
        hour_to_col[h] = f'{h}:00 AM'
    hour_to_col[12] = '12:00 PM'
    for h in range(13, 24):
        hour_to_col[h] = f'{h-12}:00 PM'
    hour_to_col[0] = '12:00 AM'
    
    # Rename the columns based on the mapping
    pivoted = pivoted.rename(columns=hour_to_col)
    
    # 6. Define the target column order verbatim
    target_cols = [
        '1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', '6:00 AM', 
        '7:00 AM', '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM', '12:00 PM', 
        '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', '6:00 PM', 
        '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM', '12:00 AM'
    ]
    
    # 7. Reset index to make 'date' a column again
    pivoted = pivoted.reset_index()
    
    # 8. Ensure all target columns exist (fill missing hours with NaN if not present in data)
    for col in target_cols:
        if col not in pivoted.columns:
            pivoted[col] = float('nan')
            
    # 9. Select and return in the exact order
    return pivoted[target_cols]