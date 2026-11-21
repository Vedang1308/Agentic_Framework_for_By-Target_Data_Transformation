import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Transform the 'CST' column to 'date'
    # Source format: 'Sat 12/01/2012' (%a %m/%d/%Y)
    # Target format: '04/01/2009' (%m/%d/%Y)
    # We can extract the date part by splitting on space and taking the second element
    df['date'] = df['CST'].str.split(' ').str[1]
    
    # 2. Define the mapping for the hourly columns
    # Source columns: '1:00', '2:00', ..., '23:00', '24:00:00'
    # Target columns: 'Hour 1', 'Hour 2', ..., 'Hour 23', 'Hour 24'
    
    col_mapping = {}
    for i in range(1, 24):
        col_mapping[f'{i}:00'] = f'Hour {i}'
    col_mapping['24:00:00'] = 'Hour 24'
    
    # 3. Rename the columns
    df = df.rename(columns=col_mapping)
    
    # 4. Select and order the columns to match the target schema exactly
    target_columns = ['date', 'Hour 1', 'Hour 2', 'Hour 3', 'Hour 4', 'Hour 5', 'Hour 6', 
                      'Hour 7', 'Hour 8', 'Hour 9', 'Hour 10', 'Hour 11', 'Hour 12', 
                      'Hour 13', 'Hour 14', 'Hour 15', 'Hour 16', 'Hour 17', 'Hour 18', 
                      'Hour 19', 'Hour 20', 'Hour 21', 'Hour 22', 'Hour 23', 'Hour 24']
    
    # Drop the original CST column as it's no longer needed
    df = df.drop(columns=['CST'])
    
    # Ensure the correct column order
    df = df[target_columns]
    
    return df[target_columns]