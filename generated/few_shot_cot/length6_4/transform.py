import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse and format the date column
    # Source format: '7/3/2014' (%m/%d/%Y)
    # Target format: '2014-01-01 00:00:00' (%Y-%m-%d %H:%M:%S)
    dt = pd.to_datetime(df['date'])
    df['Date'] = dt.dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # 2. Map source hourly columns to target hourly columns
    # Source columns: '12:00 AM', '1:00 AM', ..., '11:00 AM', '12:00 PM', '1:00 PM', ..., '11:00 PM'
    # Target columns: 'Hr 1', 'Hr 2', ..., 'Hr 11', 'Hr 12', 'Hr 13', ..., 'Hr 24'
    
    rename_dict = {}
    
    # AM hours: 12:00 AM is Hr 1, 1:00 AM is Hr 2, ..., 11:00 AM is Hr 11
    rename_dict['12:00 AM'] = 'Hr 1'
    for i in range(1, 12):
        rename_dict[f'{i}:00 AM'] = f'Hr {i + 1}'
        
    # PM hours: 12:00 PM is Hr 12, 1:00 PM is Hr 13, ..., 11:00 PM is Hr 24
    rename_dict['12:00 PM'] = 'Hr 12'
    for i in range(1, 12):
        rename_dict[f'{i}:00 PM'] = f'Hr {i + 12}'
        
    df = df.rename(columns=rename_dict)
    
    # 3. Define target columns in the correct order
    target_columns = ['Date'] + [f'Hr {i}' for i in range(1, 25)]
    
    # 4. Return the transformed dataframe with only the target columns
    return df[target_columns]