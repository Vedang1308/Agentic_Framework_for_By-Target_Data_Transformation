import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Transform the date column
    # Source format: 'Sat 12/01/2012' (%a %m/%d/%Y)
    # Target format: '04/01/2009' (%m/%d/%Y)
    dt = pd.to_datetime(df['CST'], format='%a %m/%d/%Y')
    df['date'] = dt.dt.strftime('%m/%d/%Y')
    
    # 2. Rename value columns
    # Source: '1:00', '2:00', ..., '23:00', '24:00:00'
    # Target: 'value1', 'value2', ..., 'value23', 'value24'
    rename_dict = {}
    for i in range(1, 24):
        rename_dict[f'{i}:00'] = f'value{i}'
    # Handle the 24th hour specifically as it has seconds in the source name
    rename_dict['24:00:00'] = 'value24'
    
    df = df.rename(columns=rename_dict)
    
    # 3. Define target columns verbatim
    target_columns = ['date'] + [f'value{i}' for i in range(1, 25)]
    
    # 4. Return the transformed dataframe with selected columns
    return df[target_columns]