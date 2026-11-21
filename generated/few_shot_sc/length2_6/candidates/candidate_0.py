import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse Date and compute dt_strata and dow
    # Source date format is M/D/YYYY
    dt_parsed = pd.to_datetime(df['Date'], format='%m/%d/%Y')
    
    # Format back to M/D/YYYY for dt_strata
    df['dt_strata'] = dt_parsed.dt.strftime('%m/%d/%Y')
    
    # Compute dow: Wed=3, Sun=0, Mon=1 implies (weekday() + 1) % 7
    # weekday(): Mon=0, Tue=1, Wed=2, Thu=3, Fri=4, Sat=5, Sun=6
    df['dow'] = (dt_parsed.dt.weekday() + 1) % 7
    
    # 2. Rename hourly columns
    # Source: 'Hr 1', 'Hr 2', ..., 'Hr 24'
    # Target: 'pct_hourly_0100', 'pct_hourly_0200', ..., 'pct_hourly_2400'
    rename_dict = {}
    for i in range(1, 25):
        rename_dict[f'Hr {i}'] = f'pct_hourly_{i:02d}00'
    
    df = df.rename(columns=rename_dict)
    
    # 3. Add pct_hourly_2500 column with 0
    df['pct_hourly_2500'] = 0
    
    # 4. Define target columns in order
    target_columns = ['dt_strata', 'dow']
    for i in range(1, 26):
        target_columns.append(f'pct_hourly_{i:02d}00')
        
    # 5. Return only target columns
    return df[target_columns]