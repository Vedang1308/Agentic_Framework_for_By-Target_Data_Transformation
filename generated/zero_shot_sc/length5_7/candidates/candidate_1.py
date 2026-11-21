import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame by parsing dates, renaming columns,
    ensuring a continuous daily time series (filling missing dates via interpolation),
    and formatting the output to match the target schema.
    """
    # 1. Parse the Date column to datetime
    df = source.copy()
    df['Date'] = pd.to_datetime(df['Date'])
    
    # 2. Set Date as index and sort to ensure chronological order
    df = df.set_index('Date').sort_index()
    
    # 3. Rename numeric columns 1-24 to value1-value24
    rename_map = {i: f'value{i}' for i in range(1, 25)}
    df = df.rename(columns=rename_map)
    
    # 4. Create a complete daily date range from min to max date in the source
    # This handles the case where source has missing days (explaining the row count increase)
    start_date = df.index.min()
    end_date = df.index.max()
    complete_index = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # 5. Reindex to the complete date range
    df = df.reindex(complete_index)
    
    # 6. Fill missing values (NaNs) for any dates that were not in the original source
    # Interpolation is suitable for load profile data
    df = df.interpolate(method='linear')
    # Forward fill and backward fill to handle any NaNs at the very beginning or end
    # if the interpolation didn't cover them (e.g., if min/max dates were missing, though reindex uses them)
    df = df.ffill().bfill()
    
    # 7. Reset index to bring 'Date' back as a column
    df = df.reset_index()
    df = df.rename(columns={'index': 'date'})
    
    # 8. Format the date column to the required string format
    df['date'] = df['date'].dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # 9. Define target columns to ensure exact order and naming
    target_columns = ['date'] + [f'value{i}' for i in range(1, 25)]
    
    # 10. Return the DataFrame with the exact target schema
    return df[target_columns]