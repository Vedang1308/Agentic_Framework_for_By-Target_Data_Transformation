import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # Define the mapping from source AM/PM columns to target Hr N columns
    # 12 AM is hour 1 (00:00), 1 AM is hour 2 (01:00), ..., 11 AM is hour 12 (11:00)
    # 12 PM is hour 13 (12:00), 1 PM is hour 14 (13:00), ..., 11 PM is hour 24 (23:00)
    rename_dict = {}
    
    # AM Hours
    # 12:00 AM -> Hr 1
    rename_dict['12:00 AM'] = 'Hr 1'
    # 1:00 AM -> Hr 2 ... 11:00 AM -> Hr 12
    for i in range(1, 12):
        rename_dict[f'{i}:00 AM'] = f'Hr {i+1}'
        
    # PM Hours
    # 12:00 PM -> Hr 13
    rename_dict['12:00 PM'] = 'Hr 13'
    # 1:00 PM -> Hr 14 ... 11:00 PM -> Hr 24
    for i in range(1, 12):
        rename_dict[f'{i}:00 PM'] = f'Hr {i+12}'
        
    # Rename columns
    df = df.rename(columns=rename_dict)
    
    # Transform the date column
    # Source format: '7/3/2014' (%m/%d/%Y)
    # Target format: '2014-01-01 00:00:00' (%Y-%m-%d %H:%M:%S)
    df['Date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Define target columns in the correct order
    target_columns = ['Date'] + [f'Hr {i}' for i in range(1, 25)]
    
    # Return only the target columns
    return df[target_columns]