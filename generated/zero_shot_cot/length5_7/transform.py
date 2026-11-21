import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame into the target DataFrame by:
    1. Parsing the Date column.
    2. Creating a complete daily date range to handle missing days (row count increase).
    3. Reindexing and interpolating missing values.
    4. Renaming columns to match the target schema.
    5. Formatting the date column.
    """
    # 1. Parse the Date column
    df = source.copy()
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
    
    # 2. Set Date as index
    df = df.set_index('Date')
    
    # 3. Define target column names for numeric values
    # Source columns are 1-24 (as strings or ints depending on read_csv, usually strings if mixed, but here float64 implies they were read as numbers, but column names might be strings '1', '2'...)
    # The source schema says '1' (float64), so column names are likely strings '1', '2', ... '24'
    source_numeric_cols = [str(i) for i in range(1, 25)]
    target_numeric_cols = [f'value{i}' for i in range(1, 25)]
    
    # Rename numeric columns
    df = df.rename(columns={str(i): f'value{i}' for i in range(1, 25)})
    
    # Drop the 'Class' column if it exists
    if 'Class' in df.columns:
        df = df.drop(columns=['Class'])
    
    # 4. Create a complete date range from min to max date in the source
    # This handles the row count increase (182 -> 183) by filling gaps
    min_date = df.index.min()
    max_date = df.index.max()
    full_date_range = pd.date_range(start=min_date, end=max_date, freq='D')
    
    # 5. Reindex to the full date range
    df = df.reindex(full_date_range)
    
    # 6. Interpolate missing values
    # Since the data represents hourly load profiles, linear interpolation is appropriate for missing days
    df = df.interpolate(method='linear')
    
    # If there are still NaNs (e.g., at the very start or end if the gap was larger than expected), 
    # we can forward fill or backward fill, though interpolation usually handles internal gaps.
    # Given the specific +1 row count, it's likely a single internal gap or edge case.
    # Let's ensure no NaNs remain by ffill/bfill just in case
    df = df.ffill().bfill()
    
    # 7. Format the date index to the required string format
    df.index = df.index.strftime('%Y-%m-%d %H:%M:%S')
    
    # 8. Reset index to make 'date' a column
    df = df.reset_index()
    df = df.rename(columns={'index': 'date'})
    
    # 9. Define final target columns
    target_columns = ['date'] + [f'value{i}' for i in range(1, 25)]
    
    # 10. Return the DataFrame with exact column order
    return df[target_columns]