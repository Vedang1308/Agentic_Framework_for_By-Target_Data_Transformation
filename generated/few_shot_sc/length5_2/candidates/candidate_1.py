import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the CST column and format as MM/DD/YYYY
    # Source format: 'Sat 12/01/2012' (%a %m/%d/%Y)
    # Target format: '04/01/2009' (%m/%d/%Y)
    dt = pd.to_datetime(df['CST'])
    df['date'] = dt.dt.strftime('%m/%d/%Y')
    
    # 2. Rename hourly columns to value1..value24
    rename_dict = {}
    for i in range(1, 24):
        rename_dict[f'{i}:00'] = f'value{i}'
    # Handle the 24th hour which has a different format in source
    rename_dict['24:00:00'] = 'value24'
    
    df = df.rename(columns=rename_dict)
    
    # 3. Define target columns verbatim
    target_columns = ['date'] + [f'value{i}' for i in range(1, 25)]
    
    # 4. Return only the target columns
    return df[target_columns]