import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse Date and format as 'Day Month/Day/Year' (e.g., 'Wed 01/01/2014')
    dt = pd.to_datetime(df['Date'])
    df['cst'] = dt.dt.strftime('%a %m/%d/%Y')
    
    # 2. Rename hourly columns from 'Hr X' to 'X:00'
    rename_dict = {}
    for i in range(1, 25):
        rename_dict[f'Hr {i}'] = f'{i}:00'
    
    df = df.rename(columns=rename_dict)
    
    # 3. Define target columns in correct order
    target_cols = ['cst'] + [f'{i}:00' for i in range(1, 25)]
    
    # 4. Return the transformed dataframe with exact target schema
    return df[target_cols]