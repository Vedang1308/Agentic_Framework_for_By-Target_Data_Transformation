import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame into the target DataFrame format.
    
    Steps:
    1. Parse the 'Date' column into datetime objects.
    2. Create 'dt_strata' column formatted as 'MM/DD/YY'.
    3. Create 'dow' column where Monday=1, ..., Sunday=7.
    4. Rename hourly columns from 'H:00'/'24:00:00' format to 'pct_hourly_HHMM'.
    5. Add an empty 'pct_hourly_2500' column with NaN values.
    6. Return the DataFrame with columns ordered as per target schema.
    """
    df = source.copy()
    
    # 1. Parse Date
    # Format: 'Thu 10/01/2009' -> '%a %m/%d/%Y'
    df['parsed_date'] = pd.to_datetime(df['Date'], format='%a %m/%d/%Y')
    
    # 2. Create dt_strata (MM/DD/YY)
    df['dt_strata'] = df['parsed_date'].dt.strftime('%m/%d/%y')
    
    # 3. Create dow (1=Monday, ..., 7=Sunday)
    # pandas weekday: 0=Monday, ..., 6=Sunday
    df['dow'] = df['parsed_date'].dt.weekday + 1
    
    # 4. Rename hourly columns
    # Identify hourly columns from source
    # Source columns look like '1:00', '2:00', ..., '23:00', '24:00:00'
    hourly_cols = [col for col in df.columns if col not in ['Segment', 'Date']]
    
    rename_map = {}
    for col in hourly_cols:
        if col == '24:00:00':
            rename_map[col] = 'pct_hourly_2400'
        else:
            # Extract hour number
            hour_str = col.split(':')[0]
            hour_int = int(hour_str)
            # Format as HHMM
            target_col = f'pct_hourly_{hour_int:02d}00'
            rename_map[col] = target_col
            
    df.rename(columns=rename_map, inplace=True)
    
    # 5. Add pct_hourly_2500 as NaN
    df['pct_hourly_2500'] = np.nan
    
    # 6. Define target columns order
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
    
    # Select and order columns
    result_df = df[target_columns]
    
    return result_df