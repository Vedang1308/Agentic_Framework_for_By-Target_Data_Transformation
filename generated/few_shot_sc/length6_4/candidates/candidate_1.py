import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame to the target schema.
    """
    df = source.copy()
    
    # 1. Transform the date column
    # Parse the source date 'M/D/YYYY' and format to 'YYYY-MM-DD 00:00:00'
    dt = pd.to_datetime(df['date'])
    df['Date'] = dt.dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # 2. Map hour columns to target names 'Hr 1' ... 'Hr 24'
    # Logic derived from semantic mapping:
    # 1:00 AM -> Hr 1, ..., 11:00 AM -> Hr 11
    # 12:00 PM -> Hr 12
    # 1:00 PM -> Hr 13, ..., 11:00 PM -> Hr 23
    # 12:00 AM -> Hr 24
    
    rename_map = {}
    
    # AM hours 1-11
    for i in range(1, 12):
        rename_map[f'{i}:00 AM'] = f'Hr {i}'
        
    # PM hours 1-11 mapped to 13-23
    for i in range(1, 12):
        rename_map[f'{i}:00 PM'] = f'Hr {i + 12}'
        
    # 12:00 PM maps to Hr 12
    rename_map['12:00 PM'] = 'Hr 12'
    
    # 12:00 AM maps to Hr 24
    rename_map['12:00 AM'] = 'Hr 24'
    
    df = df.rename(columns=rename_map)
    
    # 3. Define target columns
    target_columns = ['Date'] + [f'Hr {i}' for i in range(1, 25)]
    
    # 4. Select and return
    return df[target_columns]