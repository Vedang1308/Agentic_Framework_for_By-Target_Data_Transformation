import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    df = source.copy()
    
    # 1. Parse the date column
    # Source format is M/D/YYYY, e.g., '7/3/2014'
    dt = pd.to_datetime(df['date'])
    
    # 2. Create dt_strata in format M/D/YYYY
    df['dt_strata'] = dt.dt.strftime('%m/%d/%Y')
    
    # 3. Calculate dow
    # Mapping observed: Mon=1, Tue=2, Wed=3, Thu=4, Fri=5, Sat=6, Sun=0
    # pandas dayofweek: Mon=0, ..., Sun=6
    # Formula: (dayofweek + 1) % 7
    df['dow'] = (dt.dt.dayofweek + 1) % 7
    
    # 4. Map hour columns
    # Source: '1:00 AM'...'11:00 AM', '12:00 PM', '1:00 PM'...'11:00 PM', '12:00 AM'
    # Target: pct_hourly_0100 ... pct_hourly_2400
    
    rename_dict = {}
    
    # 1:00 AM to 11:00 AM -> Hours 1 to 11
    for h in range(1, 12):
        rename_dict[f'{h}:00 AM'] = f'pct_hourly_{h:02d}00'
        
    # 12:00 PM -> Hour 12
    rename_dict['12:00 PM'] = 'pct_hourly_1200'
    
    # 1:00 PM to 11:00 PM -> Hours 13 to 23
    for h in range(1, 12):
        rename_dict[f'{h}:00 PM'] = f'pct_hourly_{h+12:02d}00'
        
    # 12:00 AM (Midnight) -> Hour 24
    rename_dict['12:00 AM'] = 'pct_hourly_2400'
    
    df = df.rename(columns=rename_dict)
    
    # 5. Add pct_hourly_2500 column with 0
    df['pct_hourly_2500'] = 0
    
    # 6. Define target columns
    target_columns = ['dt_strata', 'dow']
    target_columns += [f'pct_hourly_{i:02d}00' for i in range(1, 25)]
    target_columns.append('pct_hourly_2500')
    
    # Ensure correct column order and types if necessary (types usually inferred)
    # The problem asks for int64 for dow and pct_hourly_2500, float64 for others.
    # Pandas will handle float64 automatically.
    df['dow'] = df['dow'].astype('int64')
    df['pct_hourly_2500'] = df['pct_hourly_2500'].astype('int64')
    
    return df[target_columns]