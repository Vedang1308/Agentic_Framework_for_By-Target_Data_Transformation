import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame into the target DataFrame.
    
    Steps:
    1. Parse the 'Date' column.
    2. Create 'dt_strata' (MM/DD/YY) and 'dow' (1=Mon, 7=Sun).
    3. Rename hourly columns from 'H:MM' format to 'pct_hourly_HHMM'.
    4. Add 'pct_hourly_2500' as NaN.
    5. Return DataFrame with specific column order.
    """
    
    # Define target column names
    target_columns = [
        'dt_strata', 'dow', 
        'pct_hourly_0100', 'pct_hourly_0200', 'pct_hourly_0300', 'pct_hourly_0400', 
        'pct_hourly_0500', 'pct_hourly_0600', 'pct_hourly_0700', 'pct_hourly_0800', 
        'pct_hourly_0900', 'pct_hourly_1000', 'pct_hourly_1100', 'pct_hourly_1200', 
        'pct_hourly_1300', 'pct_hourly_1400', 'pct_hourly_1500', 'pct_hourly_1600', 
        'pct_hourly_1700', 'pct_hourly_1800', 'pct_hourly_1900', 'pct_hourly_2000', 
        'pct_hourly_2100', 'pct_hourly_2200', 'pct_hourly_2300', 'pct_hourly_2400', 
        'pct_hourly_2500'
    ]
    
    # 1. Parse Date
    # Format: 'Thu 10/01/2009' -> '%a %m/%d/%Y'
    df = source.copy()
    df['parsed_date'] = pd.to_datetime(df['Date'], format='%a %m/%d/%Y')
    
    # 2. Create dt_strata (MM/DD/YY)
    df['dt_strata'] = df['parsed_date'].dt.strftime('%m/%d/%y')
    
    # 3. Create dow (1=Monday, ..., 7=Sunday)
    # pandas dayofweek: 0=Monday, 6=Sunday
    df['dow'] = df['parsed_date'].dt.dayofweek + 1
    
    # 4. Rename hourly columns
    # Source columns: '1:00', '2:00', ..., '23:00', '24:00:00'
    # Target columns: 'pct_hourly_0100', ..., 'pct_hourly_2300', 'pct_hourly_2400'
    
    # Identify source hourly columns
    source_hourly_cols = [c for c in df.columns if c not in ['Segment', 'Date', 'parsed_date']]
    
    # Create a mapping for renaming
    rename_map = {}
    for i, col in enumerate(source_hourly_cols):
        # i goes from 0 to 23
        hour_num = i + 1
        target_col_name = f'pct_hourly_{hour_num:02d}00'
        rename_map[col] = target_col_name
        
    df = df.rename(columns=rename_map)
    
    # 5. Add pct_hourly_2500 as NaN
    df['pct_hourly_2500'] = np.nan
    
    # 6. Select and order columns
    # Ensure we only return the target columns
    result_df = df[target_columns].copy()
    
    # Ensure correct data types
    result_df['dow'] = result_df['dow'].astype('int64')
    # dt_strata is already object/string
    # Float columns should remain float64
    
    return result_df