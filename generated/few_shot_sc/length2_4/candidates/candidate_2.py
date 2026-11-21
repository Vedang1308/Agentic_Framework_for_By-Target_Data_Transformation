import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse Date and compute dt_strata and dow
    dt = pd.to_datetime(df['Date'])
    df['dt_strata'] = dt.dt.strftime('%m/%d/%Y')
    
    # Calculate dow: Monday=1, ..., Saturday=6, Sunday=0
    # Python dayofweek: Monday=0, ..., Sunday=6
    # Formula: (dayofweek + 1) % 7
    df['dow'] = (dt.dt.dayofweek + 1) % 7
    
    # 2. Rename hourly columns
    # Source columns are integers 1 through 24
    rename_dict = {}
    for i in range(1, 25):
        # Source column names are likely integers or strings of integers
        # The schema lists them as 1, 2, ... so we map int i to string format
        rename_dict[i] = f'pct_hourly_{i:02d}00'
        
    df = df.rename(columns=rename_dict)
    
    # 3. Add pct_hourly_2500 column with NaN
    df['pct_hourly_2500'] = np.nan
    
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
    
    # 5. Return selected columns
    return df[target_columns]