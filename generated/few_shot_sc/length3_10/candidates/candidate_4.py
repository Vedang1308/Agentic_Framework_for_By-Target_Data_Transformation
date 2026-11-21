import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Transform the Date column
    # Source format: 'Thu 10/01/2009' (%a %m/%d/%Y)
    # Target format: '01/01/2003' (%m/%d/%Y)
    # We can parse the datetime and then format it, or simply strip the day name.
    # Parsing is robust.
    dt = pd.to_datetime(df['Date'])
    df['date'] = dt.dt.strftime('%m/%d/%Y')
    
    # 2. Rename hourly columns
    # Source: '1:00', '2:00', ..., '23:00', '24:00:00'
    # Target: 'Hour 1', 'Hour 2', ..., 'Hour 23', 'Hour 24'
    rename_map = {}
    for i in range(1, 24):
        rename_map[f'{i}:00'] = f'Hour {i}'
    rename_map['24:00:00'] = 'Hour 24'
    
    df = df.rename(columns=rename_map)
    
    # 3. Define target columns in order
    target_columns = ['date'] + [f'Hour {i}' for i in range(1, 25)]
    
    # 4. Return the transformed dataframe with only target columns
    return df[target_columns]