import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    df = source.copy()
    
    # 1. Parse Date and format dt_strata
    # Source format: M/D/YYYY (e.g., 7/3/2013)
    # Target format: M/D/YYYY (e.g., 1/1/2013) - Non-zero-padded
    dt = pd.to_datetime(df['Date'])
    
    # Construct non-zero-padded date string
    df['dt_strata'] = dt.dt.month.astype(str) + '/' + dt.dt.day.astype(str) + '/' + dt.dt.year.astype(str)
    
    # 2. Calculate dow
    # Mapping observed: Tue->2, Sun->0, Mon->1
    # Python dayofweek: Mon=0, Tue=1, ..., Sun=6
    # Formula: (dayofweek + 1) % 7
    # Mon: (0+1)%7 = 1
    # Tue: (1+1)%7 = 2
    # Sun: (6+1)%7 = 0
    df['dow'] = (dt.dt.dayofweek + 1) % 7
    
    # 3. Rename hourly columns
    # Source: 1, 2, ..., 24
    # Target: pct_hourly_0100, ..., pct_hourly_2400
    rename_dict = {}
    for i in range(1, 25):
        rename_dict[str(i)] = f'pct_hourly_{i:02d}00'
    
    df = df.rename(columns=rename_dict)
    
    # 4. Add pct_hourly_2500 column with NaN
    df['pct_hourly_2500'] = np.nan
    
    # 5. Define target columns verbatim
    target_columns = ['dt_strata', 'dow'] + [f'pct_hourly_{i:02d}00' for i in range(1, 25)] + ['pct_hourly_2500']
    
    return df[target_columns]