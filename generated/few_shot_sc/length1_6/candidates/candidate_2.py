import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse Date and format as 'cst'
    # Source format: M/D/YYYY (e.g., '1/1/2014')
    # Target format: %a %m/%d/%Y (e.g., 'Wed 01/01/2014')
    dt = pd.to_datetime(df['Date'])
    df['cst'] = dt.dt.strftime('%a %m/%d/%Y')
    
    # 2. Rename hourly columns from 'Hr X' to 'X:00'
    rename_dict = {f'Hr {i}': f'{i}:00' for i in range(1, 25)}
    df = df.rename(columns=rename_dict)
    
    # 3. Define target columns
    target_columns = ['cst'] + [f'{i}:00' for i in range(1, 25)]
    
    # 4. Return the transformed DataFrame with only target columns
    return df[target_columns]