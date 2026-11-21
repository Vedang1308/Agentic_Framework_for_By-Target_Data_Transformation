import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse Date column
    # Source format: 'Thu 10/01/2009' (%a %m/%d/%Y)
    # We can parse this directly using pd.to_datetime
    dt = pd.to_datetime(df['Date'])
    
    # 2. Create dt_strata column
    # Target format: '10/01/2009' (%m/%d/%Y)
    df['dt_strata'] = dt.dt.strftime('%m/%d/%Y')
    
    # 3. Create dow column
    # Target: Monday=1, ..., Sunday=7
    # pandas dayofweek: Monday=0, ..., Sunday=6
    df['dow'] = dt.dt.dayofweek + 1
    
    # 4. Rename hourly columns
    # Source: '1:00' ... '23:00', '24:00:00'
    # Target: 'pct_hourly_0100' ... 'pct_hourly_2300', 'pct_hourly_2400'
    rename_dict = {}
    for i in range(1, 24):
        rename_dict[f'{i}:00'] = f'pct_hourly_{i:02d}00'
    
    # Handle the 24th hour specifically as it has seconds in source
    if '24:00:00' in df.columns:
        rename_dict['24:00:00'] = 'pct_hourly_2400'
    elif '24:00' in df.columns:
        rename_dict['24:00'] = 'pct_hourly_2400'
        
    df = df.rename(columns=rename_dict)
    
    # 5. Add pct_hourly_2500 column
    # The target sample shows NaN for this column.
    df['pct_hourly_2500'] = float('nan')
    
    # 6. Define target columns in order
    target_columns = ['dt_strata', 'dow'] + [f'pct_hourly_{i:02d}00' for i in range(1, 26)]
    
    return df[target_columns]