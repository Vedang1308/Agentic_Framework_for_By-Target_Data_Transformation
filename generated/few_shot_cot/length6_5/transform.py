import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse and format the Date column
    # Source format: M/D/YYYY (e.g., '7/3/2013')
    # Target format: MM/DD/YYYY (e.g., '01/01/2013')
    df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%m/%d/%Y')
    
    # 2. Rename hour columns from integers 1-24 to 'Hr 1'-'Hr 24'
    rename_dict = {i: f'Hr {i}' for i in range(1, 25)}
    df = df.rename(columns=rename_dict)
    
    # 3. Define target columns in the correct order
    target_columns = ['Date'] + [f'Hr {i}' for i in range(1, 25)]
    
    # 4. Select and return the target columns
    # Note: The 'Class' column is dropped implicitly by not including it in target_columns
    return df[target_columns]