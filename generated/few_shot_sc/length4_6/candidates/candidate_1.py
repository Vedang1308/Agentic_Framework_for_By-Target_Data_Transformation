import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse and format the date
    dt = pd.to_datetime(df['Date'])
    df['date'] = dt.dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # 2. Map source hourly columns to target 12-hour format columns
    # Source: Hr 1 (1 AM) ... Hr 11 (11 AM), Hr 12 (12 PM/Noon), Hr 13 (1 PM) ... Hr 23 (11 PM), Hr 24 (12 AM/Midnight)
    # Target columns requested in specific order:
    # 1:00 AM ... 11:00 AM, 12:00 AM, 1:00 PM ... 11:00 PM, 12:00 PM
    
    rename_dict = {}
    
    # AM Hours: 1 to 11
    for i in range(1, 12):
        rename_dict[f'Hr {i}'] = f'{i}:00 AM'
        
    # Midnight: Hr 24 -> 12:00 AM
    rename_dict['Hr 24'] = '12:00 AM'
    
    # PM Hours: 1 to 11 (Source Hr 13 to 23)
    for i in range(1, 12):
        source_hr = i + 12
        rename_dict[f'Hr {source_hr}'] = f'{i}:00 PM'
        
    # Noon: Hr 12 -> 12:00 PM
    rename_dict['Hr 12'] = '12:00 PM'
    
    df = df.rename(columns=rename_dict)
    
    # 3. Define target columns in the exact order specified
    target_columns = [
        'date', 
        '1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', '6:00 AM', 
        '7:00 AM', '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM', 
        '12:00 AM', 
        '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', '6:00 PM', 
        '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM', 
        '12:00 PM'
    ]
    
    return df[target_columns]