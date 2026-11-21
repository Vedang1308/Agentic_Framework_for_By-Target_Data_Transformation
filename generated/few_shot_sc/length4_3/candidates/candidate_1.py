import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Process Date Column
    # Parse DT_STRATA and format as MM/DD/YYYY
    dt = pd.to_datetime(df['DT_STRATA'])
    df['date'] = dt.dt.strftime('%m/%d/%Y')
    
    # 2. Map Hourly Columns
    # Source: PCT_HOURLY_XX00 (XX is 01-24)
    # Target: "H:MM AM/PM"
    
    rename_dict = {}
    
    # Hours 1-11 AM
    for h in range(1, 12):
        src_col = f'PCT_HOURLY_{h:02d}00'
        tgt_col = f'{h}:00 AM'
        rename_dict[src_col] = tgt_col
        
    # Hour 12 PM (Noon)
    rename_dict['PCT_HOURLY_1200'] = '12:00 PM'
    
    # Hours 1-11 PM (Source 13-23)
    for h in range(13, 24):
        src_col = f'PCT_HOURLY_{h:02d}00'
        # Convert 24h to 12h
        h_12 = h - 12
        tgt_col = f'{h_12}:00 PM'
        rename_dict[src_col] = tgt_col
        
    # Hour 24 -> 12:00 AM (Midnight)
    rename_dict['PCT_HOURLY_2400'] = '12:00 AM'
    
    # Apply renaming
    df = df.rename(columns=rename_dict)
    
    # 3. Define Target Columns in Exact Verbatim Order
    # The prompt specifies this exact order:
    # 1-11 AM, then 12 AM, then 1-11 PM, then 12 PM
    target_cols = ['date']
    
    # 1:00 AM to 11:00 AM
    for h in range(1, 12):
        target_cols.append(f'{h}:00 AM')
        
    # 12:00 AM (Midnight) - placed after 11 AM in the target schema provided
    target_cols.append('12:00 AM')
    
    # 1:00 PM to 11:00 PM
    for h in range(1, 12):
        target_cols.append(f'{h}:00 PM')
        
    # 12:00 PM (Noon) - placed at the end in the target schema provided
    target_cols.append('12:00 PM')
    
    return df[target_cols]