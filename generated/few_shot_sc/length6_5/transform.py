import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse Date column to datetime
    df['Date'] = pd.to_datetime(df['Date'])
    
    # 2. Set Date as index to facilitate reindexing for missing dates
    df = df.set_index('Date')
    
    # 3. Sort index to ensure chronological order
    df = df.sort_index()
    
    # 4. Create a complete date range from min to max date in the source
    # This handles the row count increase (182 -> 183) by filling in missing days
    full_date_range = pd.date_range(start=df.index.min(), end=df.index.max(), freq='D')
    
    # 5. Reindex to the full date range, introducing NaN rows for missing dates
    df = df.reindex(full_date_range)
    
    # 6. Fill missing values. Forward fill is appropriate for daily time series data
    # where a single day's profile might be missing.
    df = df.ffill()
    
    # 7. Reset index to convert Date back to a column
    df = df.reset_index()
    df = df.rename(columns={'index': 'Date'})
    
    # 8. Format Date column to '%m/%d/%Y'
    df['Date'] = df['Date'].dt.strftime('%m/%d/%Y')
    
    # 9. Rename numeric columns 1-24 to 'Hr 1' - 'Hr 24'
    rename_dict = {str(i): f'Hr {i}' for i in range(1, 25)}
    df = df.rename(columns=rename_dict)
    
    # 10. Define target columns verbatim
    target_columns = ['Date'] + [f'Hr {i}' for i in range(1, 25)]
    
    # 11. Return the dataframe with only the target columns
    # Note: We drop 'Class' implicitly by selecting only target_columns
    return df[target_columns]