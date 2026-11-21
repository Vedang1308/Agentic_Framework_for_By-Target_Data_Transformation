import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the Date column to datetime
    dt = pd.to_datetime(df['Date'])
    
    # 2. Create 'dt_strata' column with format '%m/%d/%Y'
    df['dt_strata'] = dt.dt.strftime('%m/%d/%Y')
    
    # 3. Create 'dow' column (Monday=0, ..., Sunday=6)
    df['dow'] = dt.dt.dayofweek
    
    # 4. Rename hourly columns: 'Hr 1' -> 'pct_hourly_0100', ..., 'Hr 24' -> 'pct_hourly_2400'
    rename_dict = {}
    for i in range(1, 25):
        rename_dict[f'Hr {i}'] = f'pct_hourly_{i:02d}00'
    df = df.rename(columns=rename_dict)
    
    # 5. Add 'pct_hourly_2500' column filled with 0
    df['pct_hourly_2500'] = 0
    
    # 6. Define target columns in the correct order
    target_cols = ['dt_strata', 'dow']
    target_cols += [f'pct_hourly_{i:02d}00' for i in range(1, 25)]
    target_cols.append('pct_hourly_2500')
    
    # 7. Return the DataFrame with only the target columns
    return df[target_cols]