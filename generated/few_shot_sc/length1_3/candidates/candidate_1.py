import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the 'date' column and format it to 'cst'
    # Source format: '7/3/2014' (M/D/YYYY)
    # Target format: 'Wed 01/01/2014' (%a %m/%d/%Y)
    dt = pd.to_datetime(df['date'])
    df['cst'] = dt.dt.strftime('%a %m/%d/%Y')
    
    # 2. Rename hourly columns from 12-hour AM/PM format to 24-hour format
    # Mapping:
    # 1:00 AM -> 1:00, ..., 11:00 AM -> 11:00
    # 12:00 PM -> 12:00
    # 1:00 PM -> 13:00, ..., 11:00 PM -> 23:00
    # 12:00 AM -> 24:00
    
    rename_dict = {}
    
    # AM hours (1-11)
    for h in range(1, 12):
        rename_dict[f'{h}:00 AM'] = f'{h}:00'
        
    # Noon
    rename_dict['12:00 PM'] = '12:00'
    
    # PM hours (1-11) -> 13:00 to 23:00
    for h in range(1, 12):
        rename_dict[f'{h}:00 PM'] = f'{h+12}:00'
        
    # Midnight (12:00 AM) -> 24:00
    rename_dict['12:00 AM'] = '24:00'
    
    df = df.rename(columns=rename_dict)
    
    # 3. Define target columns in the correct order
    target_cols = ['cst'] + [f'{h}:00' for h in range(1, 25)]
    
    # 4. Return the DataFrame with only the target columns
    return df[target_cols]