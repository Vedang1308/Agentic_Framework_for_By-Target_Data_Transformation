import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame into the target DataFrame by renaming columns,
    formatting dates, and sorting chronologically.
    """
    df = source.copy()
    
    # 1. Parse the Date column to datetime to handle formatting and sorting
    # The source format is '%m/%d/%Y' (e.g., '7/3/2013')
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
    
    # 2. Format the date to '%m/%d/%Y' which ensures zero-padding (e.g., '01/01/2013')
    # This matches the target sample format.
    df['date'] = df['Date'].dt.strftime('%m/%d/%Y')
    
    # 3. Rename the hour columns from integers 1-24 to 'Hour 1'-'Hour 24'
    hour_columns = {str(i): f'Hour {i}' for i in range(1, 25)}
    df.rename(columns=hour_columns, inplace=True)
    
    # 4. Select only the required columns for the target
    # The target does not have 'Date' (original) or 'Class'
    target_columns = [
        'date', 'Hour 1', 'Hour 2', 'Hour 3', 'Hour 4', 'Hour 5', 'Hour 6', 
        'Hour 7', 'Hour 8', 'Hour 9', 'Hour 10', 'Hour 11', 'Hour 12', 
        'Hour 13', 'Hour 14', 'Hour 15', 'Hour 16', 'Hour 17', 'Hour 18', 
        'Hour 19', 'Hour 20', 'Hour 21', 'Hour 22', 'Hour 23', 'Hour 24'
    ]
    
    # 5. Sort by date to match the target's chronological order
    # We use the parsed datetime 'Date' column for sorting, then drop it later
    df = df.sort_values(by='Date')
    
    # 6. Reset index and drop the temporary 'Date' column if it's not in target_columns
    df = df.reset_index(drop=True)
    
    # 7. Return the DataFrame with exact target columns
    return df[target_columns]