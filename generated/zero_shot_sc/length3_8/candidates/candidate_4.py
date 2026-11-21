import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Transform the date column 'CST' to 'date'
    # Source format: '%a %m/%d/%Y' (e.g., 'Sat 12/01/2012')
    # Target format: '%m/%d/%Y' (e.g., '12/01/2012')
    df['date'] = pd.to_datetime(df['CST'], format='%a %m/%d/%Y').dt.strftime('%m/%d/%Y')
    
    # 2. Rename the hourly columns
    # Source columns: '1:00', '2:00', ..., '23:00', '24:00:00'
    # Target columns: 'Hour 1', 'Hour 2', ..., 'Hour 23', 'Hour 24'
    
    rename_map = {}
    for i in range(1, 24):
        rename_map[f'{i}:00'] = f'Hour {i}'
    rename_map['24:00:00'] = 'Hour 24'
    
    df = df.rename(columns=rename_map)
    
    # 3. Define target columns in the exact required order
    target_columns = [
        'date', 'Hour 1', 'Hour 2', 'Hour 3', 'Hour 4', 'Hour 5', 'Hour 6', 
        'Hour 7', 'Hour 8', 'Hour 9', 'Hour 10', 'Hour 11', 'Hour 12', 
        'Hour 13', 'Hour 14', 'Hour 15', 'Hour 16', 'Hour 17', 'Hour 18', 
        'Hour 19', 'Hour 20', 'Hour 21', 'Hour 22', 'Hour 23', 'Hour 24'
    ]
    
    # 4. Select and return the columns in the correct order
    return df[target_columns]