import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse date and create dt_strata and dow
    dt = pd.to_datetime(df['date'])
    df['dt_strata'] = dt.dt.strftime('%m/%d/%Y')
    # Monday=1 ... Sunday=7
    df['dow'] = dt.dt.dayofweek + 1
    
    # 2. Rename value columns to pct_hourly_XX00
    rename_dict = {}
    for i in range(1, 25):
        rename_dict[f'value{i}'] = f'pct_hourly_{i:02d}00'
    
    df = df.rename(columns=rename_dict)
    
    # 3. Add pct_hourly_2500 column with value 0
    df['pct_hourly_2500'] = 0
    
    # 4. Define target columns in exact order
    target_cols = ['dt_strata', 'dow']
    for i in range(1, 26):
        target_cols.append(f'pct_hourly_{i:02d}00')
        
    # 5. Return only the target columns
    return df[target_cols]