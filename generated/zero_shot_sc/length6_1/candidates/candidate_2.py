import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame into the target DataFrame.
    
    Steps:
    1. Rename 'DT_STRATA' to 'Date' and format the date strings to '%m/%d/%Y'.
    2. Rename hourly columns 'PCT_HOURLY_XXXX' to 'Hr X'.
    3. Select and order the columns to match the target schema.
    """
    df = source.copy()
    
    # 1. Format Date
    # Parse the date string and re-format to ensure leading zeros (e.g., 1/1/2016 -> 01/01/2016)
    df['Date'] = pd.to_datetime(df['DT_STRATA'], format='%m/%d/%Y').dt.strftime('%m/%d/%Y')
    
    # 2. Rename Hourly Columns
    # Create a mapping from PCT_HOURLY_XXXX to Hr X
    rename_map = {}
    for i in range(1, 25):
        # Source columns are like PCT_HOURLY_0100, PCT_HOURLY_0200, ..., PCT_HOURLY_2400
        src_col = f'PCT_HOURLY_{i:04d}'
        tgt_col = f'Hr {i}'
        rename_map[src_col] = tgt_col
        
    df = df.rename(columns=rename_map)
    
    # 3. Define Target Columns
    target_columns = ['Date'] + [f'Hr {i}' for i in range(1, 25)]
    
    # 4. Select and Return
    return df[target_columns]