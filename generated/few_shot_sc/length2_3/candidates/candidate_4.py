import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse Date and Create dt_strata and dow
    dt = pd.to_datetime(df['date'])
    
    # Format date as M/D/YYYY (no leading zeros for single digits based on sample '1/1/2014')
    # Using apply to handle formatting explicitly to avoid locale issues with %-m
    df['dt_strata'] = dt.apply(lambda x: f"{x.month}/{x.day}/{x.year}")
    
    # Calculate dow: Sunday=0, Monday=1, ..., Saturday=6
    # pd.Timestamp.weekday() returns Monday=0, Sunday=6
    # Formula: (weekday + 1) % 7
    df['dow'] = (dt.dt.weekday() + 1) % 7
    
    # 2. Map Hourly Columns
    # Source: 1:00 AM ... 12:00 AM ... 1:00 PM ... 12:00 PM
    # Target: pct_hourly_0100 ... pct_hourly_2400
    
    col_map = {}
    
    # AM Hours: 1 AM -> 1, ..., 11 AM -> 11
    for h in range(1, 12):
        col_map[f'{h}:00 AM'] = f'pct_hourly_{h:02d}00'
        
    # 12:00 PM -> 12
    col_map['12:00 PM'] = 'pct_hourly_1200'
    
    # PM Hours: 1 PM -> 13, ..., 11 PM -> 23
    for h in range(1, 12):
        target_h = h + 12
        col_map[f'{h}:00 PM'] = f'pct_hourly_{target_h:02d}00'
        
    # 12:00 AM -> 24 (Midnight end of day)
    col_map['12:00 AM'] = 'pct_hourly_2400'
    
    df = df.rename(columns=col_map)
    
    # 3. Add pct_hourly_2500 column
    df['pct_hourly_2500'] = 0
    
    # 4. Define target columns
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
    
    # 5. Return selected columns
    return df[target_columns]