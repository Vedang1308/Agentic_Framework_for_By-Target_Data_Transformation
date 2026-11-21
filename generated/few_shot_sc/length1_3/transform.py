import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the date column and format it for 'cst'
    # Source format: 'M/D/YYYY' or 'MM/DD/YYYY'
    # Target format: 'Day MM/DD/YYYY' (e.g., 'Wed 01/01/2014')
    dt = pd.to_datetime(df['date'])
    df['cst'] = dt.dt.strftime('%a %m/%d/%Y')
    
    # 2. Define the mapping from Source Hourly Columns to Target Hourly Columns
    # Source: 1:00 AM ... 11:00 AM, 12:00 AM, 1:00 PM ... 12:00 PM
    # Target: 1:00 ... 11:00, 24:00, 13:00 ... 12:00
    
    rename_dict = {}
    
    # AM Hours: 1:00 AM -> 1:00, ..., 11:00 AM -> 11:00
    for i in range(1, 12):
        rename_dict[f'{i}:00 AM'] = f'{i}:00'
        
    # 12:00 AM -> 24:00
    rename_dict['12:00 AM'] = '24:00'
    
    # PM Hours: 1:00 PM -> 13:00, ..., 11:00 PM -> 23:00
    for i in range(1, 12):
        rename_dict[f'{i}:00 PM'] = f'{i + 12}:00'
        
    # 12:00 PM -> 12:00
    rename_dict['12:00 PM'] = '12:00'
    
    # 3. Rename the columns
    df = df.rename(columns=rename_dict)
    
    # 4. Define the target column order
    target_cols = ['cst'] + [f'{i}:00' for i in range(1, 25)]
    
    # 5. Select and return the target columns
    return df[target_cols]