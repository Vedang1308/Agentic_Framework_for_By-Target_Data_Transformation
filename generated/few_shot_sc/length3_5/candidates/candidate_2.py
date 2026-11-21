import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse and format the date column
    # Source format is like '7/3/2011' (%m/%d/%Y)
    # Target format is '2011-01-01 00:00:00' (%Y-%m-%d %H:%M:%S)
    dt = pd.to_datetime(df['date'])
    df['date'] = dt.dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # 2. Rename value columns to Hour columns
    rename_dict = {f'value{i}': f'Hour {i}' for i in range(1, 25)}
    df = df.rename(columns=rename_dict)
    
    # 3. Define target columns in the exact required order
    target_cols = ['date'] + [f'Hour {i}' for i in range(1, 25)]
    
    # 4. Select and return the target columns
    return df[target_cols]