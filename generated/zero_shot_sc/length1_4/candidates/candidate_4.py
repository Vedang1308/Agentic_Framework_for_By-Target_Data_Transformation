import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    # 1. Parse the Date column to datetime
    df = source.copy()
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
    
    # 2. Set Date as index for easier time-series manipulation
    df = df.set_index('Date')
    
    # 3. Identify the full range of dates
    # The target has more rows, implying missing dates in source that need to be filled.
    min_date = df.index.min()
    max_date = df.index.max()
    
    # 4. Create a complete date range
    complete_dates = pd.date_range(start=min_date, end=max_date, freq='D')
    
    # 5. Reindex to include missing dates (introduces NaNs)
    df = df.reindex(complete_dates)
    
    # 6. Interpolate missing values
    # The numeric columns are 1-24. We drop 'Class' if it exists.
    if 'Class' in df.columns:
        df = df.drop(columns=['Class'])
        
    # Interpolate linearly across the dates (rows)
    # axis=0 is default. This fills NaNs in the time series.
    df = df.interpolate(method='linear')
    
    # 7. Rename numeric columns from '1'-'24' to '1:00'-'24:00'
    # The source columns are integers 1-24 (or strings '1'-'24')
    rename_map = {str(i): f"{i}:00" for i in range(1, 25)}
    df = df.rename(columns=rename_map)
    
    # 8. Format the index into the 'cst' column
    # Format: '%a %m/%d/%Y' (e.g., 'Tue 01/01/2013')
    df['cst'] = df.index.strftime('%a %m/%d/%Y')
    
    # 9. Reset index to bring 'cst' into the columns
    df = df.reset_index(drop=True)
    
    # 10. Define target columns and reorder
    target_columns = ['cst'] + [f"{i}:00" for i in range(1, 25)]
    
    # Ensure all target columns exist and return in correct order
    return df[target_columns]