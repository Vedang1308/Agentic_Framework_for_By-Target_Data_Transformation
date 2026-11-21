import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse and format the date column
    # Source CST format: 'Sat 12/01/2012' -> Target date format: '04/01/2009'
    # Extract the date part (last element after splitting by space)
    date_str = df['CST'].str.split(' ').str[-1]
    dt = pd.to_datetime(date_str, format='%m/%d/%Y')
    df['date'] = dt.dt.strftime('%m/%d/%Y')
    
    # 2. Rename hourly columns
    # Source: '1:00', '2:00', ..., '24:00:00'
    # Target: 'Hour 1', 'Hour 2', ..., 'Hour 24'
    rename_dict = {}
    for i in range(1, 24):
        rename_dict[f'{i}:00'] = f'Hour {i}'
    # Handle the last hour specifically as it has seconds in source
    rename_dict['24:00:00'] = 'Hour 24'
    
    df = df.rename(columns=rename_dict)
    
    # 3. Define target columns verbatim
    target_columns = ['date'] + [f'Hour {i}' for i in range(1, 25)]
    
    # 4. Return the transformed dataframe
    return df[target_columns]