import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse and format the date column
    # Source format: '%m/%d/%Y' (e.g., '7/3/2011')
    # Target format: '%Y-%m-%d %H:%M:%S' (e.g., '2011-01-01 00:00:00')
    df['Date'] = pd.to_datetime(df['date'], format='%m/%d/%Y').dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # 2. Rename value columns to Hr columns
    # Map value1 -> Hr 1, value2 -> Hr 2, ..., value24 -> Hr 24
    rename_map = {f'value{i}': f'Hr {i}' for i in range(1, 25)}
    df = df.rename(columns=rename_map)
    
    # 3. Define the target columns in the correct order
    target_columns = ['Date', 'Hr 1', 'Hr 2', 'Hr 3', 'Hr 4', 'Hr 5', 'Hr 6', 'Hr 7', 'Hr 8', 'Hr 9', 'Hr 10', 'Hr 11', 'Hr 12', 'Hr 13', 'Hr 14', 'Hr 15', 'Hr 16', 'Hr 17', 'Hr 18', 'Hr 19', 'Hr 20', 'Hr 21', 'Hr 22', 'Hr 23', 'Hr 24']
    
    # 4. Select only the required columns
    df = df[target_columns]
    
    # 5. Sort by Date to ensure chronological order as seen in the target sample
    df = df.sort_values(by='Date').reset_index(drop=True)
    
    return df[target_columns]