import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    # Define the target column names verbatim
    target_columns = [
        'Date', 'Hr 1', 'Hr 2', 'Hr 3', 'Hr 4', 'Hr 5', 'Hr 6', 'Hr 7', 'Hr 8', 
        'Hr 9', 'Hr 10', 'Hr 11', 'Hr 12', 'Hr 13', 'Hr 14', 'Hr 15', 'Hr 16', 
        'Hr 17', 'Hr 18', 'Hr 19', 'Hr 20', 'Hr 21', 'Hr 22', 'Hr 23', 'Hr 24'
    ]
    
    # Create a copy to avoid modifying the original source
    df = source.copy()
    
    # 1. Parse the date column from '%m/%d/%Y' to datetime
    df['date_parsed'] = pd.to_datetime(df['date'], format='%m/%d/%Y')
    
    # 2. Format the date to '%Y-%m-%d %H:%M:%S' as required by the target
    df['Date'] = df['date_parsed'].dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # 3. Rename value columns to Hr columns
    rename_map = {f'value{i}': f'Hr {i}' for i in range(1, 25)}
    df = df.rename(columns=rename_map)
    
    # 4. Select and order the columns to match the target schema
    # We select 'Date' and the 24 'Hr' columns
    df = df[['Date'] + [f'Hr {i}' for i in range(1, 25)]]
    
    # 5. Ensure correct data types
    # The target schema specifies Date as object (string) and Hr columns as float64
    df['Date'] = df['Date'].astype(str)
    for col in [f'Hr {i}' for i in range(1, 25)]:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        
    # 6. Return the DataFrame with the exact target column names
    return df[target_columns]