import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the date column from '%m/%d/%Y' to datetime
    df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y')
    
    # 2. Format the date to '%Y-%m-%d %H:%M:%S' as required by the target 'Date' column
    df['Date'] = df['date'].dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # 3. Rename value columns to Hr columns
    # Mapping value1 -> Hr 1, value2 -> Hr 2, ..., value24 -> Hr 24
    rename_map = {}
    for i in range(1, 25):
        rename_map[f'value{i}'] = f'Hr {i}'
    
    df.rename(columns=rename_map, inplace=True)
    
    # 4. Define the target column order
    target_columns = ['Date', 'Hr 1', 'Hr 2', 'Hr 3', 'Hr 4', 'Hr 5', 'Hr 6', 'Hr 7', 'Hr 8', 'Hr 9', 'Hr 10', 'Hr 11', 'Hr 12', 'Hr 13', 'Hr 14', 'Hr 15', 'Hr 16', 'Hr 17', 'Hr 18', 'Hr 19', 'Hr 20', 'Hr 21', 'Hr 22', 'Hr 23', 'Hr 24']
    
    # 5. Select and return the required columns
    # Note: The source might have other columns (class, Description, etc.) which we ignore.
    return df[target_columns]