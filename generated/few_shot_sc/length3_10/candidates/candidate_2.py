import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Process the Date column
    # Source format: '%a %m/%d/%Y' (e.g., 'Thu 10/01/2009')
    # Target format: '%m/%d/%Y' (e.g., '01/01/2003')
    # pd.to_datetime can parse the source format directly.
    dt_parsed = pd.to_datetime(df['Date'])
    df['date'] = dt_parsed.dt.strftime('%m/%d/%Y')
    
    # 2. Rename hour columns
    # Source: '1:00', '2:00', ..., '23:00', '24:00:00'
    # Target: 'Hour 1', 'Hour 2', ..., 'Hour 23', 'Hour 24'
    rename_dict = {}
    for i in range(1, 24):
        rename_dict[f'{i}:00'] = f'Hour {i}'
    # Handle the specific 24th hour column name variation
    if '24:00:00' in df.columns:
        rename_dict['24:00:00'] = 'Hour 24'
    elif '24:00' in df.columns:
        rename_dict['24:00'] = 'Hour 24'
    
    df = df.rename(columns=rename_dict)
    
    # 3. Define target columns verbatim
    target_columns = ['date'] + [f'Hour {i}' for i in range(1, 25)]
    
    # 4. Return the transformed dataframe
    return df[target_columns]