import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # Define the target column names
    target_columns = ['date', 'value1', 'value2', 'value3', 'value4', 'value5', 'value6', 'value7', 'value8', 'value9', 'value10', 'value11', 'value12', 'value13', 'value14', 'value15', 'value16', 'value17', 'value18', 'value19', 'value20', 'value21', 'value22', 'value23', 'value24']
    
    # Create a mapping for renaming the hourly columns
    rename_mapping = {}
    for i in range(1, 24):
        rename_mapping[f'{i}:00'] = f'value{i}'
    rename_mapping['24:00:00'] = 'value24'
    
    # Rename the columns
    df = df.rename(columns=rename_mapping)
    
    # Parse and format the date column
    # Source format: '%a %m/%d/%Y' (e.g., 'Sat 12/01/2012')
    # Target format: '%m/%d/%Y' (e.g., '04/01/2009')
    df['date'] = pd.to_datetime(df['CST'], format='%a %m/%d/%Y').dt.strftime('%m/%d/%Y')
    
    # Drop the original CST column if it still exists (it should be replaced/renamed, but CST is not in rename_mapping)
    if 'CST' in df.columns:
        df = df.drop(columns=['CST'])
    
    # Ensure the columns are in the correct order
    return df[target_columns]