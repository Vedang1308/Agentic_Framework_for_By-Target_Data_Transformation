import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame with hourly data into a target DataFrame
    with stratified date, day of week, and renamed hourly percentage columns.
    """
    # Create a copy to avoid modifying the original
    df = source.copy()
    
    # 1. Parse the date column to extract day of week and format for dt_strata
    # The source date format is M/D/YYYY (e.g., '7/3/2015')
    df['parsed_date'] = pd.to_datetime(df['date'], format='%m/%d/%Y')
    
    # 2. Create dt_strata in format M/D/YYYY (no leading zeros)
    # Using apply to ensure cross-platform consistency with no leading zeros
    df['dt_strata'] = df['parsed_date'].apply(lambda x: f"{x.month}/{x.day}/{x.year}")
    
    # 3. Create dow (Day of Week)
    # Monday=0, Sunday=6 based on target sample (1/1/2015 is Thursday -> 4, 1/4/2015 is Sunday -> 0)
    df['dow'] = df['parsed_date'].dt.weekday
    
    # 4. Rename Hour columns to pct_hourly_NN00
    # Map 'Hour 1' -> 'pct_hourly_0100', ..., 'Hour 24' -> 'pct_hourly_2400'
    rename_map = {}
    for col in df.columns:
        if col.startswith('Hour '):
            try:
                hour_num = int(col.split(' ')[1])
                new_col_name = f"pct_hourly_{hour_num:02d}00"
                rename_map[col] = new_col_name
            except (IndexError, ValueError):
                pass # Ignore if parsing fails
    
    df.rename(columns=rename_map, inplace=True)
    
    # 5. Add pct_hourly_2500 column with NaN values
    df['pct_hourly_2500'] = np.nan
    
    # 6. Define target columns in the required order
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
    # Ensure all columns exist before selecting
    for col in target_columns:
        if col not in df.columns:
            df[col] = np.nan
            
    return df[target_columns]