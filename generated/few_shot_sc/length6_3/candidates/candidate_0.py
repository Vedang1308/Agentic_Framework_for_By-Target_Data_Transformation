import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the source date column and format it to the target format
    # Source format: '%m/%d/%Y' (e.g., '7/3/2011')
    # Target format: '%Y-%m-%d %H:%M:%S' (e.g., '2011-01-01 00:00:00')
    df['Date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # 2. Rename value columns to Hr columns
    # value1 -> Hr 1, value2 -> Hr 2, ..., value24 -> Hr 24
    rename_dict = {f'value{i}': f'Hr {i}' for i in range(1, 25)}
    df = df.rename(columns=rename_dict)
    
    # 3. Define the target columns in the correct order
    target_columns = ['Date'] + [f'Hr {i}' for i in range(1, 25)]
    
    # 4. Select only the required columns
    df = df[target_columns]
    
    # 5. Sort by Date to ensure chronological order, matching the target sample style
    df = df.sort_values('Date').reset_index(drop=True)
    
    return df[target_columns]