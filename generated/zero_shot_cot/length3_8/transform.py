import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    # Create a copy to avoid modifying the original
    df = source.copy()
    
    # Define the target column names
    target_columns = [
        'date', 'Hour 1', 'Hour 2', 'Hour 3', 'Hour 4', 'Hour 5', 'Hour 6', 
        'Hour 7', 'Hour 8', 'Hour 9', 'Hour 10', 'Hour 11', 'Hour 12', 
        'Hour 13', 'Hour 14', 'Hour 15', 'Hour 16', 'Hour 17', 'Hour 18', 
        'Hour 19', 'Hour 20', 'Hour 21', 'Hour 22', 'Hour 23', 'Hour 24'
    ]
    
    # Transform the 'CST' column to 'date'
    # Source format: '%a %m/%d/%Y' (e.g., 'Sat 12/01/2012')
    # Target format: '%m/%d/%Y' (e.g., '04/01/2009')
    # We can parse the date and then format it.
    # Note: pd.to_datetime might be slow for large datasets, but it's robust.
    # Alternatively, we can just extract the substring if the format is strictly consistent.
    # Let's use pd.to_datetime for robustness.
    df['date'] = pd.to_datetime(df['CST'], format='%a %m/%d/%Y').dt.strftime('%m/%d/%Y')
    
    # Define the mapping for hourly columns
    # Source columns: '1:00', '2:00', ..., '23:00', '24:00:00'
    # Target columns: 'Hour 1', 'Hour 2', ..., 'Hour 23', 'Hour 24'
    col_mapping = {}
    for i in range(1, 24):
        col_mapping[f'{i}:00'] = f'Hour {i}'
    col_mapping['24:00:00'] = 'Hour 24'
    
    # Rename the columns
    df = df.rename(columns=col_mapping)
    
    # Select and order the columns as per the target schema
    # We need to drop the original 'CST' column and keep the new 'date' column
    # and the renamed hourly columns.
    df = df[target_columns]
    
    return df[target_columns]