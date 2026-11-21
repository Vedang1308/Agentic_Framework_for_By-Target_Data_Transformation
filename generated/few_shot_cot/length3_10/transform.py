import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Transform the Date column
    # Source format: 'Thu 10/01/2009' (%a %m/%d/%Y)
    # Target format: '01/01/2003' (%m/%d/%Y)
    # Extract the date part (last token after splitting by space)
    date_str = df['Date'].str.split(' ').str[-1]
    # Parse to datetime
    dt = pd.to_datetime(date_str, format='%m/%d/%Y')
    # Format to target string
    df['date'] = dt.dt.strftime('%m/%d/%Y')
    
    # 2. Rename hourly columns
    # Source: '1:00', '2:00', ..., '23:00', '24:00:00'
    # Target: 'Hour 1', 'Hour 2', ..., 'Hour 23', 'Hour 24'
    rename_dict = {}
    for i in range(1, 24):
        rename_dict[f'{i}:00'] = f'Hour {i}'
    # Handle the 24th hour specifically as it has seconds in source
    rename_dict['24:00:00'] = 'Hour 24'
    
    df = df.rename(columns=rename_dict)
    
    # 3. Define target columns and select them
    target_columns = ['date'] + [f'Hour {i}' for i in range(1, 25)]
    
    return df[target_columns]