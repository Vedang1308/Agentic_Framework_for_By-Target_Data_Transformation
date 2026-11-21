import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame into the target DataFrame format.
    
    Steps:
    1. Parse the 'Date' column into datetime objects.
    2. Generate 'dt_strata' in 'MM/DD/YY' format.
    3. Generate 'dow' as integer (1=Monday, ..., 7=Sunday).
    4. Rename hourly columns from '1:00', ..., '24:00:00' to 'pct_hourly_0100', ..., 'pct_hourly_2400'.
    5. Add 'pct_hourly_2500' column filled with NaN.
    6. Select and order columns to match target schema.
    """
    df = source.copy()
    
    # 1. Parse Date
    # The format is '%a %m/%d/%Y' e.g., 'Thu 10/01/2009'
    df['parsed_date'] = pd.to_datetime(df['Date'], format='%a %m/%d/%Y')
    
    # 2. Create dt_strata (MM/DD/YY)
    df['dt_strata'] = df['parsed_date'].dt.strftime('%m/%d/%y')
    
    # 3. Create dow (1=Monday, ..., 7=Sunday)
    # pandas weekday(): Monday=0, ..., Sunday=6
    df['dow'] = df['parsed_date'].dt.weekday() + 1
    
    # 4. Rename hourly columns
    # Source columns are '1:00', '2:00', ..., '23:00', '24:00:00'
    # Target columns are 'pct_hourly_0100', ..., 'pct_hourly_2400'
    
    rename_map = {}
    
    # Map 1:00 to 23:00
    for h in range(1, 24):
        src_col = f"{h}:00"
        if src_col in df.columns:
            tgt_col = f"pct_hourly_{h:04d}"
            rename_map[src_col] = tgt_col
            
    # Map 24:00:00
    if '24:00:00' in df.columns:
        rename_map['24:00:00'] = 'pct_hourly_2400'
        
    df.rename(columns=rename_map, inplace=True)
    
    # 5. Add pct_hourly_2500 as NaN
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
    
    # Ensure all target columns exist (some might be missing if source didn't have them, though unlikely based on schema)
    for col in target_columns:
        if col not in df.columns:
            df[col] = np.nan
            
    # Return the dataframe with columns in the correct order
    return df[target_columns]