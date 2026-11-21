import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame with CST date and hourly columns 
    into a target DataFrame with formatted date and renamed hourly columns.
    """
    # Define the target column names verbatim
    target_columns = [
        'date', 'Hour 1', 'Hour 2', 'Hour 3', 'Hour 4', 'Hour 5', 'Hour 6', 
        'Hour 7', 'Hour 8', 'Hour 9', 'Hour 10', 'Hour 11', 'Hour 12', 
        'Hour 13', 'Hour 14', 'Hour 15', 'Hour 16', 'Hour 17', 'Hour 18', 
        'Hour 19', 'Hour 20', 'Hour 21', 'Hour 22', 'Hour 23', 'Hour 24'
    ]
    
    # 1. Process the Date Column
    # Parse the 'CST' column which is in format '%a %m/%d/%Y' (e.g., 'Sat 12/01/2012')
    # We strip the day of week part to parse just the date, or use strptime directly.
    # Since the format is consistent, we can parse it.
    # Note: pd.to_datetime might struggle with the '%a ' prefix directly if not handled carefully, 
    # but usually it handles '%a %m/%d/%Y' if the locale matches or if we just extract the date part.
    # A safer approach for '%a %m/%d/%Y' is to strip the first 4 characters (e.g., 'Sat ') or parse carefully.
    
    # Extract the date part by removing the day-of-week abbreviation (3 chars + space)
    date_strings = source['CST'].str.split().str[1] # Takes '12/01/2012' from 'Sat 12/01/2012'
    dates = pd.to_datetime(date_strings, format='%m/%d/%Y')
    formatted_dates = dates.dt.strftime('%m/%d/%Y')
    
    # 2. Map Source Hour Columns to Target Hour Columns
    # Source columns: '1:00', '2:00', ..., '23:00', '24:00:00'
    # Target columns: 'Hour 1', 'Hour 2', ..., 'Hour 23', 'Hour 24'
    
    # Create a list of source hour columns in order
    source_hour_cols = []
    for i in range(1, 24):
        source_hour_cols.append(f'{i}:00')
    source_hour_cols.append('24:00:00')
    
    # Create a list of target hour columns in order
    target_hour_cols = [f'Hour {i}' for i in range(1, 25)]
    
    # 3. Construct the new DataFrame
    # Initialize with the date column
    df = pd.DataFrame()
    df['date'] = formatted_dates.values
    
    # Assign the hour columns
    for src_col, tgt_col in zip(source_hour_cols, target_hour_cols):
        df[tgt_col] = source[src_col].values
        
    # 4. Ensure final column order matches target exactly
    return df[target_columns]