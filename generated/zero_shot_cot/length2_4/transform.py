import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame into the target DataFrame format.
    
    Steps:
    1. Parse the 'Date' column into datetime objects.
    2. Create 'dt_strata' by formatting the date as 'm/d/Y'.
    3. Create 'dow' (Day of Week) where Sunday=0, Monday=1, ..., Saturday=6.
    4. Rename columns 1-24 to pct_hourly_0100 - pct_hourly_2400.
    5. Add a new column pct_hourly_2500 filled with NaN.
    6. Return the DataFrame with the specified target columns.
    """
    
    # Create a copy to avoid modifying the original
    df = source.copy()
    
    # 1. Parse Date
    df['parsed_date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
    
    # 2. Create dt_strata in format m/d/Y (no leading zeros)
    df['dt_strata'] = df['parsed_date'].apply(lambda x: f"{x.month}/{x.day}/{x.year}")
    
    # 3. Create dow (Sunday=0, Monday=1, ..., Saturday=6)
    # pandas dt.dayofweek is Monday=0, Sunday=6.
    # We want Sunday=0.
    # Mapping: 
    # Mon(0)->1, Tue(1)->2, Wed(2)->3, Thu(3)->4, Fri(4)->5, Sat(5)->6, Sun(6)->0
    # Formula: (dayofweek + 1) % 7
    df['dow'] = (df['parsed_date'].dt.dayofweek + 1) % 7
    
    # 4. Rename numeric columns 1-24 to pct_hourly_0100 - pctct_hourly_2400
    rename_map = {}
    for i in range(1, 25):
        old_col = str(i)
        new_col = f"pct_hourly_{i:04d}00" # e.g., 1 -> 0100, 24 -> 2400
        # Wait, the target columns are pct_hourly_0100, pct_hourly_0200...
        # The pattern is pct_hourly_ + 4-digit hour + 00?
        # Let's check the target columns again:
        # 'pct_hourly_0100', 'pct_hourly_0200', ... 'pct_hourly_2400'
        # It seems the hour is represented as HH00.
        # So hour 1 is 0100, hour 2 is 0200, ..., hour 24 is 2400.
        # My previous logic: f"pct_hourly_{i:04d}00" would give pct_hourly_000100 for i=1. That's wrong.
        # It should be f"pct_hourly_{i:02d}00"
        new_col = f"pct_hourly_{i:02d}00"
        rename_map[old_col] = new_col
        
    df.rename(columns=rename_map, inplace=True)
    
    # 5. Add pct_hourly_2500 column with NaN
    df['pct_hourly_2500'] = np.nan
    
    # 6. Define target columns
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
    
    # Select and return the target columns
    # Ensure dtypes are correct if necessary, but pandas usually handles float64 automatically
    result_df = df[target_columns]
    
    # Ensure dow is int64
    result_df['dow'] = result_df['dow'].astype('int64')
    
    return result_df