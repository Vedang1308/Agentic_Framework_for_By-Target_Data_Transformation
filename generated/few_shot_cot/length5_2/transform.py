import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the CST column to datetime and format as 'MM/DD/YYYY'
    # The source format is '%a %m/%d/%Y' (e.g., 'Sat 12/01/2012')
    # We extract the date part or parse directly. pd.to_datetime handles '%a %m/%d/%Y' well.
    dt = pd.to_datetime(df['CST'], format='%a %m/%d/%Y')
    df['date'] = dt.dt.strftime('%m/%d/%Y')
    
    # 2. Rename the hourly columns to value1...value24
    rename_dict = {}
    for i in range(1, 24):
        rename_dict[f'{i}:00'] = f'value{i}'
    # Handle the 24th hour specifically as it has seconds in the source name
    rename_dict['24:00:00'] = 'value24'
    
    df = df.rename(columns=rename_dict)
    
    # 3. Define the target columns in the correct order
    target_columns = ['date'] + [f'value{i}' for i in range(1, 25)]
    
    # 4. Return the DataFrame with only the target columns
    return df[target_columns]