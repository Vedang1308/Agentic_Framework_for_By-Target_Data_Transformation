import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame into the target DataFrame format.
    
    Steps:
    1. Parse the 'date' column to datetime to extract the day of the week.
    2. Calculate 'dow' where Sunday=0, Monday=1, ..., Saturday=6.
    3. Rename 'date' to 'dt_strata'.
    4. Rename 'Hour 1'...'Hour 24' to 'pct_hourly_0100'...'pct_hourly_2400'.
    5. Add a new column 'pct_hourly_2500' filled with NaN.
    6. Reorder columns to match the target schema.
    """
    df = source.copy()
    
    # 1. Parse date and calculate dow
    # Using strftime('%w') gives Sunday=0, Monday=1, ..., Saturday=6
    df['dow'] = pd.to_datetime(df['date']).dt.strftime('%w').astype(int)
    
    # 2. Rename 'date' to 'dt_strata'
    df = df.rename(columns={'date': 'dt_strata'})
    
    # 3. Rename Hour columns to pct_hourly_XXXX
    rename_map = {}
    for i in range(1, 25):
        old_col = f'Hour {i}'
        new_col = f'pct_hourly_{i:04d}'
        rename_map[old_col] = new_col
    
    df = df.rename(columns=rename_map)
    
    # 4. Add pct_hourly_2500 column with NaN
    df['pct_hourly_2500'] = np.nan
    
    # 5. Define target columns in the correct order
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
    
    # 6. Select and return columns in the specified order
    return df[target_columns]