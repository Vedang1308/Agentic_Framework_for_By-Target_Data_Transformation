import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame into the target DataFrame format.
    - Parses dates and extracts day of week.
    - Renames hourly columns 1-24 to pct_hourly_0100 - pct_hourly_2400.
    - Adds a pct_hourly_2500 column filled with NaN.
    """
    # 1. Parse the Date column
    # Source format is '%m/%d/%Y'
    df = source.copy()
    df['parsed_date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
    
    # 2. Create dt_strata (formatted back to string)
    df['dt_strata'] = df['parsed_date'].dt.strftime('%m/%d/%Y')
    
    # 3. Calculate dow
    # Mapping observed:
    # Tue (1/1/2013) -> 2
    # Wed (1/2/2013) -> 3
    # Sun (6/30/2013) -> 0
    # Mon (7/1/2013) -> 1
    # Python weekday(): Mon=0, Tue=1, Wed=2, Thu=3, Fri=4, Sat=5, Sun=6
    # Formula: (weekday() + 1) % 7
    df['dow'] = (df['parsed_date'].dt.weekday + 1) % 7
    
    # 4. Rename hourly columns
    # Source columns are integers 1 through 24 (as strings or ints in header)
    # Target columns are pct_hourly_0100 through pct_hourly_2400
    
    # Identify numeric columns
    numeric_cols = [str(i) for i in range(1, 25)]
    
    # Create mapping dict
    rename_map = {}
    for col in numeric_cols:
        if col in df.columns:
            hour_num = int(col)
            # Format: pct_hourly_HHMM where HH is 2 digits, MM is 00
            # e.g., 1 -> pct_hourly_0100
            new_col_name = f"pct_hourly_{hour_num:02d}00"
            rename_map[col] = new_col_name
            
    df.rename(columns=rename_map, inplace=True)
    
    # 5. Add the 25th hour column with NaN
    df['pct_hourly_2500'] = np.nan
    
    # 6. Define the target columns in the exact order
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
    
    # 7. Select and return only the target columns
    # Ensure types are correct if necessary, but pandas usually handles float/int conversion
    # The target dow is int64.
    df['dow'] = df['dow'].astype('int64')
    
    return df[target_columns]