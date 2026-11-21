import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame to the target DataFrame.
    
    Steps:
    1. Parse the 'CST' column to datetime.
    2. Format the date to 'MM/DD/YYYY' for the 'date' column.
    3. Rename the hourly columns from 'H:00'/'24:00:00' to 'Hour H'.
    4. Reorder columns to match the target schema.
    """
    df = source.copy()
    
    # 1. Parse the CST column to datetime
    # Format is '%a %m/%d/%Y' e.g., 'Sat 12/01/2012'
    df['CST_parsed'] = pd.to_datetime(df['CST'], format='%a %m/%d/%Y')
    
    # 2. Create the 'date' column in the required format '%m/%d/%Y'
    df['date'] = df['CST_parsed'].dt.strftime('%m/%d/%Y')
    
    # 3. Define column mapping for hours
    # Source columns: 1:00, 2:00, ..., 23:00, 24:00:00
    # Target columns: Hour 1, Hour 2, ..., Hour 23, Hour 24
    rename_map = {}
    
    # Map 1:00 to 23:00
    for h in range(1, 24):
        rename_map[f'{h}:00'] = f'Hour {h}'
        
    # Map 24:00:00 to Hour 24
    rename_map['24:00:00'] = 'Hour 24'
    
    # Apply renaming
    df = df.rename(columns=rename_map)
    
    # 4. Define the target column order
    target_columns = ['date', 'Hour 1', 'Hour 2', 'Hour 3', 'Hour 4', 'Hour 5', 'Hour 6', 'Hour 7', 'Hour 8', 'Hour 9', 'Hour 10', 'Hour 11', 'Hour 12', 'Hour 13', 'Hour 14', 'Hour 15', 'Hour 16', 'Hour 17', 'Hour 18', 'Hour 19', 'Hour 20', 'Hour 21', 'Hour 22', 'Hour 23', 'Hour 24']
    
    # 5. Select and return the final DataFrame
    # Drop the intermediate parsed column if it exists
    if 'CST_parsed' in df.columns:
        df = df.drop(columns=['CST_parsed'])
        
    return df[target_columns]