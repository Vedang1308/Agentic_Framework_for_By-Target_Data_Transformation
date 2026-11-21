import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    # Make a copy to avoid modifying the original
    df = source.copy()
    
    # 1. Parse the date column
    # The format is m/d/Y (e.g., 7/3/2011)
    df['date_parsed'] = pd.to_datetime(df['date'], format='%m/%d/%Y')
    
    # 2. Create dt_strata
    # Format back to m/d/Y string
    df['dt_strata'] = df['date_parsed'].dt.strftime('%m/%d/%Y')
    
    # 3. Calculate dow (Day of Week)
    # 1/1/2011 is Saturday -> dow 6. 
    # pandas dayofweek: Monday=0, ..., Sunday=6.
    # Saturday is 5. 5 + 1 = 6.
    # Sunday is 6. 6 + 1 = 7.
    df['dow'] = df['date_parsed'].dt.dayofweek + 1
    
    # 4. Rename value columns to pct_hourly_XXXX
    # value1 -> pct_hourly_0100
    # value2 -> pct_hourly_0200
    # ...
    # value24 -> pct_hourly_2400
    rename_map = {}
    for i in range(1, 25):
        old_col = f'value{i}'
        new_col = f'pct_hourly_{i:04d}'
        rename_map[old_col] = new_col
        
    df = df.rename(columns=rename_map)
    
    # 5. Add the dummy column pct_hourly_2500 with value 0
    df['pct_hourly_2500'] = 0
    
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
    # Ensure dtypes match if necessary, though pandas usually infers correctly
    # dow should be int64
    df['dow'] = df['dow'].astype('int64')
    # pct_hourly_2500 should be int64
    df['pct_hourly_2500'] = df['pct_hourly_2500'].astype('int64')
    
    return df[target_columns]