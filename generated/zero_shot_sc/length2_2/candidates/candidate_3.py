import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # 1. Parse the date column to datetime objects to facilitate dow calculation
    # The source date format is '%m/%d/%Y' (e.g., '7/3/2011')
    df = source.copy()
    df['date_parsed'] = pd.to_datetime(df['date'], format='%m/%d/%Y')
    
    # 2. Calculate Day of Week (dow)
    # Target dow: 1=Monday, ..., 7=Sunday.
    # pandas dt.weekday returns 0=Monday, ..., 6=Sunday.
    # So we add 1.
    df['dow'] = df['date_parsed'].dt.weekday + 1
    
    # 3. Format dt_strata
    # Target format is 'M/D/YYYY' without leading zeros (e.g., '1/1/2011')
    # We construct the string manually to ensure no leading zeros and cross-platform compatibility
    df['dt_strata'] = df['date_parsed'].apply(lambda x: f"{x.month}/{x.day}/{x.year}")
    
    # 4. Rename value columns to pct_hourly columns
    # value1 -> pct_hourly_0100, ..., value24 -> pct_hourly_2400
    rename_map = {}
    for i in range(1, 25):
        old_col = f"value{i}"
        new_col = f"pct_hourly_{i:04d}"
        rename_map[old_col] = new_col
        
    df.rename(columns=rename_map, inplace=True)
    
    # 5. Add the extra column pct_hourly_2500 with value 0
    # The target schema specifies pct_hourly_2500 as int64
    df['pct_hourly_2500'] = 0
    
    # 6. Define the target columns in the exact order required
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
    
    # 7. Select and return the final DataFrame
    return df[target_columns]