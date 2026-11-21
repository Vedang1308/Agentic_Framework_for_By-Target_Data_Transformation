import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # Define the target column names verbatim
    target_columns = [
        'date', 'value1', 'value2', 'value3', 'value4', 'value5', 'value6', 
        'value7', 'value8', 'value9', 'value10', 'value11', 'value12', 'value13', 
        'value14', 'value15', 'value16', 'value17', 'value18', 'value19', 'value20', 
        'value21', 'value22', 'value23', 'value24'
    ]
    
    # Create a copy to avoid modifying the original source
    df = source.copy()
    
    # Drop the 'Segment' column as it is not in the target schema
    if 'Segment' in df.columns:
        df = df.drop(columns=['Segment'])
    
    # Define the mapping from source time columns to target value columns
    # Source columns are '1:00', '2:00', ..., '23:00', '24:00:00'
    # Target columns are 'value1', 'value2', ..., 'value23', 'value24'
    
    rename_map = {}
    
    # Map Date to date
    rename_map['Date'] = 'date'
    
    # Map 1:00 to 23:00 to value1 to value23
    for i in range(1, 24):
        rename_map[f'{i}:00'] = f'value{i}'
        
    # Map 24:00:00 to value24
    rename_map['24:00:00'] = 'value24'
    
    # Apply the renaming
    df = df.rename(columns=rename_map)
    
    # Select and reorder columns to match the target schema exactly
    return df[target_columns]