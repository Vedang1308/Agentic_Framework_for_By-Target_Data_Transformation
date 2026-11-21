import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Transform the Date column
    # Source format: 'Thu 10/01/2009' (%a %m/%d/%Y)
    # Target format: '01/01/2003' (%m/%d/%Y)
    # Extract the date part by splitting on space and taking the last element
    date_str = df['Date'].str.split(' ').str[-1]
    # Parse to datetime and format
    dt = pd.to_datetime(date_str, format='%m/%d/%Y')
    df['date'] = dt.dt.strftime('%m/%d/%Y')
    
    # 2. Rename Hour columns
    # Map '1:00' -> 'Hour 1', ..., '23:00' -> 'Hour 23'
    rename_dict = {}
    for i in range(1, 24):
        rename_dict[f'{i}:00'] = f'Hour {i}'
    
    # Map '24:00:00' -> 'Hour 24'
    rename_dict['24:00:00'] = 'Hour 24'
    
    df = df.rename(columns=rename_dict)
    
    # 3. Select and order target columns
    target_columns = ['date'] + [f'Hour {i}' for i in range(1, 25)]
    
    return df[target_columns]