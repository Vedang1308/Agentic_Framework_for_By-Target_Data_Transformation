import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    df = source.copy()
    
    # 1. Parse and format the date column
    # Source CST format: '%a %m/%d/%Y' (e.g., 'Sat 12/01/2012')
    # Target date format: '%m/%d/%Y' (e.g., '12/01/2012')
    # We can parse the whole string or just split. pd.to_datetime handles '%a %m/%d/%Y' well.
    dt = pd.to_datetime(df['CST'], format='%a %m/%d/%Y')
    df['date'] = dt.dt.strftime('%m/%d/%Y')
    
    # 2. Rename the hourly columns
    # Source columns: '1:00', '2:00', ..., '23:00', '24:00:00'
    # Target columns: 'Hour 1', 'Hour 2', ..., 'Hour 23', 'Hour 24'
    rename_dict = {}
    for i in range(1, 24):
        rename_dict[f'{i}:00'] = f'Hour {i}'
    rename_dict['24:00:00'] = 'Hour 24'
    
    df = df.rename(columns=rename_dict)
    
    # 3. Define target columns verbatim
    target_columns = ['date'] + [f'Hour {i}' for i in range(1, 25)]
    
    # 4. Return the transformed dataframe
    return df[target_columns]