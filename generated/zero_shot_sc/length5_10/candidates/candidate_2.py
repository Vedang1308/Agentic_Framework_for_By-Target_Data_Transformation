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
    
    # Create a mapping from source columns to target columns
    # Source columns: '1:00', '2:00', ..., '23:00', '24:00:00'
    # Target columns: 'value1', 'value2', ..., 'value23', 'value24'
    rename_map = {
        'Date': 'date'
    }
    
    # Map hourly columns
    for i in range(1, 24):
        rename_map[f'{i}:00'] = f'value{i}'
    
    # Handle the 24th hour specifically as it has a different format in source
    rename_map['24:00:00'] = 'value24'
    
    # Rename columns
    df = source.rename(columns=rename_map)
    
    # Select only the required target columns in the correct order
    # Note: We assume all source columns needed are present.
    # We drop 'Segment' implicitly by not selecting it.
    result_df = df[target_columns]
    
    return result_df