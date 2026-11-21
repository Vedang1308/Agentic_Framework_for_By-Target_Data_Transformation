import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse Date and create dt_strata
    # Source format is %m/%d/%Y, target is also %m/%d/%Y
    dt = pd.to_datetime(df['Date'], format='%m/%d/%Y')
    df['dt_strata'] = dt.dt.strftime('%m/%d/%Y')
    
    # 2. Calculate dow
    # Mapping observed: Mon=1, Tue=2, ..., Sat=6, Sun=0
    # Python weekday(): Mon=0, ..., Sun=6
    # Formula: (weekday + 1) % 7
    df['dow'] = (dt.dt.weekday() + 1) % 7
    
    # 3. Rename hourly columns
    # Source: 'Hr 1' ... 'Hr 24'
    # Target: 'pct_hourly_0100' ... 'pct_hourly_2400'
    rename_dict = {}
    for i in range(1, 25):
        src_col = f'Hr {i}'
        tgt_col = f'pct_hourly_{i:02d}00'
        rename_dict[src_col] = tgt_col
    
    df = df.rename(columns=rename_dict)
    
    # 4. Add pct_hourly_2500 column with 0s
    df['pct_hourly_2500'] = 0
    
    # 5. Define target columns verbatim
    target_cols = ['dt_strata', 'dow'] + [f'pct_hourly_{i:02d}00' for i in range(1, 26)]
    
    return df[target_cols]