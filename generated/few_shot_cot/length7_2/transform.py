import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse DT_STRATA to datetime to extract month
    dt = pd.to_datetime(df['DT_STRATA'])
    df['month'] = dt.dt.strftime('%B')
    
    # 2. Map DOW to daytype
    # Standard mapping: 1-5 weekday, 6-7 weekend, H holiday, D weekday (assumed)
    def map_daytype(dow):
        if dow in ['1', '2', '3', '4', '5']:
            return 'weekday'
        elif dow in ['6', '7']:
            return 'weekend'
        elif dow == 'H':
            return 'holiday'
        elif dow == 'D':
            return 'weekday' # Assumption based on common patterns if not weekend/holiday
        else:
            return 'weekday' # Default fallback
    
    df['daytype'] = df['DOW'].apply(map_daytype)
    
    # 3. Rename hourly columns
    rename_dict = {}
    for i in range(1, 25):
        src_col = f'PCT_HOURLY_{i:02d}00'
        tgt_col = f'hr{i}'
        if src_col in df.columns:
            rename_dict[src_col] = tgt_col
            
    df = df.rename(columns=rename_dict)
    
    # 4. Define target columns
    target_columns = ['month', 'daytype'] + [f'hr{i}' for i in range(1, 25)]
    
    # 5. Return selected columns
    return df[target_columns]