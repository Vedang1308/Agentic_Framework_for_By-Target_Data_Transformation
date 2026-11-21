import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # Define target column names exactly as required
    target_columns = [
        'date', 'Hour 1', 'Hour 2', 'Hour 3', 'Hour 4', 'Hour 5', 'Hour 6', 
        'Hour 7', 'Hour 8', 'Hour 9', 'Hour 10', 'Hour 11', 'Hour 12', 
        'Hour 13', 'Hour 14', 'Hour 15', 'Hour 16', 'Hour 17', 'Hour 18', 
        'Hour 19', 'Hour 20', 'Hour 21', 'Hour 22', 'Hour 23', 'Hour 24'
    ]
    
    # 1. Transform the Date column
    # Source format: '%a %m/%d/%Y' (e.g., 'Thu 10/01/2009')
    # Target format: '%m/%d/%Y' (e.g., '01/01/2003')
    # We parse the source date and then format it to the target string representation.
    parsed_dates = pd.to_datetime(source['Date'], format='%a %m/%d/%Y')
    formatted_dates = parsed_dates.dt.strftime('%m/%d/%Y')
    
    # 2. Prepare the hourly columns
    # Source columns: '1:00', '2:00', ..., '23:00', '24:00:00'
    # Target columns: 'Hour 1', 'Hour 2', ..., 'Hour 23', 'Hour 24'
    
    # Create a mapping for renaming
    rename_map = {}
    for i in range(1, 24):
        rename_map[f'{i}:00'] = f'Hour {i}'
    rename_map['24:00:00'] = 'Hour 24'
    
    # Select only the hourly columns from source and rename them
    hourly_cols_source = [f'{i}:00' for i in range(1, 24)] + ['24:00:00']
    df_hours = source[hourly_cols_source].rename(columns=rename_map)
    
    # 3. Construct the final DataFrame
    df = pd.DataFrame()
    df['date'] = formatted_dates
    
    # Assign the renamed hourly columns
    for col in target_columns[1:]: # Skip 'date' as it's already added
        df[col] = df_hours[col]
        
    # Ensure the column order matches the target schema exactly
    return df[target_columns]