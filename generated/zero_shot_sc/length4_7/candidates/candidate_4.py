import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # Define the exact target columns in the required order
    target_columns = [
        'date', '1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', '6:00 AM', '7:00 AM', 
        '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM', '12:00 AM', '1:00 PM', '2:00 PM', 
        '3:00 PM', '4:00 PM', '5:00 PM', '6:00 PM', '7:00 PM', '8:00 PM', '9:00 PM', 
        '10:00 PM', '11:00 PM', '12:00 PM'
    ]
    
    # Create a copy to avoid modifying the original
    df = source.copy()
    
    # 1. Process the Date column
    # Source format: '%a %m/%d/%Y' (e.g., 'Thu 10/01/2009')
    # Target format: '%m/%d/%Y' (e.g., '01/01/2003')
    df['date'] = pd.to_datetime(df['Date'], format='%a %m/%d/%Y').dt.strftime('%m/%d/%Y')
    
    # 2. Define mapping from source hour columns to target hour columns
    # Source columns: 1:00, 2:00, ..., 12:00, 13:00, ..., 23:00, 24:00:00
    # Target columns: 1:00 AM, ..., 11:00 AM, 12:00 PM (Noon), 1:00 PM, ..., 11:00 PM, 12:00 AM (Midnight)
    
    col_mapping = {}
    
    # Hours 1-11 correspond to 1:00 AM - 11:00 AM
    for h in range(1, 12):
        col_mapping[f'{h}:00'] = f'{h}:00 AM'
        
    # Hour 12 corresponds to 12:00 PM (Noon)
    col_mapping['12:00'] = '12:00 PM'
    
    # Hours 13-23 correspond to 1:00 PM - 11:00 PM
    for h in range(13, 24):
        target_h = h - 12
        col_mapping[f'{h}:00'] = f'{target_h}:00 PM'
        
    # Hour 24:00:00 corresponds to 12:00 AM (Midnight)
    col_mapping['24:00:00'] = '12:00 AM'
    
    # 3. Rename the columns
    df.rename(columns=col_mapping, inplace=True)
    
    # 4. Select and order columns to match target schema exactly
    return df[target_columns]