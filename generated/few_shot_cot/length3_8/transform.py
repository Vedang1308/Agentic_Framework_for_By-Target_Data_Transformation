import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse and format the date column
    # Source format: 'Sat 12/01/2012' (%a %m/%d/%Y)
    # Target format: '04/01/2009' (%m/%d/%Y)
    dt = pd.to_datetime(df['CST'], format='%a %m/%d/%Y')
    df['date'] = dt.dt.strftime('%m/%d/%Y')
    
    # 2. Rename hourly columns
    # Source: '1:00', '2:00', ..., '23:00', '24:00:00'
    # Target: 'Hour 1', 'Hour 2', ..., 'Hour 23', 'Hour 24'
    rename_dict = {}
    for i in range(1, 24):
        rename_dict[f'{i}:00'] = f'Hour {i}'
    rename_dict['24:00:00'] = 'Hour 24'
    
    df = df.rename(columns=rename_dict)
    
    # 3. Define target columns in exact order
    target_columns = ['date'] + [f'Hour {i}' for i in range(1, 25)]
    
    # 4. Return the transformed dataframe with only target columns
    return df[target_columns]