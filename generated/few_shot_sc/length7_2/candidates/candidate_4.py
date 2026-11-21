import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse DT_STRATA to datetime and extract month name
    dt = pd.to_datetime(df['DT_STRATA'])
    df['month'] = dt.dt.strftime('%B')
    
    # 2. Map DOW to daytype
    # Based on standard CBECS/energy data conventions and distinct values ['1'..'7', 'H', 'D']:
    # 1-5: Weekday
    # 6-7, D: Weekend
    # H: Holiday
    def map_daytype(dow):
        if dow in ['1', '2', '3', '4', '5']:
            return 'weekday'
        elif dow in ['6', '7', 'D']:
            return 'weekend'
        elif dow == 'H':
            return 'holiday'
        else:
            return 'weekday' # Default fallback
    
    df['daytype'] = df['DOW'].apply(map_daytype)
    
    # 3. Rename hourly columns from PCT_HOURLY_XX00 to hrX
    rename_dict = {}
    for i in range(1, 25):
        src_col = f'PCT_HOURLY_{i:02d}00'
        tgt_col = f'hr{i}'
        if src_col in df.columns:
            rename_dict[src_col] = tgt_col
            
    df = df.rename(columns=rename_dict)
    
    # 4. Define target columns and return
    target_cols = ['month', 'daytype'] + [f'hr{i}' for i in range(1, 25)]
    
    return df[target_cols]