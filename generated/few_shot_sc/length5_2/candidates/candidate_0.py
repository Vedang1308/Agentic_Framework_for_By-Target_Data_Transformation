import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the CST column and format as MM/DD/YYYY for the 'date' column
    # Source format: '%a %m/%d/%Y' (e.g., 'Sat 12/01/2012')
    dt = pd.to_datetime(df['CST'], format='%a %m/%d/%Y')
    df['date'] = dt.dt.strftime('%m/%d/%Y')
    
    # 2. Rename the hourly columns
    # Source columns: '1:00', '2:00', ..., '23:00', '24:00:00'
    # Target columns: 'value1', 'value2', ..., 'value23', 'value24'
    rename_dict = {}
    for i in range(1, 24):
        rename_dict[f'{i}:00'] = f'value{i}'
    rename_dict['24:00:00'] = 'value24'
    
    df = df.rename(columns=rename_dict)
    
    # 3. Define target columns in order
    target_columns = ['date'] + [f'value{i}' for i in range(1, 25)]
    
    # 4. Select and return the columns
    return df[target_columns]