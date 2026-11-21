import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    # Make a copy to avoid modifying the original source
    df = source.copy()
    
    # 1. Parse and format the date column
    # Source format: %m/%d/%Y (e.g., '7/3/2011')
    # Target format: %Y-%m-%d %H:%M:%S (e.g., '2011-01-01 00:00:00')
    # Target schema indicates 'date' is object type, so we convert to string format
    df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y')
    df['date'] = df['date'].dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # 2. Rename value columns to Hour columns
    # Map value1 -> Hour 1, value2 -> Hour 2, ..., value24 -> Hour 24
    rename_mapping = {f'value{i}': f'Hour {i}' for i in range(1, 25)}
    df = df.rename(columns=rename_mapping)
    
    # 3. Define the target columns in the correct order
    target_columns = ['date'] + [f'Hour {i}' for i in range(1, 25)]
    
    # 4. Select only the required columns
    # This implicitly drops class, Description, analysis, uom
    df = df[target_columns]
    
    # 5. Ensure float types for hour columns (they should already be float64)
    for col in target_columns[1:]:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        
    return df[target_columns]