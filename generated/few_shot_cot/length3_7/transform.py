import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Rename numeric columns 1-24 to 'Hour 1'-'Hour 24'
    rename_dict = {str(i): f'Hour {i}' for i in range(1, 25)}
    df = df.rename(columns=rename_dict)
    
    # 2. Format the Date column
    # Source 'Date' is object, format '%m/%d/%Y' (e.g., '7/3/2013')
    # Target 'date' is object, format '%m/%d/%Y' (e.g., '01/01/2013')
    # We parse to datetime to ensure consistent formatting (zero-padding)
    df['date'] = pd.to_datetime(df['Date']).dt.strftime('%m/%d/%Y')
    
    # 3. Define target columns
    target_columns = ['date'] + [f'Hour {i}' for i in range(1, 25)]
    
    # 4. Return the DataFrame with only the target columns
    return df[target_columns]