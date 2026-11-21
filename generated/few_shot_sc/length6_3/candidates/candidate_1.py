import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse and Format the Date Column
    # Source format: '%m/%d/%Y' (e.g., '7/3/2011')
    # Target format: '%Y-%m-%d %H:%M:%S' (e.g., '2011-07-03 00:00:00')
    df['Date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # 2. Rename Value Columns
    # Map 'value1'...'value24' to 'Hr 1'...'Hr 24'
    rename_dict = {}
    for i in range(1, 25):
        rename_dict[f'value{i}'] = f'Hr {i}'
    
    df = df.rename(columns=rename_dict)
    
    # 3. Define Target Columns
    target_columns = ['Date'] + [f'Hr {i}' for i in range(1, 25)]
    
    # 4. Return the DataFrame with only the target columns
    return df[target_columns]