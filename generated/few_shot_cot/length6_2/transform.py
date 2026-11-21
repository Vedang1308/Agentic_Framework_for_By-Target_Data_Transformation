import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the CST column and format as MM/DD/YYYY for the 'Date' column
    # Source format: '%a %m/%d/%Y' (e.g., 'Sat 12/01/2012')
    # Target format: '%m/%d/%Y' (e.g., '12/01/2012')
    df['Date'] = pd.to_datetime(df['CST']).dt.strftime('%m/%d/%Y')
    
    # 2. Rename the hourly columns
    # Source: '1:00', '2:00', ..., '23:00', '24:00:00'
    # Target: 'Hr 1', 'Hr 2', ..., 'Hr 23', 'Hr 24'
    rename_dict = {}
    for i in range(1, 24):
        rename_dict[f'{i}:00'] = f'Hr {i}'
    rename_dict['24:00:00'] = 'Hr 24'
    
    df = df.rename(columns=rename_dict)
    
    # 3. Define the target columns in the correct order
    target_columns = ['Date'] + [f'Hr {i}' for i in range(1, 25)]
    
    # 4. Return the DataFrame with only the target columns
    return df[target_columns]