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
    # Source columns are '1:00', '2:00', ..., '23:00', '24:00:00'
    # Target columns are 'Hr 1', 'Hr 2', ..., 'Hr 23', 'Hr 24'
    col_mapping = {}
    
    # Map hours 1 through 23
    for i in range(1, 24):
        src_col = f"{i}:00"
        tgt_col = f"Hr {i}"
        col_mapping[src_col] = tgt_col
        
    # Map hour 24 (note the specific format '24:00:00' in source)
    col_mapping['24:00:00'] = 'Hr 24'
    
    # Rename the columns
    df = source.rename(columns=col_mapping)
    
    # Select only the required columns in the correct order
    # Note: 'Date' is already present in the source. 'Segment' is ignored.
    df = df[target_columns]
    
    return df[target_columns]