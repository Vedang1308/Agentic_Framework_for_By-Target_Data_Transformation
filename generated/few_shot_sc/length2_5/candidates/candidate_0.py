import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse date and format dt_strata
    # Source 'date' is '%m/%d/%Y'. Target 'dt_strata' is '%m/%d/%Y'.
    # We parse to datetime to ensure correctness, then format back.
    dt = pd.to_datetime(df['date'])
    df['dt_strata'] = dt.dt.strftime('%m/%d/%Y')
    
    # 2. Compute dow
    # Mapping observed: Mon=1, Tue=2, ..., Sat=6, Sun=0
    # pandas dayofweek: Mon=0, ..., Sun=6
    # Formula: (dayofweek + 1) % 7
    df['dow'] = (dt.dt.dayofweek + 1) % 7
    
    # 3. Rename hourly columns
    # Source: 'Hour 1' ... 'Hour 24'
    # Target: 'pct_hourly_0100' ... 'pct_hourly_2400'
    rename_dict = {}
    for i in range(1, 25):
        src_col = f'Hour {i}'
        tgt_col = f'pct_hourly_{i:02d}00'
        if src_col in df.columns:
            rename_dict[src_col] = tgt_col
            
    df = df.rename(columns=rename_dict)
    
    # 4. Add pct_hourly_2500 column if not present
    # Target schema includes pct_hourly_2500, which is NaN in samples.
    if 'pct_hourly_2500' not in df.columns:
        df['pct_hourly_2500'] = np.nan
        
    # 5. Define target columns and return
    target_columns = ['dt_strata', 'dow'] + [f'pct_hourly_{i:02d}00' for i in range(1, 26)]
    
    return df[target_columns]