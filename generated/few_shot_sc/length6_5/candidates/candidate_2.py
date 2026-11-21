import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    df = source.copy()
    
    # 1. Parse and format the Date column
    # Convert to datetime to ensure consistent handling
    df['Date'] = pd.to_datetime(df['Date'])
    # Format as MM/DD/YYYY
    df['Date'] = df['Date'].dt.strftime('%m/%d/%Y')
    
    # 2. Rename hourly columns from '1'...'24' to 'Hr 1'...'Hr 24'
    rename_dict = {str(i): f'Hr {i}' for i in range(1, 25)}
    df = df.rename(columns=rename_dict)
    
    # 3. Define target columns
    target_columns = ['Date'] + [f'Hr {i}' for i in range(1, 25)]
    
    # 4. Select and return the target columns
    # Ensure the order matches the target schema
    return df[target_columns]