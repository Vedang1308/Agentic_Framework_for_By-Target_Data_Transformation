import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # 1. Parse the Date column to datetime
    df = source.copy()
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
    
    # 2. Sort by date to ensure correct order for interpolation
    df = df.sort_values('Date')
    
    # 3. Set Date as index to facilitate reindexing
    df = df.set_index('Date')
    
    # 4. Determine the full date range to fill any gaps
    # The row count change suggests missing dates need to be filled
    min_date = df.index.min()
    max_date = df.index.max()
    
    # Create a complete daily date range
    full_date_range = pd.date_range(start=min_date, end=max_date, freq='D')
    
    # Reindex to the full date range. This introduces NaN rows for missing dates.
    df = df.reindex(full_date_range)
    
    # 5. Interpolate missing values (linear interpolation across days)
    # This handles the gap filling for the hourly columns
    df = df.interpolate(method='linear')
    
    # 6. Drop the 'Class' column as it is not in the target
    if 'Class' in df.columns:
        df = df.drop(columns=['Class'])
    
    # 7. Rename columns from integers 1-24 to 'Hr 1'-'Hr 24'
    rename_map = {i: f'Hr {i}' for i in range(1, 25)}
    df = df.rename(columns=rename_map)
    
    # 8. Reset index to make Date a column again
    df = df.reset_index()
    df = df.rename(columns={'index': 'Date'})
    
    # 9. Format the Date column back to string '%m/%d/%Y'
    df['Date'] = df['Date'].dt.strftime('%m/%d/%Y')
    
    # 10. Define the target columns in the exact order
    target_columns = ['Date'] + [f'Hr {i}' for i in range(1, 25)]
    
    # 11. Ensure only target columns are present and in correct order
    df = df[target_columns]
    
    return df[target_columns]