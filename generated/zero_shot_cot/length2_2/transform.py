import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the date column
    # The source date format is '%m/%d/%Y'
    df['date_parsed'] = pd.to_datetime(df['date'], format='%m/%d/%Y')
    
    # 2. Create dt_strata
    # Format back to '%m/%d/%Y' as seen in target sample
    df['dt_strata'] = df['date_parsed'].dt.strftime('%m/%d/%Y')
    
    # 3. Create dow (Day of Week)
    # Pandas dayofweek: 0=Monday, ..., 6=Sunday
    # Target sample: 1/1/2011 (Saturday) -> 6, 1/2/2011 (Sunday) -> 7, 1/3/2011 (Monday) -> 1
    # This implies 1=Monday, ..., 7=Sunday
    df['dow'] = df['date_parsed'].dt.dayofweek + 1
    
    # 4. Rename value columns to pct_hourly columns
    # value1 -> pct_hourly_0100, ..., value24 -> pct_hourly_2400
    rename_map = {}
    for i in range(1, 25):
        old_col = f'value{i}'
        new_col = f'pct_hourly_{i:04d}'
        rename_map[old_col] = new_col
    
    df = df.rename(columns=rename_map)
    
    # 5. Add pct_hourly_2500 column
    # Based on target sample, this is always 0 and is an integer
    df['pct_hourly_2500'] = 0
    
    # 6. Define target columns in the correct order
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
    
    # 7. Select and return the final dataframe
    # Ensure dt_strata is object (string), dow is int64, and hourly cols are float64 (except 2500)
    df['dt_strata'] = df['dt_strata'].astype('object')
    df['dow'] = df['dow'].astype('int64')
    df['pct_hourly_2500'] = df['pct_hourly_2500'].astype('int64')
    
    # The hourly columns should be float64. They are already float64 from source.
    
    return df[target_columns]