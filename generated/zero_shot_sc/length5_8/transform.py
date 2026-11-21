import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    # Create a copy to avoid modifying the original
    df = source.copy()
    
    # Define the target column names
    target_columns = [
        'date', 'value1', 'value2', 'value3', 'value4', 'value5', 'value6', 
        'value7', 'value8', 'value9', 'value10', 'value11', 'value12', 'value13', 
        'value14', 'value15', 'value16', 'value17', 'value18', 'value19', 'value20', 
        'value21', 'value22', 'value23', 'value24'
    ]
    
    # Step 1: Parse the date column
    # The source date format is '%m/%d/%Y'
    df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y')
    
    # Step 2: Rename columns from 'Hour X' to 'valueX'
    rename_map = {}
    for i in range(1, 25):
        rename_map[f'Hour {i}'] = f'value{i}'
    
    df.rename(columns=rename_map, inplace=True)
    
    # Step 3: Format the date column to '%Y-%m-%d %H:%M:%S'
    df['date'] = df['date'].dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Step 4: Ensure the column order matches the target schema
    # The target schema starts with 'date' followed by value1 to value24
    return df[target_columns]