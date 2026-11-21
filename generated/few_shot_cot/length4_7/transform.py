import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Process Date Column
    # Source format: 'Thu 10/01/2009' (%a %m/%d/%Y)
    # Target format: '01/01/2003' (%m/%d/%Y)
    # We can parse the date part directly.
    # Splitting by space and taking the last element gives '10/01/2009'
    date_str = df['Date'].str.split(' ').str[-1]
    dt = pd.to_datetime(date_str, format='%m/%d/%Y')
    df['date'] = dt.dt.strftime('%m/%d/%Y')
    
    # 2. Rename Hour Columns
    # Source: '1:00'...'23:00', '24:00:00'
    # Target: '1:00 AM'...'11:00 AM', '12:00 PM', '1:00 PM'...'11:00 PM', '12:00 AM'
    
    rename_dict = {}
    
    # 1:00 to 11:00 -> 1:00 AM to 11:00 AM
    for h in range(1, 12):
        rename_dict[f'{h}:00'] = f'{h}:00 AM'
        
    # 12:00 -> 12:00 PM (Noon)
    rename_dict['12:00'] = '12:00 PM'
    
    # 13:00 to 23:00 -> 1:00 PM to 11:00 PM
    for h in range(13, 24):
        rename_dict[f'{h}:00'] = f'{h-12}:00 PM'
        
    # 24:00:00 -> 12:00 AM (Midnight)
    rename_dict['24:00:00'] = '12:00 AM'
    
    df = df.rename(columns=rename_dict)
    
    # 3. Define Target Columns in the exact order specified
    target_columns = [
        'date', 
        '1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', '6:00 AM', '7:00 AM', 
        '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM', '12:00 AM', 
        '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', '6:00 PM', 
        '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM', '12:00 PM'
    ]
    
    return df[target_columns]