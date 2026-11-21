import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse and format the date column
    # Source format: '%a %m/%d/%Y' (e.g., 'Sat 12/01/2012')
    # Target format: '%m/%d/%Y' (e.g., '04/01/2009')
    df['date'] = pd.to_datetime(df['CST'], format='%a %m/%d/%Y').dt.strftime('%m/%d/%Y')
    
    # 2. Rename the hourly value columns
    # Source columns: '1:00', '2:00', ..., '23:00', '24:00:00'
    # Target columns: 'value1', 'value2', ..., 'value23', 'value24'
    
    rename_map = {}
    for i in range(1, 24):
        rename_map[f'{i}:00'] = f'value{i}'
    rename_map['24:00:00'] = 'value24'
    
    df = df.rename(columns=rename_map)
    
    # 3. Define the target column order
    target_columns = ['date'] + [f'value{i}' for i in range(1, 25)]
    
    # 4. Select and return the columns in the correct order
    return df[target_columns]