import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the date from the 'CST' column
    # Source format: '%a %m/%d/%Y' (e.g., 'Sat 12/01/2012')
    # We can parse this directly using pd.to_datetime
    dt = pd.to_datetime(df['CST'])
    
    # 2. Format the date for the 'Date' column
    # Target format: '%m/%d/%Y' (e.g., '12/01/2012')
    df['Date'] = dt.dt.strftime('%m/%d/%Y')
    
    # 3. Rename the hourly columns
    # Source columns: '1:00', '2:00', ..., '23:00', '24:00:00'
    # Target columns: 'Hr 1', 'Hr 2', ..., 'Hr 23', 'Hr 24'
    
    rename_dict = {}
    for i in range(1, 24):
        rename_dict[f'{i}:00'] = f'Hr {i}'
    # Handle the 24th hour specifically as it has a different source name
    rename_dict['24:00:00'] = 'Hr 24'
    
    df = df.rename(columns=rename_dict)
    
    # 4. Define the target column order
    target_columns = ['Date'] + [f'Hr {i}' for i in range(1, 25)]
    
    # 5. Return the dataframe with only the target columns
    return df[target_columns]