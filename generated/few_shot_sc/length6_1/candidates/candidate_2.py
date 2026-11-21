import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse and format the date column
    # Source DT_STRATA is 'M/D/YYYY', Target Date is 'MM/DD/YYYY'
    dt_parsed = pd.to_datetime(df['DT_STRATA'])
    df['Date'] = dt_parsed.dt.strftime('%m/%d/%Y')
    
    # 2. Rename hourly columns
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
    
    # 4. Select and return the target columns
    return df[target_columns]