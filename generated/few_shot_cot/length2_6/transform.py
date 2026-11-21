import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse Date and create dt_strata
    # Source format is M/D/YYYY, target is M/D/YYYY. 
    # We parse to datetime to extract DOW, then format back to string.
    dt = pd.to_datetime(df['Date'])
    df['dt_strata'] = dt.dt.strftime('%m/%d/%Y')
    
    # 2. Compute DOW
    # Based on samples: Wed=3, Thu=4, Sun=0, Mon=1.
    # This matches strftime('%w') where Sunday=0, Monday=1, ..., Saturday=6.
    df['dow'] = dt.dt.strftime('%w').astype(int)
    
    # 3. Rename Hour columns
    # Source: 'Hr 1', 'Hr 2', ..., 'Hr 24'
    # Target: 'pct_hourly_0100', 'pct_hourly_0200', ..., 'pct_hourly_2400'
    rename_dict = {}
    for i in range(1, 25):
        src_col = f'Hr {i}'
        tgt_col = f'pct_hourly_{i:02d}00'
        if src_col in df.columns:
            rename_dict[src_col] = tgt_col
            
    df = df.rename(columns=rename_dict)
    
    # 4. Add pct_hourly_2500 column filled with 0
    df['pct_hourly_2500'] = 0
    
    # 5. Define target columns in exact order
    target_cols = ['dt_strata', 'dow']
    for i in range(1, 26):
        target_cols.append(f'pct_hourly_{i:02d}00')
        
    # 6. Return the transformed dataframe
    return df[target_cols]