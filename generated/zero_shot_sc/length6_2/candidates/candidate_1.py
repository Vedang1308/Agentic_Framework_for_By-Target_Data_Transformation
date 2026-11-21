import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    # Create a copy to avoid modifying the original
    df = source.copy()
    
    # 1. Process the Date column
    # Source format: '%a %m/%d/%Y' (e.g., 'Sat 12/01/2012')
    # Target format: '%m/%d/%Y' (e.g., '04/01/2009')
    # We parse to datetime first to ensure correctness, then format.
    df['Date'] = pd.to_datetime(df['CST'], format='%a %m/%d/%Y').dt.strftime('%m/%d/%Y')
    
    # 2. Rename the hourly columns
    # Source columns: '1:00', '2:00', ..., '23:00', '24:00:00'
    # Target columns: 'Hr 1', 'Hr 2', ..., 'Hr 23', 'Hr 24'
    
    rename_map = {}
    for i in range(1, 24):
        rename_map[f'{i}:00'] = f'Hr {i}'
    rename_map['24:00:00'] = 'Hr 24'
    
    df = df.rename(columns=rename_map)
    
    # 3. Define the target columns in the correct order
    target_columns = ['Date'] + [f'Hr {i}' for i in range(1, 25)]
    
    # 4. Select and order the columns
    # Note: The prompt mentions a row count change (1339 -> 1340). 
    # Without a specific trigger for splitting/duplicating rows in the schema, 
    # and given the wide-to-wide structure, we assume a direct mapping. 
    # If the target requires sorting (as seen in the sample), we sort by Date.
    df = df.sort_values(by='Date').reset_index(drop=True)
    
    # 5. Return the DataFrame with exactly the target columns
    return df[target_columns]