import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # Rename the Date column to date
    df = df.rename(columns={'Date': 'date'})
    
    # Create a mapping for the hourly columns
    # Source: '1:00', '2:00', ..., '23:00', '24:00:00'
    # Target: 'value1', 'value2', ..., 'value23', 'value24'
    rename_dict = {}
    
    # Map hours 1 to 23
    for i in range(1, 24):
        rename_dict[f'{i}:00'] = f'value{i}'
        
    # Map hour 24 specifically as '24:00:00' in source
    rename_dict['24:00:00'] = 'value24'
    
    df = df.rename(columns=rename_dict)
    
    # Define the target columns in the exact required order
    target_columns = ['date'] + [f'value{i}' for i in range(1, 25)]
    
    # Select only the target columns
    return df[target_columns]