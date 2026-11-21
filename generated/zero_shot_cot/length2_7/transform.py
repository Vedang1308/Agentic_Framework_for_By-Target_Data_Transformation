import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame into the target DataFrame format.
    
    Steps:
    1. Parse the 'Date' column.
    2. Generate 'dt_strata' (MM/DD/YY) and 'dow' (1=Mon, ..., 7=Sun).
    3. Rename hourly columns from 'H:00' format to 'pct_hourly_HH00'.
    4. Add 'pct_hourly_2500' as NaN.
    5. Return the DataFrame with the specific target column order.
    """
    
    # 1. Parse Date
    # Source format: '%a %m/%d/%Y' e.g., 'Thu 10/01/2009'
    df = source.copy()
    df['parsed_date'] = pd.to_datetime(df['Date'], format='%a %m/%d/%Y')
    
    # 2. Create dt_strata and dow
    # dt_strata format: '%m/%d/%y' e.g., '10/01/09'
    df['dt_strata'] = df['parsed_date'].dt.strftime('%m/%d/%y')
    
    # dow: 1 for Monday, 7 for Sunday
    # pandas dayofweek: 0=Mon, 6=Sun
    df['dow'] = df['parsed_date'].dt.dayofweek + 1
    
    # 3. Rename hourly columns
    # Source columns: '1:00', '2:00', ..., '24:00:00'
    # Target columns: 'pct_hourly_0100', ..., 'pct_hourly_2400'
    
    # Identify source hourly columns
    # They are all columns except 'Segment', 'Date'
    # Or we can construct the expected source names
    source_hourly_cols = []
    for h in range(1, 25):
        if h == 24:
            source_hourly_cols.append('24:00:00')
        else:
            source_hourly_cols.append(f'{h}:00')
            
    target_hourly_cols = []
    for h in range(1, 25):
        target_hourly_cols.append(f'pct_hourly_{h:02d}00')
        
    # Create a mapping dict
    col_map = dict(zip(source_hourly_cols, target_hourly_cols))
    
    # Rename
    df = df.rename(columns=col_map)
    
    # 4. Add pct_hourly_2500
    df['pct_hourly_2500'] = np.nan
    
    # 5. Define final target columns
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
    
    # Select and return
    return df[target_columns]