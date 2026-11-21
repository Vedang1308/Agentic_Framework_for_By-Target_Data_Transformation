import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse and format the date column
    # Source 'date' is M/D/YYYY, Target 'cst' is '%a %m/%d/%Y'
    dt = pd.to_datetime(df['date'])
    df['cst'] = dt.dt.strftime('%a %m/%d/%Y')
    
    # 2. Map source hourly columns to target hourly columns
    # Source: 1:00 AM ... 11:00 AM, 12:00 PM, 1:00 PM ... 11:00 PM, 12:00 AM
    # Target: 1:00 ... 11:00, 12:00, 13:00 ... 23:00, 24:00
    
    rename_dict = {}
    
    # 1:00 AM to 11:00 AM -> 1:00 to 11:00
    for h in range(1, 12):
        rename_dict[f'{h}:00 AM'] = f'{h}:00'
        
    # 12:00 PM -> 12:00
    rename_dict['12:00 PM'] = '12:00'
    
    # 1:00 PM to 11:00 PM -> 13:00 to 23:00
    for h in range(1, 12):
        rename_dict[f'{h}:00 PM'] = f'{h + 12}:00'
        
    # 12:00 AM -> 24:00
    rename_dict['12:00 AM'] = '24:00'
    
    df = df.rename(columns=rename_dict)
    
    # 3. Define target columns in the correct order
    target_cols = ['cst'] + [f'{h}:00' for h in range(1, 25)]
    
    # 4. Return the transformed dataframe with only the target columns
    return df[target_cols]