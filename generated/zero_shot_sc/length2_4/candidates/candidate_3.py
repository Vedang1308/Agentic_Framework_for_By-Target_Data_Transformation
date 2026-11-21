import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # 1. Parse the Date column
    df = source.copy()
    df['parsed_date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
    
    # 2. Calculate dow (Day of Week)
    # Based on sample: 
    # 1/1/2013 (Tue) -> 2
    # 1/2/2013 (Wed) -> 3
    # 6/30/2013 (Sun) -> 0
    # 7/1/2013 (Mon) -> 1
    # Logic: (dayofweek + 1) % 7
    # pandas dayofweek: Mon=0, Tue=1, ..., Sun=6
    df['dow'] = (df['parsed_date'].dt.dayofweek + 1) % 7
    
    # 3. Format dt_strata
    df['dt_strata'] = df['parsed_date'].dt.strftime('%m/%d/%Y')
    
    # 4. Rename numeric columns 1-24 to pct_hourly_0100 - pct_hourly_2400
    rename_map = {}
    for i in range(1, 25):
        old_col = str(i)
        new_col = f'pct_hourly_{i:04d}00' # Wait, format is 0100, 0200...
        # The target columns are pct_hourly_0100, pct_hourly_0200...
        # Hour 1 -> 0100? Usually hour 1 is 01:00.
        # Let's check the naming convention.
        # Target: pct_hourly_0100 ... pct_hourly_2400
        # Source: 1 ... 24
        # Mapping: 1 -> 0100, 2 -> 0200, etc.
        # Format string for hour h: f'{h:02d}00'
        new_col = f'pct_hourly_{i:02d}00'
        rename_map[old_col] = new_col
        
    df.rename(columns=rename_map, inplace=True)
    
    # 5. Add pct_hourly_2500 column with NaN
    df['pct_hourly_2500'] = np.nan
    
    # 6. Define target columns in exact order
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
    
    # 7. Select and return
    return df[target_columns]