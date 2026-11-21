import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    df = source.copy()
    
    # 1. Parse Date
    dt = pd.to_datetime(df['Date'])
    
    # 2. Create dt_strata (M/D/YYYY without leading zeros)
    # Standard strftime gives MM/DD/YYYY. We need to strip leading zeros from M and D.
    # Format: M/D/YYYY
    dt_str_raw = dt.strftime('%m/%d/%Y')
    # Replace '01/' with '1/', '02/' with '2/', etc. for month
    # And '/01/' with '/1/', etc. for day
    # Using regex is cleaner
    dt_str = dt_str_raw.str.replace(r'^0(\d)/', r'\1/') \
                         .str.replace(r'/0(\d)/', r'/\1/')
    df['dt_strata'] = dt_str
    
    # 3. Create dow (0=Sun, 1=Mon, ..., 6=Sat)
    # strftime('%w') returns string, convert to int
    df['dow'] = dt.strftime('%w').astype(int)
    
    # 4. Rename hourly columns 1-24 to pct_hourly_0100 - pct_hourly_2400
    rename_dict = {}
    for i in range(1, 25):
        rename_dict[str(i)] = f'pct_hourly_{i:02d}00'
    
    df = df.rename(columns=rename_dict)
    
    # 5. Add pct_hourly_2500 column with NaN
    df['pct_hourly_2500'] = np.nan
    
    # 6. Define target columns
    target_cols = ['dt_strata', 'dow']
    for i in range(1, 26):
        target_cols.append(f'pct_hourly_{i:02d}00')
        
    # 7. Return selected columns
    return df[target_cols]