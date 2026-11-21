import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame into the target DataFrame.
    
    Steps:
    1. Parse the 'date' column to extract the day of week.
    2. Create 'dow' column (1=Monday, ..., 7=Sunday).
    3. Rename 'date' to 'dt_strata'.
    4. Rename 'value1'...'value24' to 'pct_hourly_0100'...'pct_hourly_2400'.
    5. Add 'pct_hourly_2500' column with value 0.
    6. Select and order columns to match target schema.
    """
    
    # Make a copy to avoid modifying the original
    df = source.copy()
    
    # Parse date to datetime object to calculate day of week
    # The format is '%m/%d/%Y'
    df['date_dt'] = pd.to_datetime(df['date'], format='%m/%d/%Y')
    
    # Calculate Day of Week: Monday=1, ..., Sunday=7
    # pandas dayofweek: Monday=0, ..., Sunday=6
    df['dow'] = df['date_dt'].dt.dayofweek + 1
    df['dow'] = df['dow'].astype('int64')
    
    # Rename 'date' to 'dt_strata'
    # We can keep the original string if it's already in the correct format
    df['dt_strata'] = df['date']
    
    # Define mapping for value columns
    value_col_mapping = {
        f'value{i}': f'pct_hourly_{i:04d}' 
        for i in range(1, 25)
    }
    
    # Rename the value columns
    df = df.rename(columns=value_col_mapping)
    
    # Add the 25th hourly column with value 0
    df['pct_hourly_2500'] = 0
    df['pct_hourly_2500'] = df['pct_hourly_2500'].astype('int64')
    
    # Define target columns in order
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
    
    # Select only the target columns
    df = df[target_columns]
    
    # Ensure dt_strata is object/string type
    df['dt_strata'] = df['dt_strata'].astype('object')
    
    return df