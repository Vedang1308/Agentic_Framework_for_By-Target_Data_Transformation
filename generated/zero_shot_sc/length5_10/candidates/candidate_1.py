import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    # Create a copy to avoid modifying the original source
    df = source.copy()
    
    # Define the target column names
    target_columns = [
        'date', 'value1', 'value2', 'value3', 'value4', 'value5', 'value6', 
        'value7', 'value8', 'value9', 'value10', 'value11', 'value12', 
        'value13', 'value14', 'value15', 'value16', 'value17', 'value18', 
        'value19', 'value20', 'value21', 'value22', 'value23', 'value24'
    ]
    
    # Create a mapping dictionary for the hourly columns
    # Source columns: '1:00', '2:00', ..., '23:00', '24:00:00'
    # Target columns: 'value1', 'value2', ..., 'value23', 'value24'
    rename_mapping = {}
    
    # Map 'Date' to 'date'
    rename_mapping['Date'] = 'date'
    
    # Map hourly columns
    for i in range(1, 24):
        source_col = f"{i}:00"
        target_col = f"value{i}"
        rename_mapping[source_col] = target_col
        
    # Handle the last column specifically as it has a different format '24:00:00'
    rename_mapping['24:00:00'] = 'value24'
    
    # Apply the renaming
    df = df.rename(columns=rename_mapping)
    
    # Select only the target columns in the correct order
    # This also effectively drops the 'Segment' column and any others not in the target list
    df = df[target_columns]
    
    return df[target_columns]