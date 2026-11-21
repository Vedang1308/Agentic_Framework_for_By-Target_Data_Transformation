import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame into the target DataFrame format.
    
    Steps:
    1. Parse the 'Date' column into datetime objects.
    2. Extract 'dt_strata' (MM/DD/YY) and 'dow' (1=Mon...7=Sun).
    3. Rename hourly columns from 'H:MM' format to 'pct_hourly_HHMM' format.
    4. Add 'pct_hourly_2500' column filled with NaN.
    5. Select and order columns to match target schema.
    """
    
    # 1. Parse Date
    # The source date format is '%a %m/%d/%Y' (e.g., 'Thu 10/01/2009')
    df = source.copy()
    df['parsed_date'] = pd.to_datetime(df['Date'], format='%a %m/%d/%Y')
    
    # 2. Create dt_strata and dow
    # dt_strata format: MM/DD/YY
    df['dt_strata'] = df['parsed_date'].dt.strftime('%m/%d/%y')
    
    # dow: 1=Monday, ..., 7=Sunday
    # pandas dayofweek: 0=Monday, ..., 6=Sunday
    df['dow'] = df['parsed_date'].dt.dayofweek + 1
    
    # 3. Rename hourly columns
    # Source columns: '1:00', '2:00', ..., '23:00', '24:00:00'
    # Target columns: 'pct_hourly_0100', ..., 'pct_hourly_2400'
    
    rename_map = {}
    for i in range(1, 25):
        if i < 10:
            src_col = f"{i}:00"
        else:
            src_col = f"{i}:00"
        
        # Handle the specific last column name '24:00:00' if it differs from pattern
        # Looking at source schema: '24:00:00'
        if i == 24:
            src_col = "24:00:00"
            
        tgt_col = f"pct_hourly_{i:02d}00"
        rename_map[src_col] = tgt_col
        
    df.rename(columns=rename_map, inplace=True)
    
    # 4. Add the 25th hour column which is NaN in the target
    df['pct_hourly_2500'] = np.nan
    
    # 5. Define target columns in exact order
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
    
    # Return only the required columns
    return df[target_columns]