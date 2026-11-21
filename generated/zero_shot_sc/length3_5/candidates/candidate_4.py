import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # Define target column names verbatim
    target_columns = [
        'date', 'Hour 1', 'Hour 2', 'Hour 3', 'Hour 4', 'Hour 5', 'Hour 6', 
        'Hour 7', 'Hour 8', 'Hour 9', 'Hour 10', 'Hour 11', 'Hour 12', 
        'Hour 13', 'Hour 14', 'Hour 15', 'Hour 16', 'Hour 17', 'Hour 18', 
        'Hour 19', 'Hour 20', 'Hour 21', 'Hour 22', 'Hour 23', 'Hour 24'
    ]
    
    # Select only the necessary columns from source
    # We need 'date' and 'value1' through 'value24'
    cols_to_select = ['date'] + [f'value{i}' for i in range(1, 25)]
    df = source[cols_to_select].copy()
    
    # Convert date column from 'M/D/YYYY' to datetime and then to target format 'YYYY-MM-DD HH:MM:SS'
    df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y').dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Rename value columns to Hour columns
    rename_map = {f'value{i}': f'Hour {i}' for i in range(1, 25)}
    df = df.rename(columns=rename_map)
    
    # Ensure the column order matches the target schema exactly
    return df[target_columns]