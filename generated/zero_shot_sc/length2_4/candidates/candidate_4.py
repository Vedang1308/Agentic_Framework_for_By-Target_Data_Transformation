import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    # Make a copy to avoid SettingWithCopy warnings
    df = source.copy()
    
    # 1. Parse the Date column to datetime
    df['parsed_date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
    
    # 2. Calculate Day of Week (dow)
    # Target mapping: Sun=0, Mon=1, ..., Sat=6
    # pd.Series.dt.weekday returns Mon=0, ..., Sun=6
    # So we use (weekday + 1) % 7
    df['dow'] = (df['parsed_date'].dt.weekday + 1) % 7
    
    # 3. Create dt_strata column
    # Format to M/D/YYYY without leading zeros
    # First format to MM/DD/YYYY, then strip leading zeros from month and day
    df['dt_strata'] = df['parsed_date'].dt.strftime('%m/%d/%Y').str.lstrip('0')
    
    # 4. Rename hourly columns
    # Source columns 1-24 map to pct_hourly_0100 - pct_hourly_2400
    rename_map = {}
    for i in range(1, 25):
        old_col = str(i)
        new_col = f'pct_hourly_{i:02d}00'
        rename_map[old_col] = new_col
        
    df.rename(columns=rename_map, inplace=True)
    
    # 5. Add pct_hourly_2500 column with NaN
    df['pct_hourly_2500'] = np.nan
    
    # 6. Select and order columns
    # Define the target columns in the exact order required
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
    
    # 7. Sort by date to ensure chronological order (matching target sample)
    df = df.sort_values(by='parsed_date').reset_index(drop=True)
    
    # 8. Return only the target columns
    return df[target_columns]