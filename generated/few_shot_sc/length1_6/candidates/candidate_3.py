import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the 'Date' column and format it as 'cst' (%a %m/%d/%Y)
    # Source format is M/D/YYYY, target is e.g., 'Wed 01/01/2014'
    dt = pd.to_datetime(df['Date'])
    df['cst'] = dt.dt.strftime('%a %m/%d/%Y')
    
    # 2. Rename hourly columns from 'Hr 1'...'Hr 24' to '1:00'...'24:00'
    rename_dict = {}
    for i in range(1, 25):
        rename_dict[f'Hr {i}'] = f'{i}:00'
    
    df = df.rename(columns=rename_dict)
    
    # 3. Define target columns verbatim
    target_columns = ['cst'] + [f'{i}:00' for i in range(1, 25)]
    
    # 4. Return the DataFrame with only the target columns
    return df[target_columns]