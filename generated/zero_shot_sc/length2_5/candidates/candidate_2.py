import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame into the target DataFrame format.
    
    Steps:
    1. Parse the 'date' column to datetime.
    2. Generate 'dt_strata' by formatting the date as '%m/%d/%Y'.
    3. Generate 'dow' (Day of Week) based on the pattern: Mon=1, ..., Sat=6, Sun=0.
    4. Rename 'Hour 1'...'Hour 24' to 'pct_hourly_0100'...'pct_hourly_2400'.
    5. Add 'pct_hourly_2500' column filled with NaN.
    6. Select and return columns in the specified order.
    """
    df = source.copy()
    
    # 1. Parse date
    # The source date format is '%m/%d/%Y'
    dt_series = pd.to_datetime(df['date'])
    
    # 2. Create dt_strata
    df['dt_strata'] = dt_series.dt.strftime('%m/%d/%Y')
    
    # 3. Create dow
    # Python weekday(): Mon=0, Tue=1, Wed=2, Thu=3, Fri=4, Sat=5, Sun=6
    # Target mapping: Mon=1, Tue=2, Wed=3, Thu=4, Fri=5, Sat=6, Sun=0
    # Formula: (weekday() + 1) % 7
    df['dow'] = (dt_series.dt.weekday() + 1) % 7
    
    # 4. Rename Hour columns
    # Hour 1 -> pct_hourly_0100, ..., Hour 24 -> pct_hourly_2400
    rename_dict = {}
    for i in range(1, 25):
        rename_dict[f'Hour {i}'] = f'pct_hourly_{i:04d}00'
    
    df = df.rename(columns=rename_dict)
    
    # 5. Add pct_hourly_2500 as NaN
    df['pct_hourly_2500'] = np.nan
    
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
    
    # Return the dataframe with only the target columns
    return df[target_columns]