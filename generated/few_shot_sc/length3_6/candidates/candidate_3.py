import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Process the date column
    # Parse the source date string (e.g., '7/3/2014') to datetime
    dt = pd.to_datetime(df['date'])
    # Format to target style: 'YYYY-MM-DD 00:00:00'
    df['date'] = dt.dt.strftime('%Y-%m-%d 00:00:00')
    
    # 2. Map hourly columns from 12-hour format with AM/PM to 24-hour Hour N format
    # Source columns: '1:00 AM', '2:00 AM', ..., '12:00 AM', '1:00 PM', ..., '12:00 PM'
    # Target columns: 'Hour 1', 'Hour 2', ..., 'Hour 24'
    
    rename_map = {}
    
    # AM Hours: 1:00 AM -> Hour 1, ..., 11:00 AM -> Hour 11
    for h in range(1, 12):
        rename_map[f'{h}:00 AM'] = f'Hour {h}'
        
    # Noon: 12:00 PM -> Hour 12
    rename_map['12:00 PM'] = 'Hour 12'
    
    # PM Hours: 1:00 PM -> Hour 13, ..., 11:00 PM -> Hour 23
    for h in range(1, 12):
        rename_map[f'{h}:00 PM'] = f'Hour {h + 12}'
        
    # Midnight: 12:00 AM -> Hour 24
    rename_map['12:00 AM'] = 'Hour 24'
    
    # Apply renaming
    df = df.rename(columns=rename_map)
    
    # 3. Define target columns in the correct order
    target_columns = ['date'] + [f'Hour {i}' for i in range(1, 25)]
    
    # 4. Select and return the target columns
    # Note: If the row count difference (182 vs 183) implies a specific row addition 
    # not derivable from source structure (like a total row), it cannot be generalized 
    # without more specific rules. Assuming 1-to-1 mapping for generalization.
    return df[target_columns]