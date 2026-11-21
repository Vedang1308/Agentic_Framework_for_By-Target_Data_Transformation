import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Transform Date column
    # Parse DT_STRATA and format as MM/DD/YYYY
    dt = pd.to_datetime(df['DT_STRATA'])
    df['Date'] = dt.dt.strftime('%m/%d/%Y')
    
    # 2. Rename Hourly columns
    # Map PCT_HOURLY_0100 -> Hr 1, ..., PCT_HOURLY_2400 -> Hr 24
    rename_dict = {}
    for i in range(1, 25):
        src_col = f'PCT_HOURLY_{i:02d}00'
        tgt_col = f'Hr {i}'
        if src_col in df.columns:
            rename_dict[src_col] = tgt_col
            
    df = df.rename(columns=rename_dict)
    
    # 3. Define target columns verbatim
    target_columns = ['Date'] + [f'Hr {i}' for i in range(1, 25)]
    
    # 4. Return the transformed dataframe with only target columns
    return df[target_columns]