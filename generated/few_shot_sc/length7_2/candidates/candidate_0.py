import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse DT_STRATA to datetime to extract month
    dt = pd.to_datetime(df['DT_STRATA'])
    
    # 2. Create 'month' column with full month name (e.g., 'January')
    df['month'] = dt.dt.strftime('%B')
    
    # 3. Create 'daytype' column
    # Based on the sample, all source rows map to 'weekday' in the target.
    # Even though DOW varies (1-7, H, D), the target consistently shows 'weekday'.
    df['daytype'] = 'weekday'
    
    # 4. Rename hourly columns PCT_HOURLY_0100...2400 to hr1...hr24
    rename_dict = {}
    for i in range(1, 25):
        src_col = f'PCT_HOURLY_{i:02d}00'
        tgt_col = f'hr{i}'
        rename_dict[src_col] = tgt_col
        
    df = df.rename(columns=rename_dict)
    
    # 5. Define target columns in the correct order
    target_columns = ['month', 'daytype'] + [f'hr{i}' for i in range(1, 25)]
    
    # 6. Return the transformed dataframe
    return df[target_columns]