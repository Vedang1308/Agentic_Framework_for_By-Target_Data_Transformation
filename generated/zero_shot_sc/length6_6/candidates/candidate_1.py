import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame into the target DataFrame.
    
    Steps:
    1. Parse the 'date' column to datetime.
    2. Rename 'Hour X' columns to 'Hr X'.
    3. Identify the full date range from min to max date in the source.
    4. Reindex to this complete daily frequency to handle missing days (increasing row count from 182 to 183).
    5. Fill missing values using forward fill and backward fill.
    6. Format the date column to the required string format.
    7. Return the dataframe with the exact target column names.
    """
    df = source.copy()
    
    # 1. Parse dates
    df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y')
    
    # 2. Rename columns from 'Hour X' to 'Hr X'
    rename_map = {col: col.replace('Hour', 'Hr') for col in df.columns if col != 'date'}
    df.rename(columns=rename_map, inplace=True)
    
    # 3. Set date as index for reindexing
    df.set_index('date', inplace=True)
    
    # 4. Create a complete date range
    # We assume the target covers all days between the min and max date of the source.
    # The discrepancy in row count (182 vs 183) suggests one day is missing in the source.
    min_date = df.index.min()
    max_date = df.index.max()
    
    # Create a continuous daily frequency range
    full_date_range = pd.date_range(start=min_date, end=max_date, freq='D')
    
    # 5. Reindex to the full date range
    # This will add rows for missing dates with NaN values
    df = df.reindex(full_date_range)
    
    # 6. Fill missing values
    # Using ffill then bfill handles gaps in the middle and at the edges
    df = df.ffill().bfill()
    
    # 7. Reset index to make date a column again
    df = df.reset_index()
    df.rename(columns={'index': 'Date'}, inplace=True)
    
    # 8. Format the Date column to 'YYYY-MM-DD HH:MM:SS'
    df['Date'] = df['Date'].dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # 9. Define target columns to ensure exact order and naming
    target_columns = ['Date', 'Hr 1', 'Hr 2', 'Hr 3', 'Hr 4', 'Hr 5', 'Hr 6', 'Hr 7', 'Hr 8', 'Hr 9', 
                      'Hr 10', 'Hr 11', 'Hr 12', 'Hr 13', 'Hr 14', 'Hr 15', 'Hr 16', 'Hr 17', 'Hr 18', 
                      'Hr 19', 'Hr 20', 'Hr 21', 'Hr 22', 'Hr 23', 'Hr 24']
    
    return df[target_columns]