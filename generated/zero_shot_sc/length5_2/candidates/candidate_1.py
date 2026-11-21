import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # Define the target column names exactly as required
    target_columns = [
        'date', 'value1', 'value2', 'value3', 'value4', 'value5', 'value6', 
        'value7', 'value8', 'value9', 'value10', 'value11', 'value12', 
        'value13', 'value14', 'value15', 'value16', 'value17', 'value18', 
        'value19', 'value20', 'value21', 'value22', 'value23', 'value24'
    ]
    
    # 1. Process the 'date' column
    # The source 'CST' column is in format 'Day MM/DD/YYYY' (e.g., 'Sat 12/01/2012')
    # The target 'date' column requires 'MM/DD/YYYY'
    # We can extract the date part by splitting the string and taking the last element
    df = source.copy()
    df['date'] = df['CST'].str.split().str[-1]
    
    # 2. Map the hourly value columns to the target value columns
    # Source columns: '1:00', '2:00', ..., '23:00', '24:00:00'
    # Target columns: 'value1', 'value2', ..., 'value23', 'value24'
    
    # Create a mapping dictionary
    col_mapping = {}
    for i in range(1, 24):
        col_mapping[f'{i}:00'] = f'value{i}'
    col_mapping['24:00:00'] = 'value24'
    
    # Rename the columns
    df = df.rename(columns=col_mapping)
    
    # 3. Select and reorder the columns to match the target schema
    # We drop the original 'CST' column and any other non-target columns if present
    # Ensure we only return the columns specified in target_columns
    result_df = df[target_columns]
    
    return result_df