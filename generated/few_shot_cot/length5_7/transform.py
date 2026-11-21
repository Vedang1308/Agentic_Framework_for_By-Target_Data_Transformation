import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the 'Date' column and format it to 'YYYY-MM-DD HH:MM:SS'
    # The source format is '%m/%d/%Y' (e.g., '7/3/2013')
    # The target format is '%Y-%m-%d %H:%M:%S' (e.g., '2013-01-01 00:00:00')
    df['date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # 2. Rename the numeric columns '1' through '24' to 'value1' through 'value24'
    rename_dict = {str(i): f'value{i}' for i in range(1, 25)}
    df = df.rename(columns=rename_dict)
    
    # 3. Define the target columns in the correct order
    target_columns = ['date'] + [f'value{i}' for i in range(1, 25)]
    
    # 4. Select only the target columns
    df = df[target_columns]
    
    # 5. Sort by date to ensure the order matches the target sample
    df = df.sort_values('date').reset_index(drop=True)
    
    return df[target_columns]