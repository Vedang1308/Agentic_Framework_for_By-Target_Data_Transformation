import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    # Make a copy to avoid modifying the original
    df = source.copy()
    
    # 1. Parse the Date column from 'MM/DD/YYYY' to datetime
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
    
    # 2. Format the Date column to 'YYYY-MM-DD HH:MM:SS' as required by target
    df['date'] = df['Date'].dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # 3. Define the column mapping
    # Source columns 1-24 need to be renamed to value1-value24
    rename_map = {'Date': 'date'}
    for i in range(1, 25):
        rename_map[str(i)] = f'value{i}'
        
    # Apply renaming
    df = df.rename(columns=rename_map)
    
    # 4. Define target columns in the correct order
    target_columns = [
        'date', 'value1', 'value2', 'value3', 'value4', 'value5', 'value6', 
        'value7', 'value8', 'value9', 'value10', 'value11', 'value12', 
        'value13', 'value14', 'value15', 'value16', 'value17', 'value18', 
        'value19', 'value20', 'value21', 'value22', 'value23', 'value24'
    ]
    
    # 5. Select only the target columns. 
    # The 'Class' column is implicitly dropped as it's not in target_columns.
    # We also drop the original 'Date' datetime column if it still exists (it's not in target_columns).
    df = df[target_columns]
    
    # 6. Sort by date to match the target sample order
    # Since 'date' is a string in YYYY-MM-DD format, string sorting works correctly for chronological order
    df = df.sort_values(by='date').reset_index(drop=True)
    
    # Ensure numeric columns are float
    for col in target_columns[1:]:
        df[col] = df[col].astype(float)
        
    return df[target_columns]