import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    # Define the target column names
    target_columns = ['Date'] + [f'Hr {i}' for i in range(1, 25)]
    
    # Create a copy to avoid modifying the original source
    df = source.copy()
    
    # Rename columns 1-24 to Hr 1-Hr 24
    rename_map = {i: f'Hr {i}' for i in range(1, 25)}
    df = df.rename(columns=rename_map)
    
    # Drop the 'Class' column as it is not in the target schema
    if 'Class' in df.columns:
        df = df.drop(columns=['Class'])
    
    # Format the Date column to ensure MM/DD/YYYY with zero-padding
    # Parse dates and then format back to string
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y').dt.strftime('%m/%d/%Y')
    
    # Ensure the columns are in the correct order and only include target columns
    # Check if all target columns exist
    for col in target_columns:
        if col not in df.columns:
            raise ValueError(f"Column {col} not found in transformed dataframe")
            
    df = df[target_columns]
    
    return df