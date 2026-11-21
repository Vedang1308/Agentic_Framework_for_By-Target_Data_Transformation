import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse Date column
    dt = pd.to_datetime(df['Date'])
    
    # 2. Create dt_strata with format M/D/YYYY (no leading zeros for single digits)
    # First format with leading zeros, then strip them
    df['dt_strata'] = dt.dt.strftime('%m/%d/%Y')
    # Remove leading zeros from month and day
    def format_date(s):
        parts = s.split('/')
        return f"{int(parts[0])}/{int(parts[1])}/{parts[2]}"
    df['dt_strata'] = df['dt_strata'].apply(format_date)
    
    # 3. Create dow column (Monday=1, ..., Sunday=7)
    # pandas dayofweek: Monday=0, ..., Sunday=6
    df['dow'] = dt.dt.dayofweek + 1
    
    # 4. Rename hourly columns 1-24 to pct_hourly_0100 - pct_hourly_2400
    rename_dict = {}
    for i in range(1, 25):
        rename_dict[str(i)] = f'pct_hourly_{i:02d}00'
    
    df = df.rename(columns=rename_dict)
    
    # 5. Add pct_hourly_2500 column with NaN
    df['pct_hourly_2500'] = np.nan
    
    # 6. Define target columns in exact order
    target_columns = ['dt_strata', 'dow'] + [f'pct_hourly_{i:02d}00' for i in range(1, 26)]
    
    # 7. Return the transformed dataframe
    return df[target_columns]