import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # Define the target column names verbatim
    target_columns = [
        'date', 'Hour 1', 'Hour 2', 'Hour 3', 'Hour 4', 'Hour 5', 'Hour 6', 
        'Hour 7', 'Hour 8', 'Hour 9', 'Hour 10', 'Hour 11', 'Hour 12', 
        'Hour 13', 'Hour 14', 'Hour 15', 'Hour 16', 'Hour 17', 'Hour 18', 
        'Hour 19', 'Hour 20', 'Hour 21', 'Hour 22', 'Hour 23', 'Hour 24'
    ]
    
    # Create a copy to avoid modifying the original
    df = source.copy()
    
    # Step 1: Transform the 'CST' column to 'date'
    # Source format: 'Sat 12/01/2012'
    # Target format: '12/01/2012'
    # We can split by space and take the last part, or parse datetime.
    # Splitting is robust given the fixed format 'Day MM/DD/YYYY'
    if 'CST' in df.columns:
        # Extract the date part (second element after splitting by space)
        # This handles cases where the day name might vary in length
        df['date'] = df['CST'].apply(lambda x: x.split()[-1] if isinstance(x, str) else x)
    else:
        # Fallback if column name is slightly different, though schema says 'CST'
        pass
        
    # Step 2: Map source hour columns to target hour columns
    # Source columns: '1:00', '2:00', ..., '23:00', '24:00:00'
    # Target columns: 'Hour 1', 'Hour 2', ..., 'Hour 23', 'Hour 24'
    
    rename_map = {'CST': 'date'}
    
    # Generate mapping for hours 1-23
    for i in range(1, 24):
        rename_map[f'{i}:00'] = f'Hour {i}'
        
    # Map the 24th hour specifically
    rename_map['24:00:00'] = 'Hour 24'
    
    # Apply renaming
    df = df.rename(columns=rename_map)
    
    # Step 3: Ensure correct column order and return
    # Filter to only include the target columns to ensure exact schema match
    # and remove any extra columns if present
    if all(col in df.columns for col in target_columns):
        return df[target_columns]
    else:
        # Debugging help if columns are missing
        missing = set(target_columns) - set(df.columns)
        raise ValueError(f"Missing columns in transformed dataframe: {missing}")