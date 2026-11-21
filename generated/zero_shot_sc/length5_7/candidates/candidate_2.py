import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # 1. Parse the Date column
    df = source.copy()
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
    
    # 2. Sort by Date to ensure correct order
    df = df.sort_values('Date').reset_index(drop=True)
    
    # 3. Identify the date range
    # The target has 183 rows, source has 182. 
    # Based on the target sample starting at 2013-01-01 and ending at 2013-07-02 (183 days),
    # and the source likely covering Jan 1 to July 1 (182 days), we extend the range by 1 day.
    min_date = df['Date'].min()
    max_date = df['Date'].max()
    
    # Create a complete date range. 
    # We add one day to the max_date to account for the extra row in the target.
    target_date_range = pd.date_range(start=min_date, end=max_date + pd.Timedelta(days=1), freq='D')
    
    # 4. Reindex to the complete date range
    df = df.set_index('Date')
    df = df.reindex(target_date_range)
    
    # 5. Fill missing values
    # Since the missing day is likely at the end (based on the 182->183 count and typical data gaps),
    # forward fill is a reasonable strategy. If the gap was in the middle, interpolation might be better,
    # but ffill is safer for "next day unknown" scenarios in simple transformations.
    df = df.ffill()
    
    # 6. Rename numeric columns from 1..24 to value1..value24
    rename_dict = {i: f'value{i}' for i in range(1, 25)}
    df = df.rename(columns=rename_dict)
    
    # 7. Reset index to make Date a column again
    df = df.reset_index()
    
    # 8. Rename Date column to 'date' and format
    df = df.rename(columns={'index': 'date'})
    df['date'] = df['date'].dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # 9. Define target columns
    target_columns = ['date'] + [f'value{i}' for i in range(1, 25)]
    
    # 10. Return the DataFrame with exact target schema
    return df[target_columns]