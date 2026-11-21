import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame into the target DataFrame format.
    
    Steps:
    1. Parse the 'date' column into datetime objects.
    2. Generate 'dt_strata' by formatting the date as '%m/%d/%Y'.
    3. Generate 'dow' (Day of Week) where Monday=1, ..., Sunday=7.
    4. Rename value columns 'value1'...'value24' to 'pct_hourly_0100'...'pct_hourly_2400'.
    5. Add a constant column 'pct_hourly_2500' with value 0.
    6. Select and order columns to match the target schema.
    """
    df = source.copy()
    
    # 1. Parse date
    df['parsed_date'] = pd.to_datetime(df['date'], format='%m/%d/%Y')
    
    # 2. Create dt_strata in the required format
    df['dt_strata'] = df['parsed_date'].dt.strftime('%m/%d/%Y')
    
    # 3. Create dow: Monday=1, Tuesday=2, ..., Sunday=7
    # pandas dayofweek: Monday=0, ..., Sunday=6
    df['dow'] = df['parsed_date'].dt.dayofweek + 1
    
    # 4. Rename value columns
    rename_map = {}
    for i in range(1, 25):
        old_col = f'value{i}'
        new_col = f'pct_hourly_{i:04d}'
        rename_map[old_col] = new_col
        
    df.rename(columns=rename_map, inplace=True)
    
    # 5. Add pct_hourly_2500 column
    df['pct_hourly_2500'] = 0
    
    # 6. Define target columns in order
    target_columns = [
        'dt_strata', 'dow', 
        'pct_hourly_0100', 'pct_hourly_0200', 'pct_hourly_0300', 
        'pct_hourly_0400', 'pct_hourly_0500', 'pct_hourly_0600', 
        'pct_hourly_0700', 'pct_hourly_0800', 'pct_hourly_0900', 
        'pct_hourly_1000', 'pct_hourly_1100', 'pct_hourly_1200', 
        'pct_hourly_1300', 'pct_hourly_1400', 'pct_hourly_1500', 
        'pct_hourly_1600', 'pct_hourly_1700', 'pct_hourly_1800', 
        'pct_hourly_1900', 'pct_hourly_2000', 'pct_hourly_2100', 
        'pct_hourly_2200', 'pct_hourly_2300', 'pct_hourly_2400', 
        'pct_hourly_2500'
    ]
    
    # Select only the target columns
    df = df[target_columns]
    
    # Ensure correct data types
    # dow is int64
    df['dow'] = df['dow'].astype('int64')
    # pct_hourly_2500 is int64
    df['pct_hourly_2500'] = df['pct_hourly_2500'].astype('int64')
    # Other hourly columns are float64 (they likely are already, but ensure)
    for col in target_columns[2:-1]: # Exclude dt_strata, dow, and last int col
        df[col] = df[col].astype('float64')
        
    return df[target_columns]