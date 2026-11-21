import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    df = source.copy()
    
    # 1. Parse the date column
    # Source format is '%m/%d/%Y %H:%M' (e.g., '7/28/2019 4:50')
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %I:%M %p', errors='coerce')
    # If the above fails due to single-digit hours without leading zeros or specific AM/PM missing,
    # pandas usually handles '%m/%d/%Y %H:%M' or mixed formats well with infer_datetime_format.
    # Let's try a more robust parsing if the simple format fails.
    # The sample '7/28/2019 4:50' suggests 24-hour or 12-hour without AM/PM?
    # Wait, the sample shows '4:50'. Is that 4:50 AM or PM?
    # Let's look at the target values.
    # If we assume standard 24h format for parsing first.
    # Actually, looking at '12/31/2020 23:50', it is clearly 24-hour format.
    # So '4:50' is 04:50.
    
    # Re-parse assuming 24-hour format for the time part, but flexible date part
    df['datetime'] = pd.to_datetime(df['date'])
    
    # 2. Create grouping keys
    # Date part for the index
    df['date_str'] = df['datetime'].dt.strftime('%m/%d/%Y')
    
    # Hour part for the columns
    df['hour'] = df['datetime'].dt.hour
    
    # 3. Map hour to target column names
    # 0 -> 12:00 AM, 1 -> 1:00 AM, ..., 11 -> 11:00 AM
    # 12 -> 12:00 PM, 13 -> 1:00 PM, ..., 23 -> 11:00 PM
    def map_hour_to_col(h):
        if h == 0:
            return '12:00 AM'
        elif h < 12:
            return f'{h}:00 AM'
        elif h == 12:
            return '12:00 PM'
        else:
            return f'{h-12}:00 PM'
            
    df['hour_col'] = df['hour'].apply(map_hour_to_col)
    
    # 4. Aggregate and Pivot
    # Group by date and hour column, take the mean of cerc_logger_1
    agg_df = df.groupby(['date_str', 'hour_col'])['cerc_logger_1'].mean().reset_index()
    
    # Pivot to wide format
    pivot_df = agg_df.pivot(index='date_str', columns='hour_col', values='cerc_logger_1')
    
    # 5. Define target columns in the correct order
    # Order: 1 AM -> 11 AM, 12 PM, 1 PM -> 11 PM, 12 AM
    am_cols = [f'{h}:00 AM' for h in range(1, 12)] # 1:00 AM to 11:00 AM
    pm_cols = [f'{h}:00 PM' for h in range(12, 24)] # 12:00 PM to 11:00 PM (12->12, 13->1, ... 23->11)
    # Wait, 12:00 PM is noon. 1:00 PM is 13:00.
    # My map_hour_to_col:
    # 12 -> 12:00 PM
    # 13 -> 1:00 PM
    # ...
    # 23 -> 11:00 PM
    # So pm_cols should be: '12:00 PM', '1:00 PM', ..., '11:00 PM'
    
    # Let's reconstruct the exact order based on the target schema provided:
    # ['1:00 AM', ..., '11:00 AM', '12:00 PM', '1:00 PM', ..., '11:00 PM', '12:00 AM']
    
    target_cols = []
    # 1 AM to 11 AM
    for h in range(1, 12):
        target_cols.append(f'{h}:00 AM')
    # 12 PM
    target_cols.append('12:00 PM')
    # 1 PM to 11 PM
    for h in range(1, 12):
        target_cols.append(f'{h}:00 PM')
    # 12 AM (Midnight)
    target_cols.append('12:00 AM')
    
    # Ensure all columns exist in pivot_df (fill missing with NaN)
    for col in target_cols:
        if col not in pivot_df.columns:
            pivot_df[col] = pd.NA
            
    # Select and order columns
    result_df = pivot_df[target_cols]
    
    # Rename index to 'date' and reset
    result_df = result_df.reset_index()
    result_df = result_df.rename(columns={'date_str': 'date'})
    
    return result_df[target_cols]