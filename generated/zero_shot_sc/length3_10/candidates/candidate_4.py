import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    # Create a copy to avoid modifying the original
    df = source.copy()
    
    # 1. Transform the Date column
    # Source format: '%a %m/%d/%Y' (e.g., 'Thu 10/01/2009')
    # Target format: '%m/%d/%Y' (e.g., '10/01/2009')
    # We can parse the datetime and then format it. 
    # Note: pd.to_datetime might struggle with the day name prefix in some contexts, 
    # so we can strip the day name part first for robustness.
    # The day name is typically 3 chars + 1 space = 4 chars.
    if 'Date' in df.columns:
        # Extract the date part by removing the day of week prefix
        # Assuming the format is consistently "Day MM/DD/YYYY"
        date_strings = df['Date'].astype(str).str.split(' ', n=1, expand=True)[1]
        # Parse to datetime to ensure valid dates, then format to MM/DD/YYYY
        dates = pd.to_datetime(date_strings, format='%m/%d/%Y')
        df['date'] = dates.dt.strftime('%m/%d/%Y')
    
    # 2. Rename Hour columns
    # Source columns are like '1:00', '2:00', ..., '24:00:00'
    # Target columns are 'Hour 1', 'Hour 2', ..., 'Hour 24'
    
    rename_map = {}
    for col in df.columns:
        # Check if column is an hour column
        # It should contain ':' and be numeric before the ':'
        if ':' in str(col):
            try:
                # Extract the number before the first colon
                hour_num = int(str(col).split(':')[0])
                rename_map[col] = f'Hour {hour_num}'
            except ValueError:
                pass # Skip if not a valid hour column
    
    df.rename(columns=rename_map, inplace=True)
    
    # 3. Define target columns
    target_columns = ['date', 'Hour 1', 'Hour 2', 'Hour 3', 'Hour 4', 'Hour 5', 'Hour 6', 
                      'Hour 7', 'Hour 8', 'Hour 9', 'Hour 10', 'Hour 11', 'Hour 12', 
                      'Hour 13', 'Hour 14', 'Hour 15', 'Hour 16', 'Hour 17', 'Hour 18', 
                      'Hour 19', 'Hour 20', 'Hour 21', 'Hour 22', 'Hour 23', 'Hour 24']
    
    # 4. Select and order columns
    # Ensure all target columns exist in df
    available_cols = [col for col in target_columns if col in df.columns]
    
    # If any target columns are missing, we might need to handle it, but based on the problem,
    # the source has all 24 hours.
    
    df = df[available_cols]
    
    return df[target_columns]