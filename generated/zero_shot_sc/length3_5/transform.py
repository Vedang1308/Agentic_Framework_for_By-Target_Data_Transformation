import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # Create a copy to avoid modifying the original
    df = source.copy()
    
    # 1. Parse the date column from '%m/%d/%Y' to datetime
    df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y')
    
    # 2. Define the mapping for value columns to Hour columns
    rename_map = {}
    for i in range(1, 25):
        rename_map[f'value{i}'] = f'Hour {i}'
    
    # 3. Rename the columns
    df = df.rename(columns=rename_map)
    
    # 4. Format the date column to '%Y-%m-%d %H:%M:%S'
    # The target sample shows '2011-01-01 00:00:00'
    df['date'] = df['date'].dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # 5. Define the target column names
    target_columns = ['date'] + [f'Hour {i}' for i in range(1, 25)]
    
    # 6. Select only the required columns
    # Note: If there are duplicate dates in source, we might need to aggregate.
    # However, based on the schema and typical TbT tasks, it's usually 1-to-1.
    # If duplicates exist, taking the first or mean is a common strategy.
    # Given the "182 vs 183" discrepancy, let's check if we need to handle duplicates.
    # If the source has multiple rows for the same date, groupby is needed.
    # Let's assume standard unique dates for now, but add a groupby just in case 
    # to ensure deterministic output if duplicates exist (using mean).
    
    # Check for duplicates in date
    if df['date'].duplicated().any():
        # Group by date and take the mean of numeric columns
        df = df.groupby('date', as_index=False).mean()
        
    # Sort by date to ensure consistent ordering
    df = df.sort_values('date').reset_index(drop=True)
    
    # Return the dataframe with exact target columns
    return df[target_columns]