import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    # Create a copy to avoid modifying the original source
    df = source.copy()
    
    # 1. Parse and format the date column
    # Source format: '%m/%d/%Y' (e.g., '7/3/2011')
    # Target format: '%Y-%m-%d %H:%M:%S' (e.g., '2011-01-01 00:00:00')
    df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y')
    df['date'] = df['date'].dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # 2. Rename value columns to Hour columns
    # Map value1 -> Hour 1, value2 -> Hour 2, ..., value24 -> Hour 24
    rename_mapping = {}
    for i in range(1, 25):
        rename_mapping[f'value{i}'] = f'Hour {i}'
    
    df.rename(columns=rename_mapping, inplace=True)
    
    # 3. Define the target column order
    target_columns = ['date'] + [f'Hour {i}' for i in range(1, 25)]
    
    # 4. Select and order the columns
    # Ensure all required columns are present
    df = df[target_columns]
    
    return df