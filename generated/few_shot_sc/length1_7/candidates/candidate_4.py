import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # Rename the Date column to cst
    df = df.rename(columns={'Date': 'cst'})
    
    # Rename the 24:00:00 column to 24:00
    # Check if the column exists to avoid errors if schema varies slightly, 
    # though the problem statement implies it exists.
    if '24:00:00' in df.columns:
        df = df.rename(columns={'24:00:00': '24:00'})
    
    # Define the target columns in the correct order
    target_columns = ['cst'] + [f'{i}:00' for i in range(1, 25)]
    
    # Return the DataFrame with only the target columns
    return df[target_columns]