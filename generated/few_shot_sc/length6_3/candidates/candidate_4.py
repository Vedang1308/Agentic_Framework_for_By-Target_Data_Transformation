import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse and format the date column
    # Source format: '7/3/2011' (M/D/YYYY)
    # Target format: '2011-01-01 00:00:00' (YYYY-MM-DD HH:MM:SS)
    dt_parsed = pd.to_datetime(df['date'])
    df['Date'] = dt_parsed.dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # 2. Rename value columns to Hr columns
    rename_dict = {}
    for i in range(1, 25):
        rename_dict[f'value{i}'] = f'Hr {i}'
    
    df = df.rename(columns=rename_dict)
    
    # 3. Define target columns
    target_columns = ['Date'] + [f'Hr {i}' for i in range(1, 25)]
    
    # 4. Select and return only the target columns
    # Sorting by Date to match typical target presentation, though not strictly required if order is preserved
    df = df.sort_values(by='Date').reset_index(drop=True)
    
    return df[target_columns]