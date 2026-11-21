import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame into the target DataFrame format.
    """
    df = source.copy()
    
    # 1. Parse DT_STRATA to extract month
    # Format is '%m/%d/%Y'
    dt_parsed = pd.to_datetime(df['DT_STRATA'], format='%m/%d/%Y')
    df['month'] = dt_parsed.dt.strftime('%B')
    
    # 2. Determine daytype based on DOW
    # Mapping inferred from sample:
    # '1' (Sunday) -> weekend
    # '7' (Saturday) -> weekend
    # 'H' (Holiday) -> holiday
    # 'D' (Likely Holiday variant) -> holiday
    # '2'-'6' (Mon-Fri) -> weekday
    
    def map_daytype(dow):
        if dow in ['1', '7']:
            return 'weekend'
        elif dow in ['H', 'D']:
            return 'holiday'
        else:
            return 'weekday'
            
    df['daytype'] = df['DOW'].apply(map_daytype)
    
    # 3. Rename hourly columns
    # Source: PCT_HOURLY_0100 ... PCT_HOURLY_2400
    # Target: hr1 ... hr24
    
    rename_map = {}
    for i in range(1, 25):
        src_col = f'PCT_HOURLY_{i:04d}00'
        tgt_col = f'hr{i}'
        rename_map[src_col] = tgt_col
        
    df.rename(columns=rename_map, inplace=True)
    
    # 4. Select and order columns for the final output
    target_columns = ['month', 'daytype'] + [f'hr{i}' for i in range(1, 25)]
    
    # Ensure only the required columns are returned
    df = df[target_columns]
    
    return df