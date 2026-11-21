import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # Define the exact target columns as specified
    target_columns = [
        'date', '1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', 
        '6:00 AM', '7:00 AM', '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM', 
        '12:00 AM', '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', 
        '6:00 PM', '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM', 
        '12:00 PM'
    ]
    
    # Create a copy to avoid modifying the original
    df = source.copy()
    
    # 1. Transform the Date column
    # Source format: '%a %m/%d/%Y' (e.g., 'Thu 10/01/2009')
    # Target format: '%m/%d/%Y' (e.g., '10/01/2009')
    # We parse the datetime and then format it to the desired string representation
    df['date'] = pd.to_datetime(df['Date'], format='%a %m/%d/%Y').dt.strftime('%m/%d/%Y')
    
    # 2. Rename the hourly columns from 24-hour format to 12-hour format with AM/PM
    # Source columns: 1:00, 2:00, ..., 11:00, 12:00, 13:00, ..., 23:00, 24:00:00
    # Target columns: 1:00 AM, ..., 11:00 AM, 12:00 PM, 1:00 PM, ..., 11:00 PM, 12:00 AM
    
    rename_map = {}
    
    # Handle hours 1 to 11 (AM)
    for h in range(1, 12):
        rename_map[f'{h}:00'] = f'{h}:00 AM'
        
    # Handle hour 12 (Noon -> PM)
    rename_map['12:00'] = '12:00 PM'
    
    # Handle hours 13 to 23 (PM)
    for h in range(13, 24):
        rename_map[f'{h}:00'] = f'{h-12}:00 PM'
        
    # Handle hour 24 (Midnight -> AM)
    # Note: Source column is '24:00:00'
    rename_map['24:00:00'] = '12:00 AM'
    
    df.rename(columns=rename_map, inplace=True)
    
    # 3. Drop the original 'Date' and 'Segment' columns as they are not in the target
    df.drop(columns=['Date', 'Segment'], inplace=True, errors='ignore')
    
    # 4. Reorder columns to match the target schema exactly
    # The target schema has a specific order: 
    # 1-11 AM, then 12:00 AM, then 1-11 PM, then 12:00 PM
    # We must ensure our dataframe has these columns in this order.
    
    # Verify that all target columns exist in df
    # (This is a sanity check, assuming the transformation is correct)
    
    return df[target_columns]