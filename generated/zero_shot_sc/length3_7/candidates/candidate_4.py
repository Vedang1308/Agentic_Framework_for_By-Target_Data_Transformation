import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    # Create a copy to avoid modifying the original source
    df = source.copy()
    
    # Define the target column names
    target_columns = [
        'date', 'Hour 1', 'Hour 2', 'Hour 3', 'Hour 4', 'Hour 5', 'Hour 6', 
        'Hour 7', 'Hour 8', 'Hour 9', 'Hour 10', 'Hour 11', 'Hour 12', 
        'Hour 13', 'Hour 14', 'Hour 15', 'Hour 16', 'Hour 17', 'Hour 18', 
        'Hour 19', 'Hour 20', 'Hour 21', 'Hour 22', 'Hour 23', 'Hour 24'
    ]
    
    # Step 1: Rename the 'Date' column to 'date'
    df = df.rename(columns={'Date': 'date'})
    
    # Step 2: Format the date column to ensure leading zeros (MM/DD/YYYY)
    # The source format is m/d/Y, target is MM/DD/YYYY
    df['date'] = pd.to_datetime(df['date']).dt.strftime('%m/%d/%Y')
    
    # Step 3: Rename numeric columns 1-24 to 'Hour 1'-'Hour 24'
    rename_dict = {str(i): f'Hour {i}' for i in range(1, 25)}
    df = df.rename(columns=rename_dict)
    
    # Step 4: Select only the target columns in the correct order
    # This also drops any columns not in the target schema (like 'Class')
    df = df[target_columns]
    
    # Step 5: Ensure the column order matches the target exactly
    # (Already done by selecting with target_columns list, but explicit sort by name isn't needed 
    # since we selected in order. However, to be safe against any previous ordering issues:)
    df = df[target_columns]
    
    return df