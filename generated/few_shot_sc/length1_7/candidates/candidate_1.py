import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # Rename Date to cst
    df = df.rename(columns={'Date': 'cst'})
    
    # Rename 24:00:00 to 24:00
    if '24:00:00' in df.columns:
        df = df.rename(columns={'24:00:00': '24:00'})
    
    # Define target columns verbatim
    target_columns = ['cst'] + [f'{i}:00' for i in range(1, 25)]
    
    # Select only the required columns
    return df[target_columns]