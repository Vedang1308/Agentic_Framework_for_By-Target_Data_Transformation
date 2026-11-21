import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    df = source.copy()
    
    # 1. Parse date
    dt = pd.to_datetime(df['date'])
    
    # 2. Format dt_strata as M/D/YYYY (no leading zeros)
    # First format with leading zeros, then strip them
    df['dt_strata'] = dt.dt.strftime('%m/%d/%Y').apply(lambda x: '/'.join([str(int(p)) for p in x.split('/')]))
    
    # 3. Calculate dow (Monday=1, Sunday=7)
    df['dow'] = dt.dt.dayofweek + 1
    
    # 4. Rename value columns to pct_hourly_XXXX
    rename_dict = {}
    for i in range(1, 25):
        rename_dict[f'value{i}'] = f'pct_hourly_{i:02d}00'
    df = df.rename(columns=rename_dict)
    
    # 5. Add pct_hourly_2500 column with 0
    df['pct_hourly_2500'] = 0
    
    # 6. Define target columns
    target_columns = ['dt_strata', 'dow'] + [f'pct_hourly_{i:02d}00' for i in range(1, 25)] + ['pct_hourly_2500']
    
    # 7. Return selected columns
    return df[target_columns]