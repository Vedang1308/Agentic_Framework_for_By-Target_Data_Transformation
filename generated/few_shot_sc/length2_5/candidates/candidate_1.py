import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the date column and format it
    # Source format: M/D/YYYY (e.g., '7/3/2015')
    # Target format: M/D/YYYY (e.g., '1/1/2015')
    dt = pd.to_datetime(df['date'])
    df['dt_strata'] = dt.dt.strftime('%m/%d/%Y')
    
    # 2. Calculate Day of Week (DOW)
    # Mapping observed: 
    # Thursday (1/1/2015) -> 4
    # Friday (1/2/2015) -> 5
    # Saturday (1/3/2015) -> 6
    # Sunday (1/4/2015) -> 0
    # Monday (6/29/2015) -> 1
    # This corresponds to (weekday() + 1) % 7
    # where weekday() is Mon=0, Tue=1, ..., Sun=6
    df['dow'] = (dt.dt.weekday() + 1) % 7
    
    # 3. Rename hourly columns
    # Source: 'Hour 1' ... 'Hour 24'
    # Target: 'pct_hourly_0100' ... 'pct_hourly_2400'
    rename_dict = {}
    for i in range(1, 25):
        rename_dict[f'Hour {i}'] = f'pct_hourly_{i:02d}00'
    
    df = df.rename(columns=rename_dict)
    
    # 4. Add the missing column 'pct_hourly_2500' with NaN
    df['pct_hourly_2500'] = float('nan')
    
    # 5. Select and order the target columns
    target_columns = ['dt_strata', 'dow'] + [f'pct_hourly_{i:02d}00' for i in range(1, 26)]
    
    return df[target_columns]