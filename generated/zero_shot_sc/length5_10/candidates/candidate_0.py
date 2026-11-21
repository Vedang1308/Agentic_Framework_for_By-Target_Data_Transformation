import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    # Start with a copy of the source dataframe to avoid modifying the original
    df = source.copy()
    
    # Define the mapping from source column names to target column names
    rename_map = {}
    
    # Map 'Date' to 'date'
    rename_map['Date'] = 'date'
    
    # Map '1:00' through '23:00' to 'value1' through 'value23'
    for hour in range(1, 24):
        rename_map[f"{hour}:00"] = f"value{hour}"
        
    # Map '24:00:00' to 'value24'
    rename_map["24:00:00"] = "value24"
    
    # Apply the renaming
    df = df.rename(columns=rename_map)
    
    # Define the exact target column order
    target_columns = [
        'date', 'value1', 'value2', 'value3', 'value4', 'value5', 'value6', 
        'value7', 'value8', 'value9', 'value10', 'value11', 'value12', 'value13', 
        'value14', 'value15', 'value16', 'value17', 'value18', 'value19', 'value20', 
        'value21', 'value22', 'value23', 'value24'
    ]
    
    # Select and order columns according to target schema
    return df[target_columns]