import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the date from the 'CST' column
    # The format is '%a %m/%d/%Y' (e.g., 'Sat 12/01/2012')
    # pd.to_datetime can handle this format directly.
    dt = pd.to_datetime(df['CST'])
    
    # 2. Format the date as '%m/%d/%Y' for the 'Date' column
    df['Date'] = dt.dt.strftime('%m/%d/%Y')
    
    # 3. Rename the hourly columns
    # Source columns: '1:00' ... '23:00', '24:00:00'
    # Target columns: 'Hr 1' ... 'Hr 23', 'Hr 24'
    rename_dict = {}
    for i in range(1, 24):
        rename_dict[f'{i}:00'] = f'Hr {i}'
    rename_dict['24:00:00'] = 'Hr 24'
    
    df = df.rename(columns=rename_dict)
    
    # 4. Define the target columns in the correct order
    target_cols = ['Date'] + [f'Hr {i}' for i in range(1, 25)]
    
    # 5. Select and return the target columns
    return df[target_cols]