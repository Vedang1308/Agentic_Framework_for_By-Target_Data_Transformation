import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    df = source.copy()
    
    # Parse the date column
    df['datetime'] = pd.to_datetime(df['date'])
    
    # Extract date string for the target 'date' column
    df['target_date'] = df['datetime'].dt.strftime('%m/%d/%Y')
    
    # Extract hour (0-23)
    df['hour'] = df['datetime'].dt.hour
    
    # Map hour to target column names
    def map_hour_to_col(h):
        if h == 0:
            return '12:00 AM'
        elif h < 12:
            return f'{h}:00 AM'
        elif h == 12:
            return '12:00 PM'
        else:
            return f'{h-12}:00 PM'
            
    df['target_col'] = df['hour'].apply(map_hour_to_col)
    
    # Pivot the table
    # Index: target_date, Columns: target_col, Values: zone_016_cooling_sp
    # Use mean to aggregate multiple entries per hour/day
    pivot_df = df.pivot_table(
        index='target_date', 
        columns='target_col', 
        values='zone_016_cooling_sp', 
        aggfunc='mean'
    )
    
    # Reset index to make 'target_date' a column
    pivot_df = pivot_df.reset_index()
    pivot_df = pivot_df.rename(columns={'target_date': 'date'})
    
    # Define the exact target column order
    target_columns = [
        'date', 
        '1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', '6:00 AM', '7:00 AM', 
        '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM', '12:00 PM', '1:00 PM', '2:00 PM', 
        '3:00 PM', '4:00 PM', '5:00 PM', '6:00 PM', '7:00 PM', '8:00 PM', '9:00 PM', 
        '10:00 PM', '11:00 PM', '12:00 AM'
    ]
    
    # Select and order columns. Missing columns in pivot_df will be filled with NaN automatically by selection if we ensure they exist, 
    # but pivot_table only creates columns that exist in the data. 
    # We need to ensure all target columns are present, filling missing ones with NaN.
    for col in target_columns:
        if col not in pivot_df.columns:
            pivot_df[col] = float('nan')
            
    return pivot_df[target_columns]