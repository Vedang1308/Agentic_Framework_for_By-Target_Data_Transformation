import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the date column and format it to the target format
    # Source format: M/D/YYYY (e.g., '7/3/2011')
    # Target format: YYYY-MM-DD 00:00:00 (e.g., '2011-01-01 00:00:00')
    df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # 2. Rename value columns to Hour columns
    rename_dict = {f'value{i}': f'Hour {i}' for i in range(1, 25)}
    df = df.rename(columns=rename_dict)
    
    # 3. Sort by date to match the chronological order in the target
    df = df.sort_values(by='date').reset_index(drop=True)
    
    # 4. Define target columns
    target_columns = ['date'] + [f'Hour {i}' for i in range(1, 25)]
    
    # 5. Return the transformed dataframe with only the target columns
    return df[target_columns]