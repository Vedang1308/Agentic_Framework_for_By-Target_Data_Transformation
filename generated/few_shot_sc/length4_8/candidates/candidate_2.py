import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    df = source.copy()
    
    # 1. Parse the date column
    # Source format: '%m/%d/%Y %H:%M'
    df['dt'] = pd.to_datetime(df['date'])
    
    # 2. Extract date string for grouping and output
    df['date_key'] = df['dt'].dt.strftime('%m/%d/%Y')
    
    # 3. Extract hour integer (0-23)
    df['hour_int'] = df['dt'].dt.hour
    
    # 4. Map hour integer to target column names
    # 0 -> 12:00 AM
    # 1-11 -> 1:00 AM - 11:00 AM
    # 12 -> 12:00 PM
    # 13-23 -> 1:00 PM - 11:00 PM
    def map_hour_to_label(h):
        if h == 0:
            return '12:00 AM'
        elif 1 <= h <= 11:
            return f'{h}:00 AM'
        elif h == 12:
            return '12:00 PM'
        else:
            return f'{h-12}:00 PM'
            
    df['hour_label'] = df['hour_int'].apply(map_hour_to_label)
    
    # 5. Pivot the data
    # Aggregate by date and hour_label, taking the mean of cerc_logger_1
    # If there are multiple readings per hour, average them.
    pivot_df = df.pivot_table(
        index='date_key',
        columns='hour_label',
        values='cerc_logger_1',
        aggfunc='mean'
    )
    
    # 6. Fill missing values with 0 (in case an hour has no data)
    pivot_df = pivot_df.fillna(0)
    
    # 7. Reset index to make date a column
    pivot_df = pivot_df.reset_index()
    pivot_df.rename(columns={'date_key': 'date'}, inplace=True)
    
    # 8. Define the exact target column order
    target_columns = [
        'date', '1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', '6:00 AM', 
        '7:00 AM', '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM', '12:00 PM', 
        '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', '6:00 PM', 
        '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM', '12:00 AM'
    ]
    
    # 9. Select and return columns in the correct order
    # Ensure all columns exist (pivot might miss some if no data for that hour ever)
    for col in target_columns:
        if col not in pivot_df.columns:
            pivot_df[col] = 0
            
    return pivot_df[target_columns]