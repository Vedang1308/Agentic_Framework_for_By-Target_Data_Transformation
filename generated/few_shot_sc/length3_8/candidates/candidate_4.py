import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Process Date Column
    # Source 'CST' is like 'Sat 12/01/2012'. We need just the date part '12/01/2012'.
    # Split by space and take the last element.
    date_part = df['CST'].str.split(' ').str[-1]
    dt = pd.to_datetime(date_part, format='%m/%d/%Y')
    df['date'] = dt.dt.strftime('%m/%d/%Y')
    
    # 2. Rename Hour Columns
    # Source columns: '1:00', '2:00', ..., '23:00', '24:00:00'
    # Target columns: 'Hour 1', 'Hour 2', ..., 'Hour 23', 'Hour 24'
    
    rename_dict = {}
    for i in range(1, 24):
        rename_dict[f'{i}:00'] = f'Hour {i}'
    rename_dict['24:00:00'] = 'Hour 24'
    
    df = df.rename(columns=rename_dict)
    
    # 3. Define Target Columns
    target_columns = ['date'] + [f'Hour {i}' for i in range(1, 25)]
    
    # 4. Return Result
    return df[target_columns]