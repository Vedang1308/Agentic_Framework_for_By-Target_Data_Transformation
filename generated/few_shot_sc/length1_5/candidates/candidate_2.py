import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the 'date' column and format it for 'cst'
    # Source format: %m/%d/%Y (e.g., '7/3/2015')
    # Target format: %a %m/%d/%Y (e.g., 'Thu 01/01/2015')
    dt = pd.to_datetime(df['date'])
    df['cst'] = dt.dt.strftime('%a %m/%d/%Y')
    
    # 2. Rename hour columns from 'Hour X' to 'X:00'
    rename_dict = {}
    for i in range(1, 25):
        rename_dict[f'Hour {i}'] = f'{i}:00'
    
    df = df.rename(columns=rename_dict)
    
    # 3. Define target columns verbatim
    target_cols = ['cst'] + [f'{i}:00' for i in range(1, 25)]
    
    # 4. Return the dataframe with only the target columns
    return df[target_cols]