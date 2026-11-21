import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse and format the Date column
    # Source format: 'Thu 10/01/2009' (%a %m/%d/%Y)
    # Target format: '01/01/2003' (%m/%d/%Y)
    dt = pd.to_datetime(df['Date'], format='%a %m/%d/%Y')
    df['date'] = dt.dt.strftime('%m/%d/%Y')
    
    # 2. Define the mapping from Source hourly columns to Target hourly columns
    # Source columns are 24-hour format: 1:00, 2:00, ..., 23:00, 24:00:00
    # Target columns are 12-hour format with AM/PM
    
    rename_dict = {}
    
    # 1:00 to 11:00 -> 1:00 AM to 11:00 AM
    for h in range(1, 12):
        rename_dict[f'{h}:00'] = f'{h}:00 AM'
        
    # 12:00 -> 12:00 PM (Noon)
    rename_dict['12:00'] = '12:00 PM'
    
    # 13:00 to 23:00 -> 1:00 PM to 11:00 PM
    for h in range(13, 24):
        hour_12 = h - 12
        rename_dict[f'{h}:00'] = f'{hour_12}:00 PM'
        
    # 24:00:00 -> 12:00 AM (Midnight)
    rename_dict['24:00:00'] = '12:00 AM'
    
    df = df.rename(columns=rename_dict)
    
    # 3. Define the exact target column order as specified in the prompt
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