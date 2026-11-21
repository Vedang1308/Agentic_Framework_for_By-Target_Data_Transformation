import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the CST column and format it to MM/DD/YYYY
    # The source format is '%a %m/%d/%Y' (e.g., 'Sat 12/01/2012')
    # The target format is '%m/%d/%Y' (e.g., '12/01/2012')
    df['date'] = pd.to_datetime(df['CST'], format='%a %m/%d/%Y').dt.strftime('%m/%d/%Y')
    
    # 2. Define the mapping for the value columns
    # Source columns are '1:00', '2:00', ..., '24:00:00'
    # Target columns are 'value1', 'value2', ..., 'value24'
    rename_mapping = {}
    for i in range(1, 24):
        rename_mapping[f'{i}:00'] = f'value{i}'
    rename_mapping['24:00:00'] = 'value24'
    
    # 3. Rename the columns
    df.rename(columns=rename_mapping, inplace=True)
    
    # 4. Drop the original CST column as it is no longer needed
    df.drop(columns=['CST'], inplace=True)
    
    # 5. Sort by date to match the target sample order
    df.sort_values(by='date', inplace=True)
    
    # 6. Reset index
    df.reset_index(drop=True, inplace=True)
    
    # 7. Define target columns to ensure exact order and naming
    target_columns = [
        'date', 'value1', 'value2', 'value3', 'value4', 'value5', 'value6', 'value7', 
        'value8', 'value9', 'value10', 'value11', 'value12', 'value13', 'value14', 
        'value15', 'value16', 'value17', 'value18', 'value19', 'value20', 'value21', 
        'value22', 'value23', 'value24'
    ]
    
    return df[target_columns]