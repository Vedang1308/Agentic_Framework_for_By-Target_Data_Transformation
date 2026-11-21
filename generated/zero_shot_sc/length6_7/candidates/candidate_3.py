import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # Define the target column names verbatim
    target_columns = [
        'Date', 'Hr 1', 'Hr 2', 'Hr 3', 'Hr 4', 'Hr 5', 'Hr 6', 'Hr 7', 'Hr 8', 
        'Hr 9', 'Hr 10', 'Hr 11', 'Hr 12', 'Hr 13', 'Hr 14', 'Hr 15', 'Hr 16', 
        'Hr 17', 'Hr 18', 'Hr 19', 'Hr 20', 'Hr 21', 'Hr 22', 'Hr 23', 'Hr 24'
    ]
    
    # Create a mapping from source hourly columns to target hourly columns
    # Source columns: '1:00', '2:00', ..., '23:00', '24:00:00'
    # Target columns: 'Hr 1', 'Hr 2', ..., 'Hr 23', 'Hr 24'
    rename_map = {}
    
    # Map 1:00 through 23:00
    for i in range(1, 24):
        rename_map[f'{i}:00'] = f'Hr {i}'
        
    # Map 24:00:00 specifically
    rename_map['24:00:00'] = 'Hr 24'
    
    # Apply the rename
    df = source.rename(columns=rename_map)
    
    # Select only the target columns in the correct order
    # Note: 'Date' is already in the source and doesn't need renaming
    result = df[target_columns]
    
    return result