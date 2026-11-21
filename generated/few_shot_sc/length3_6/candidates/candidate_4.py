import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse and format the date column
    # Source format: '%m/%d/%Y' (e.g., '7/3/2014')
    # Target format: '%Y-%m-%d %H:%M:%S' (e.g., '2014-01-01 00:00:00')
    df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # 2. Define mapping for hour columns
    # Source columns: '1:00 AM'...'11:00 AM', '12:00 AM', '1:00 PM'...'12:00 PM'
    # Target columns: 'Hour 1'...'Hour 24'
    
    mapping = {}
    
    # AM Hours: 1:00 AM -> Hour 1, ..., 11:00 AM -> Hour 11
    for h in range(1, 12):
        mapping[f'{h}:00 AM'] = f'Hour {h}'
        
    # 12:00 PM -> Hour 12
    mapping['12:00 PM'] = 'Hour 12'
    
    # PM Hours: 1:00 PM -> Hour 13, ..., 11:00 PM -> Hour 23
    for h in range(1, 12):
        mapping[f'{h}:00 PM'] = f'Hour {h + 12}'
        
    # 12:00 AM -> Hour 24
    mapping['12:00 AM'] = 'Hour 24'
    
    # Apply renaming
    df = df.rename(columns=mapping)
    
    # 3. Define target columns
    target_columns = ['date'] + [f'Hour {i}' for i in range(1, 25)]
    
    # 4. Select and return
    return df[target_columns]