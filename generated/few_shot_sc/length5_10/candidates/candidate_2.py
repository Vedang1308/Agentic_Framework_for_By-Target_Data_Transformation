import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Handle the date column
    # Source 'Date' format is '%a %m/%d/%Y' (e.g., 'Thu 10/01/2009')
    # Target 'date' format is '%a %m/%d/%Y' (e.g., 'Wed 01/01/2003')
    # We parse and re-format to ensure consistency and correct weekday abbreviation.
    dt = pd.to_datetime(df['Date'], format='%a %m/%d/%Y')
    df['date'] = dt.dt.strftime('%a %m/%d/%Y')
    
    # 2. Rename the hourly columns
    # Source columns: '1:00', '2:00', ..., '23:00', '24:00:00'
    # Target columns: 'value1', 'value2', ..., 'value23', 'value24'
    
    rename_dict = {}
    for i in range(1, 24):
        rename_dict[f'{i}:00'] = f'value{i}'
    
    # Handle the 24th hour specifically as it might have ':00:00' suffix
    if '24:00:00' in df.columns:
        rename_dict['24:00:00'] = 'value24'
    elif '24:00' in df.columns:
        rename_dict['24:00'] = 'value24'
        
    df = df.rename(columns=rename_dict)
    
    # 3. Define target columns and return
    target_columns = ['date'] + [f'value{i}' for i in range(1, 25)]
    
    return df[target_columns]