import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Transform Date column to 'cst'
    # Parse the date string (format M/D/YYYY) and format as '%a %m/%d/%Y'
    dt = pd.to_datetime(df['Date'])
    df['cst'] = dt.dt.strftime('%a %m/%d/%Y')
    
    # 2. Rename hourly columns
    # Source: 'Hr 1' ... 'Hr 24'
    # Target: '1:00' ... '24:00'
    rename_dict = {f'Hr {i}': f'{i}:00' for i in range(1, 25)}
    df = df.rename(columns=rename_dict)
    
    # 3. Define target columns verbatim
    target_cols = ['cst'] + [f'{i}:00' for i in range(1, 25)]
    
    # 4. Return the selected columns
    return df[target_cols]