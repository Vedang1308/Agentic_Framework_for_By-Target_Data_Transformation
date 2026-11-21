import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame with daily hourly data into a target DataFrame
    with day-of-week and standardized hourly percentage columns.
    """
    df = source.copy()
    
    # 1. Parse the date column to datetime to facilitate dow calculation
    # The format is %m/%d/%Y
    df['date_parsed'] = pd.to_datetime(df['date'], format='%m/%d/%Y')
    
    # 2. Create dt_strata: Format the date back to string %m/%d/%Y
    # Using dt.strftime to ensure consistent format
    df['dt_strata'] = df['date_parsed'].dt.strftime('%m/%d/%Y')
    
    # 3. Create dow: Day of week where Sunday=0, Monday=1, ..., Saturday=6
    # pandas weekday(): Monday=0, Sunday=6
    # We want Sunday=0. 
    # Formula: (weekday + 1) % 7
    # Mon (0) -> 1, Tue (1) -> 2, ..., Sat (5) -> 6, Sun (6) -> 0
    df['dow'] = (df['date_parsed'].dt.weekday + 1) % 7
    
    # 4. Rename Hour columns to pct_hourly_XXXX format
    # Map 'Hour 1' to 'pct_hourly_0100', ..., 'Hour 24' to 'pct_hourly_2400'
    rename_map = {}
    for i in range(1, 25):
        old_col = f'Hour {i}'
        new_col = f'pct_hourly_{i:02d}00'
        rename_map[old_col] = new_col
    
    df = df.rename(columns=rename_map)
    
    # 5. Add the new column pct_hourly_2500 with NaN values
    df['pct_hourly_2500'] = np.nan
    
    # 6. Define the target column order
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
    
    # 7. Select and return only the target columns
    # Note: The intermediate 'date' and 'date_parsed' columns are excluded by this selection
    return df[target_columns]