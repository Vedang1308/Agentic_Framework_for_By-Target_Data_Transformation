import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    # Define the target column names verbatim
    target_columns = [
        'date', 'value1', 'value2', 'value3', 'value4', 'value5', 'value6', 
        'value7', 'value8', 'value9', 'value10', 'value11', 'value12', 
        'value13', 'value14', 'value15', 'value16', 'value17', 'value18', 
        'value19', 'value20', 'value21', 'value22', 'value23', 'value24'
    ]
    
    # Create a mapping for renaming columns
    # Source 'Date' -> Target 'date'
    # Source '1:00' -> 'value1', ..., '24:00:00' -> 'value24'
    rename_map = {'Date': 'date'}
    for i in range(1, 25):
        if i < 24:
            old_col = f"{i}:00"
        else:
            old_col = f"{i}:00:00"
        new_col = f"value{i}"
        rename_map[old_col] = new_col
    
    # Rename the columns
    df = source.rename(columns=rename_map)
    
    # Select only the target columns in the correct order
    # This also effectively drops any columns not in target_columns (like 'Segment')
    df = df[target_columns]
    
    return df[target_columns]