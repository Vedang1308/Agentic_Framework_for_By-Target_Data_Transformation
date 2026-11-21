import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame from CST/Hour columns to Date/Hr columns.
    """
    df = source.copy()
    
    # 1. Process the Date column
    # Source format: 'Sat 12/01/2012' (%a %m/%d/%Y)
    # Target format: '12/01/2012' (%m/%d/%Y)
    # We can parse the full string or just extract the date part.
    # pd.to_datetime can handle 'Sat 12/01/2012' directly in many versions, 
    # but to be safe and explicit, we can split or use format inference.
    # Let's try parsing directly first, as it's robust.
    dt_series = pd.to_datetime(df['CST'], format='%a %m/%d/%Y')
    df['Date'] = dt_series.dt.strftime('%m/%d/%Y')
    
    # 2. Rename the hourly columns
    # Source: '1:00', '2:00', ..., '23:00', '24:00:00'
    # Target: 'Hr 1', 'Hr 2', ..., 'Hr 23', 'Hr 24'
    
    rename_map = {}
    
    # Handle hours 1 to 23
    for i in range(1, 24):
        src_col = f'{i}:00'
        tgt_col = f'Hr {i}'
        if src_col in df.columns:
            rename_map[src_col] = tgt_col
            
    # Handle hour 24 specifically as it has ':00:00' in source
    src_col_24 = '24:00:00'
    tgt_col_24 = 'Hr 24'
    if src_col_24 in df.columns:
        rename_map[src_col_24] = tgt_col_24
        
    df = df.rename(columns=rename_map)
    
    # 3. Define target columns in the correct order
    target_columns = ['Date'] + [f'Hr {i}' for i in range(1, 25)]
    
    # 4. Return the DataFrame with only the target columns
    return df[target_columns]