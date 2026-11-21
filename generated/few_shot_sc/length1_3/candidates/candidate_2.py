import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Transform the date column
    # Source 'date' is '%m/%d/%Y', Target 'cst' is '%a %m/%d/%Y'
    dt = pd.to_datetime(df['date'])
    df['cst'] = dt.dt.strftime('%a %m/%d/%Y')
    
    # 2. Map source hourly columns (12-hour AM/PM) to target hourly columns (24-hour)
    # Mapping logic:
    # 1:00 AM -> 1:00
    # ...
    # 11:00 AM -> 11:00
    # 12:00 PM -> 12:00 (Noon)
    # 1:00 PM -> 13:00
    # ...
    # 11:00 PM -> 23:00
    # 12:00 AM -> 24:00 (Midnight/End of day)
    
    rename_dict = {}
    
    # AM hours: 1 AM to 11 AM map to 1:00 to 11:00
    for h in range(1, 12):
        rename_dict[f'{h}:00 AM'] = f'{h}:00'
        
    # Noon: 12 PM maps to 12:00
    rename_dict['12:00 PM'] = '12:00'
    
    # PM hours: 1 PM to 11 PM map to 13:00 to 23:00
    for h in range(1, 12):
        rename_dict[f'{h}:00 PM'] = f'{h + 12}:00'
        
    # Midnight: 12 AM maps to 24:00
    rename_dict['12:00 AM'] = '24:00'
    
    df = df.rename(columns=rename_dict)
    
    # 3. Define target columns in the correct order
    target_cols = ['cst'] + [f'{i}:00' for i in range(1, 25)]
    
    # 4. Return the dataframe with only the target columns
    return df[target_cols]