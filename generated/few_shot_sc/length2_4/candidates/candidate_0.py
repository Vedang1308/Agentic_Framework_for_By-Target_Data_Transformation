import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse Date and create dt_strata
    # Source format is M/D/YYYY, target is M/D/YYYY
    dt = pd.to_datetime(df['Date'])
    df['dt_strata'] = dt.dt.strftime('%m/%d/%Y')
    
    # 2. Calculate dow
    # Mapping observed: Sun=0, Mon=1, ..., Sat=6
    # Pandas weekday: Mon=0, ..., Sun=6
    # Formula: (weekday + 1) % 7
    df['dow'] = (dt.dt.weekday() + 1) % 7
    
    # 3. Rename hourly columns 1-24 to pct_hourly_0100 - pct_hourly_2400
    rename_dict = {}
    for i in range(1, 25):
        rename_dict[str(i)] = f'pct_hourly_{i:02d}00'
    
    df = df.rename(columns=rename_dict)
    
    # 4. Add pct_hourly_2500 column with NaN
    df['pct_hourly_2500'] = np.nan
    
    # 5. Define target columns verbatim
    target_columns = ['dt_strata', 'dow']
    for i in range(1, 26):
        target_columns.append(f'pct_hourly_{i:02d}00')
        
    return df[target_columns]