import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse Date and compute dt_strata and dow
    # Source Date format is '%m/%d/%Y'
    dt = pd.to_datetime(df['Date'])
    
    # Format dt_strata as '%m/%d/%Y'
    df['dt_strata'] = dt.dt.strftime('%m/%d/%Y')
    
    # Compute dow: Sunday=0, Monday=1, ..., Saturday=6
    # pandas weekday: Mon=0, ..., Sun=6
    # Mapping: (weekday + 1) % 7 yields Sun=0, Mon=1, ..., Sat=6
    df['dow'] = (dt.dt.weekday + 1) % 7
    
    # 2. Rename hourly columns
    rename_dict = {}
    for i in range(1, 25):
        src_col = f'Hr {i}'
        tgt_col = f'pct_hourly_{i:02d}00'
        if src_col in df.columns:
            rename_dict[src_col] = tgt_col
            
    df = df.rename(columns=rename_dict)
    
    # 3. Add pct_hourly_2500 column with 0s
    df['pct_hourly_2500'] = 0
    
    # 4. Define target columns in exact order
    target_cols = ['dt_strata', 'dow']
    for i in range(1, 26):
        target_cols.append(f'pct_hourly_{i:02d}00')
        
    # 5. Return the transformed dataframe
    return df[target_cols]