import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse date and compute dt_strata and dow
    # Source date format is M/D/YYYY
    dt = pd.to_datetime(df['date'])
    
    # Target dt_strata format is M/D/YYYY (same as source, but ensure consistency)
    df['dt_strata'] = dt.dt.strftime('%m/%d/%Y')
    
    # Compute dow: Wed=3, Thu=4, Sun=0, Mon=1
    # pandas dayofweek: Mon=0, Tue=1, Wed=2, Thu=3, Fri=4, Sat=5, Sun=6
    # Mapping: (dayofweek + 1) % 7
    # Wed(2) -> 3, Thu(3) -> 4, Sun(6) -> 0, Mon(0) -> 1
    df['dow'] = (dt.dt.dayofweek + 1) % 7
    
    # 2. Map hourly columns
    # Define the mapping from source 12-hour format to target 24-hour format
    rename_dict = {
        '1:00 AM': 'pct_hourly_0100',
        '2:00 AM': 'pct_hourly_0200',
        '3:00 AM': 'pct_hourly_0300',
        '4:00 AM': 'pct_hourly_0400',
        '5:00 AM': 'pct_hourly_0500',
        '6:00 AM': 'pct_hourly_0600',
        '7:00 AM': 'pct_hourly_0700',
        '8:00 AM': 'pct_hourly_0800',
        '9:00 AM': 'pct_hourly_0900',
        '10:00 AM': 'pct_hourly_1000',
        '11:00 AM': 'pct_hourly_1100',
        '12:00 PM': 'pct_hourly_1200',
        '1:00 PM': 'pct_hourly_1300',
        '2:00 PM': 'pct_hourly_1400',
        '3:00 PM': 'pct_hourly_1500',
        '4:00 PM': 'pct_hourly_1600',
        '5:00 PM': 'pct_hourly_1700',
        '6:00 PM': 'pct_hourly_1800',
        '7:00 PM': 'pct_hourly_1900',
        '8:00 PM': 'pct_hourly_2000',
        '9:00 PM': 'pct_hourly_2100',
        '10:00 PM': 'pct_hourly_2200',
        '11:00 PM': 'pct_hourly_2300',
        '12:00 AM': 'pct_hourly_2400'
    }
    
    df = df.rename(columns=rename_dict)
    
    # 3. Add pct_hourly_2500 column with 0
    df['pct_hourly_2500'] = 0
    
    # 4. Define target columns in order
    target_columns = ['dt_strata', 'dow'] + [f'pct_hourly_{i:02d}00' for i in range(1, 26)]
    
    # 5. Return the transformed dataframe
    return df[target_columns]