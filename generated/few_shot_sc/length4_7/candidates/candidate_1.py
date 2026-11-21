import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    df = source.copy()
    
    # 1. Parse and format the date column
    # Source format: 'Thu 10/01/2009'
    # Extract the date part (last whitespace-separated token)
    date_str = df['Date'].str.split(' ').str[-1]
    # Convert to datetime
    dt = pd.to_datetime(date_str, format='%m/%d/%Y')
    # Format as 'MM/DD/YYYY'
    df['date'] = dt.dt.strftime('%m/%d/%Y')
    
    # 2. Define the mapping from source 24-hour columns to target 12-hour AM/PM columns
    # Source columns: '1:00' to '23:00' and '24:00:00'
    # Target columns: '1:00 AM' ... '12:00 PM' etc.
    
    rename_dict = {}
    
    # Hours 1-11 map to 1 AM - 11 AM
    for h in range(1, 12):
        rename_dict[f'{h}:00'] = f'{h}:00 AM'
        
    # Hour 12 maps to 12:00 PM (Noon)
    rename_dict['12:00'] = '12:00 PM'
    
    # Hours 13-23 map to 1 PM - 11 PM
    for h in range(13, 24):
        target_h = h - 12
        rename_dict[f'{h}:00'] = f'{target_h}:00 PM'
        
    # Hour 24:00:00 maps to 12:00 AM (Midnight)
    rename_dict['24:00:00'] = '12:00 AM'
    
    # Apply renaming
    df = df.rename(columns=rename_dict)
    
    # 3. Define the exact target column order as specified in the prompt
    target_cols = [
        'date', 
        '1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', '6:00 AM', '7:00 AM', '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM', 
        '12:00 AM', 
        '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', '6:00 PM', '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM', 
        '12:00 PM'
    ]
    
    # Return the dataframe with the specified columns
    return df[target_cols]