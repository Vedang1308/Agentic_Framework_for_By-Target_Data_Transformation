import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    # Create a copy to avoid modifying the original
    df = source.copy()
    
    # 1. Parse the date column
    # The source date format is 'M/D/YYYY' (e.g., '7/3/2011')
    df['date_parsed'] = pd.to_datetime(df['date'], format='mixed')
    
    # 2. Create dt_strata column
    # Format as 'M/D/YYYY' without leading zeros
    df['dt_strata'] = df['date_parsed'].apply(lambda x: f"{x.month}/{x.day}/{x.year}")
    
    # 3. Create dow column
    # Based on sample: 1/1/2011 (Sat) -> 6, 1/2/2011 (Sun) -> 7, 1/3/2011 (Mon) -> 1
    # This corresponds to isoweekday() where Mon=1, Sun=7
    df['dow'] = df['date_parsed'].dt.isoweekday()
    
    # 4. Rename value columns to pct_hourly_XXXX
    # value1 -> pct_hourly_0100, ..., value24 -> pct_hourly_2400
    rename_mapping = {
        f'value{i}': f'pct_hourly_{i:04d}00' for i in range(1, 25)
    }
    df.rename(columns=rename_mapping, inplace=True)
    
    # 5. Add pct_hourly_2500 column with 0
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
    
    # 7. Sort by date
    # We sort by the parsed date to ensure chronological order
    df = df.sort_values(by='date_parsed').reset_index(drop=True)
    
    # 8. Select only the target columns
    result = df[target_columns]
    
    # 9. Ensure correct types
    # dow is int64, pct_hourly_2500 is int64, others are float64
    result['dow'] = result['dow'].astype('int64')
    result['pct_hourly_2500'] = result['pct_hourly_2500'].astype('int64')
    
    return result