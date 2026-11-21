import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the date column and format it to 'cst' format: '%a %m/%d/%Y'
    # Source 'date' is like '7/3/2015'. Target 'cst' is like 'Thu 01/01/2015'.
    dt = pd.to_datetime(df['date'])
    df['cst'] = dt.dt.strftime('%a %m/%d/%Y')
    
    # 2. Rename hour columns from 'Hour 1', 'Hour 2', ... to '1:00', '2:00', ...
    rename_dict = {}
    for i in range(1, 25):
        rename_dict[f'Hour {i}'] = f'{i}:00'
    
    df = df.rename(columns=rename_dict)
    
    # 3. Define the target columns in the exact order required
    target_cols = ['cst'] + [f'{i}:00' for i in range(1, 25)]
    
    # 4. Return the DataFrame with the specified columns
    return df[target_cols]