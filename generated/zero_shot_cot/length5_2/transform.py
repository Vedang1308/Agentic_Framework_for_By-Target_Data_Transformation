import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    # Define target column names
    target_columns = ['date', 'value1', 'value2', 'value3', 'value4', 'value5', 'value6', 'value7', 'value8', 'value9', 'value10', 'value11', 'value12', 'value13', 'value14', 'value15', 'value16', 'value17', 'value18', 'value19', 'value20', 'value21', 'value22', 'value23', 'value24']
    
    # Create a copy of the source to avoid modifying the original
    df = source.copy()
    
    # Parse the 'CST' column to datetime and format it as 'MM/DD/YYYY'
    # The source format is '%a %m/%d/%Y' (e.g., 'Sat 12/01/2012')
    df['date'] = pd.to_datetime(df['CST'], format='%a %m/%d/%Y').dt.strftime('%m/%d/%Y')
    
    # Define the mapping from source value columns to target value columns
    # Source columns: '1:00', '2:00', ..., '23:00', '24:00:00'
    # Target columns: 'value1', 'value2', ..., 'value23', 'value24'
    source_value_cols = [f'{i}:00' if i < 24 else '24:00:00' for i in range(1, 25)]
    target_value_cols = [f'value{i}' for i in range(1, 25)]
    
    # Create a rename dictionary
    rename_dict = dict(zip(source_value_cols, target_value_cols))
    
    # Rename the value columns
    df = df.rename(columns=rename_dict)
    
    # Select only the target columns in the correct order
    # We drop the original 'CST' column as it's not in the target
    df = df[target_columns]
    
    return df[target_columns]