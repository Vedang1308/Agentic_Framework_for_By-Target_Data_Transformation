import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Format the Date column
    # Parse the date string and format it to MM/DD/YYYY with zero-padding
    df['Date'] = pd.to_datetime(df['DT_STRATA'], format='%m/%d/%Y').dt.strftime('%m/%d/%Y')
    
    # 2. Define the mapping for hourly columns
    # Source columns: PCT_HOURLY_0100 to PCT_HOURLY_2400
    # Target columns: Hr 1 to Hr 24
    rename_mapping = {}
    for i in range(1, 25):
        src_col = f'PCT_HOURLY_{i:04d}'
        tgt_col = f'Hr {i}'
        rename_mapping[src_col] = tgt_col
        
    # 3. Rename the columns
    df = df.rename(columns=rename_mapping)
    
    # 4. Define the target columns in the correct order
    target_columns = ['Date'] + [f'Hr {i}' for i in range(1, 25)]
    
    # 5. Select only the required columns
    df = df[target_columns]
    
    return df[target_columns]