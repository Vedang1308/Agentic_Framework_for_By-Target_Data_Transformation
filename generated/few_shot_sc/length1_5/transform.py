import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Transform the date column 'date' to 'cst' with format '%a %m/%d/%Y'
    # Parse the date column from the source format (e.g., '7/3/2015')
    dt = pd.to_datetime(df['date'])
    # Format as 'Thu 01/01/2015'
    df['cst'] = dt.dt.strftime('%a %m/%d/%Y')
    
    # 2. Rename hourly columns from 'Hour i' to 'i:00'
    rename_dict = {}
    for i in range(1, 25):
        rename_dict[f'Hour {i}'] = f'{i}:00'
    
    df = df.rename(columns=rename_dict)
    
    # 3. Define the target columns verbatim
    target_cols = ['cst'] + [f'{i}:00' for i in range(1, 25)]
    
    # 4. Return the dataframe with only the target columns
    return df[target_cols]