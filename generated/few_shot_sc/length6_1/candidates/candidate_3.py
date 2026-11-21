import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Transform DT_STRATA to Date column with format MM/DD/YYYY
    dt = pd.to_datetime(df['DT_STRATA'])
    df['Date'] = dt.dt.strftime('%m/%d/%Y')
    
    # 2. Rename hourly columns from PCT_HOURLY_HH00 to Hr H
    # Source: PCT_HOURLY_0100 ... PCT_HOURLY_2400
    # Target: Hr 1 ... Hr 24
    rename_dict = {}
    for i in range(1, 25):
        src_col = f'PCT_HOURLY_{i:02d}00'
        tgt_col = f'Hr {i}'
        rename_dict[src_col] = tgt_col
    
    df = df.rename(columns=rename_dict)
    
    # 3. Define target columns verbatim
    target_columns = ['Date'] + [f'Hr {i}' for i in range(1, 25)]
    
    # 4. Return only the target columns
    return df[target_columns]