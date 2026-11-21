import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the date column
    # The source date format is '%m/%d/%Y' (e.g., '7/3/2011')
    dt = pd.to_datetime(df['date'])
    
    # 2. Create dt_strata with non-zero-padded format (e.g., '1/1/2011')
    # Using component-wise string construction to ensure cross-platform compatibility
    # and match the exact 'M/D/YYYY' format seen in the target sample.
    df['dt_strata'] = (
        dt.dt.month.astype(str) + '/' + 
        dt.dt.day.astype(str) + '/' + 
        dt.dt.year.astype(str)
    )
    
    # 3. Calculate dow (Day of Week)
    # Target sample: 1/1/2011 (Saturday) -> 6, 1/2/2011 (Sunday) -> 7, 1/3/2011 (Monday) -> 1
    # pandas dayofweek: Monday=0, ..., Sunday=6
    # So, dow = dayofweek + 1
    df['dow'] = dt.dt.dayofweek + 1
    
    # 4. Rename value columns to pct_hourly columns
    # value1 -> pct_hourly_0100
    # value2 -> pct_hourly_0200
    # ...
    # value24 -> pct_hourly_2400
    rename_dict = {}
    for i in range(1, 25):
        old_col = f'value{i}'
        new_col = f'pct_hourly_{i:02d}00'
        rename_dict[old_col] = new_col
        
    df = df.rename(columns=rename_dict)
    
    # 5. Add the 25th hourly column which is always 0
    df['pct_hourly_2500'] = 0
    
    # 6. Define target columns in the exact order specified
    target_columns = ['dt_strata', 'dow'] + [f'pct_hourly_{i:02d}00' for i in range(1, 26)]
    
    # 7. Return the dataframe with only the target columns
    return df[target_columns]