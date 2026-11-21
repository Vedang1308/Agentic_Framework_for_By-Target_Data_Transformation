import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the CST column to datetime
    # Format in source: '%a %m/%d/%Y' (e.g., 'Sat 12/01/2012')
    df['datetime'] = pd.to_datetime(df['CST'])
    
    # 2. Create the 'date' column with format '%m/%d/%Y'
    df['date'] = df['datetime'].dt.strftime('%m/%d/%Y')
    
    # 3. Rename hourly columns
    # Source: '1:00', ..., '23:00', '24:00:00'
    # Target: 'Hour 1', ..., 'Hour 23', 'Hour 24'
    rename_dict = {}
    for i in range(1, 24):
        rename_dict[f'{i}:00'] = f'Hour {i}'
    rename_dict['24:00:00'] = 'Hour 24'
    
    df = df.rename(columns=rename_dict)
    
    # 4. Define target columns verbatim
    target_columns = ['date'] + [f'Hour {i}' for i in range(1, 25)]
    
    # 5. Select and return
    return df[target_columns]