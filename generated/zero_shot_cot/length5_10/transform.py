import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # Define the target column names in the required order
    target_columns = ['date'] + [f'value{i}' for i in range(1, 25)]
    
    # Create a mapping from source column names to target column names
    rename_map = {'Date': 'date'}
    
    # Map time columns 1:00 to 23:00 to value1 to value23
    for i in range(1, 24):
        rename_map[f'{i}:00'] = f'value{i}'
        
    # Map the last time column 24:00:00 to value24
    rename_map['24:00:00'] = 'value24'
    
    # Rename the columns
    df = df.rename(columns=rename_map)
    
    # Select only the target columns in the correct order
    # This also implicitly drops any columns not in target_columns (like 'Segment')
    df = df[target_columns]
    
    return df[target_columns]