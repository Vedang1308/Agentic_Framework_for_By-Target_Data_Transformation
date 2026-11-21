import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame to the target DataFrame by:
    1. Parsing the 'date' column to datetime.
    2. Reindexing to a complete daily date range from min to max date to handle missing days.
    3. Filling missing values with 0.
    4. Renaming columns from 'Hour X' to 'Hr X' and 'date' to 'Date'.
    5. Formatting the 'Date' column as 'YYYY-MM-DD HH:MM:SS'.
    """
    
    # 1. Parse the date column
    df = source.copy()
    df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y')
    
    # 2. Sort by date to ensure correct min/max and order
    df = df.sort_values('date')
    
    # 3. Create a complete date range from the minimum to maximum date in the source
    # This handles the row count increase (182 -> 183) by filling in any missing days
    min_date = df['date'].min()
    max_date = df['date'].max()
    full_date_range = pd.date_range(start=min_date, end=max_date, freq='D')
    
    # 4. Set date as index and reindex to the full range
    df = df.set_index('date')
    df = df.reindex(full_date_range)
    
    # 5. Fill missing values (NaN) with 0
    # The target shows 0 for integer columns and specific values for floats.
    # Missing days are typically zero-load or zero-value in these contexts.
    df = df.fillna(0)
    
    # 6. Rename columns
    # Map 'Hour X' to 'Hr X'
    rename_map = {}
    for i in range(1, 25):
        rename_map[f'Hour {i}'] = f'Hr {i}'
    
    df = df.rename(columns=rename_map)
    
    # 7. Reset index to bring 'date' back as a column, then rename it to 'Date'
    df = df.reset_index()
    df = df.rename(columns={'date': 'Date'})
    
    # 8. Format the Date column as required: 'YYYY-MM-DD HH:MM:SS'
    df['Date'] = df['Date'].dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # 9. Define the exact target column order
    target_columns = [
        'Date', 'Hr 1', 'Hr 2', 'Hr 3', 'Hr 4', 'Hr 5', 'Hr 6', 'Hr 7', 
        'Hr 8', 'Hr 9', 'Hr 10', 'Hr 11', 'Hr 12', 'Hr 13', 'Hr 14', 
        'Hr 15', 'Hr 16', 'Hr 17', 'Hr 18', 'Hr 19', 'Hr 20', 'Hr 21', 
        'Hr 22', 'Hr 23', 'Hr 24'
    ]
    
    # 10. Ensure correct column order and return
    return df[target_columns]