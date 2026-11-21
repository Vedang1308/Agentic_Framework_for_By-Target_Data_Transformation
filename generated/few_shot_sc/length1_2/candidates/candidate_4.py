import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the date column
    dt = pd.to_datetime(df['date'])
    
    # 2. Format the date as 'Day MM/DD/YYYY' for the 'cst' column
    # %a = Abbreviated weekday name (e.g., Sat)
    # %m = Zero-padded month
    # %d = Zero-padded day
    # %Y = Four-digit year
    df['cst'] = dt.dt.strftime('%a %m/%d/%Y')
    
    # 3. Rename value columns to hour columns
    rename_dict = {}
    for i in range(1, 25):
        rename_dict[f'value{i}'] = f'{i}:00'
    
    df = df.rename(columns=rename_dict)
    
    # 4. Define target columns in the correct order
    target_columns = ['cst'] + [f'{i}:00' for i in range(1, 25)]
    
    # 5. Return the transformed dataframe with only the target columns
    return df[target_columns]