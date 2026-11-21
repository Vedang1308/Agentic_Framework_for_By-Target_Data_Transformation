import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the date column
    dt = pd.to_datetime(df['date'])
    
    # 2. Create dt_strata with format M/D/YYYY (no leading zeros)
    # Using strftime with %-m and %-d is platform dependent (Unix vs Windows)
    # Safer approach: construct string from components
    df['dt_strata'] = dt.dt.apply(lambda t: f"{t.month}/{t.day}/{t.year}")
    
    # 3. Calculate dow (Monday=1, ..., Sunday=7)
    df['dow'] = dt.dt.dayofweek + 1
    
    # 4. Rename value columns to pct_hourly_XXXX
    rename_map = {}
    for i in range(1, 25):
        src_col = f'value{i}'
        tgt_col = f'pct_hourly_{i:02d}00'
        if src_col in df.columns:
            rename_map[src_col] = tgt_col
            
    df = df.rename(columns=rename_map)
    
    # 5. Add pct_hourly_2500 column filled with 0
    df['pct_hourly_2500'] = 0
    
    # 6. Define target columns verbatim
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
    
    # 7. Return only the target columns
    return df[target_columns]