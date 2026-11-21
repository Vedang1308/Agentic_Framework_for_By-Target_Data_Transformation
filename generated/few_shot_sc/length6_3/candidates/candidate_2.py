import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the date column to datetime
    df['date'] = pd.to_datetime(df['date'])
    
    # 2. Set date as index for easy reindexing
    df = df.set_index('date')
    
    # 3. Create a complete date range from min to max date in the source
    # This handles the row count increase by filling missing days
    min_date = df.index.min()
    max_date = df.index.max()
    complete_date_range = pd.date_range(start=min_date, end=max_date, freq='D')
    
    # 4. Reindex the dataframe to the complete date range
    # Missing dates will be filled with NaN
    df = df.reindex(complete_date_range)
    
    # 5. Rename value columns to Hr 1 ... Hr 24
    rename_dict = {f'value{i}': f'Hr {i}' for i in range(1, 25)}
    df = df.rename(columns=rename_dict)
    
    # 6. Drop non-target columns (class, Description, analysis, uom)
    # We only need the Hour columns and the date index
    target_hour_cols = [f'Hr {i}' for i in range(1, 25)]
    df = df[target_hour_cols]
    
    # 7. Format the index (date) to the target string format '%Y-%m-%d %H:%M:%S'
    # The target sample shows '2011-01-01 00:00:00'
    df.index = df.index.strftime('%Y-%m-%d %H:%M:%S')
    
    # 8. Reset index to make 'Date' a column
    df = df.reset_index()
    df = df.rename(columns={'index': 'Date'})
    
    # 9. Define target columns verbatim
    target_columns = ['Date'] + [f'Hr {i}' for i in range(1, 25)]
    
    return df[target_columns]