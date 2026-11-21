import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse Date column
    # Source format: 'Thu 10/01/2009' -> '%a %m/%d/%Y'
    # We can parse this directly.
    dt = pd.to_datetime(df['Date'], format='%a %m/%d/%Y')
    
    # 2. Create dt_strata: 'MM/DD/YY' or 'MM/DD/YYYY'? 
    # Target sample: '01/01/03'. This is %m/%d/%y (2-digit year).
    # Let's verify with another row: '09/27/09' -> %m/%d/%y.
    df['dt_strata'] = dt.dt.strftime('%m/%d/%y')
    
    # 3. Create dow: Monday=1, ..., Sunday=7
    df['dow'] = dt.dt.dayofweek + 1
    
    # 4. Rename hourly columns
    # Source: '1:00' ... '23:00', '24:00:00'
    # Target: 'pct_hourly_0100' ... 'pct_hourly_2300', 'pct_hourly_2400'
    rename_dict = {}
    for i in range(1, 24):
        rename_dict[f'{i}:00'] = f'pct_hourly_{i:02d}00'
    
    # Handle the 24th hour specifically as it has seconds in source
    rename_dict['24:00:00'] = 'pct_hourly_2400'
    
    df = df.rename(columns=rename_dict)
    
    # 5. Add pct_hourly_2500 column
    # In the target sample, this column is NaN.
    df['pct_hourly_2500'] = float('nan')
    
    # 6. Define target columns in exact order
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