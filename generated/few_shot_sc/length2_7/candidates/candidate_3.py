import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse Date and create dt_strata and dow
    # Source Date format: 'Thu 10/01/2009' -> '%a %m/%d/%Y'
    dt = pd.to_datetime(df['Date'], format='%a %m/%d/%Y')
    
    # Target dt_strata format: '01/01/03' -> '%m/%d/%y'
    df['dt_strata'] = dt.dt.strftime('%m/%d/%y')
    
    # Target dow: Monday=1 ... Sunday=7
    # pandas dayofweek: Monday=0 ... Sunday=6
    df['dow'] = dt.dt.dayofweek + 1
    
    # 2. Rename hourly columns
    # Source: '1:00' ... '23:00', '24:00:00'
    # Target: 'pct_hourly_0100' ... 'pct_hourly_2300', 'pct_hourly_2400'
    rename_dict = {}
    for i in range(1, 24):
        rename_dict[f'{i}:00'] = f'pct_hourly_{i:02d}00'
    # Handle the specific 24:00:00 case
    if '24:00:00' in df.columns:
        rename_dict['24:00:00'] = 'pct_hourly_2400'
    elif '24:00' in df.columns:
        rename_dict['24:00'] = 'pct_hourly_2400'
        
    df = df.rename(columns=rename_dict)
    
    # 3. Add pct_hourly_2500 column
    # Based on target sample, this column is NaN
    df['pct_hourly_2500'] = float('nan')
    
    # 4. Define target columns verbatim
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
    
    return df[target_columns]