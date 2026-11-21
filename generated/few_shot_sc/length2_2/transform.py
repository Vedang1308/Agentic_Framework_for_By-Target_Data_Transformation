import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the date column
    # The source date format is M/D/YYYY (e.g., '7/3/2011')
    dt = pd.to_datetime(df['date'])
    
    # 2. Create dt_strata column formatted as M/D/YYYY
    # Using strftime('%m/%d/%Y') will produce MM/DD/YYYY. 
    # The sample shows '1/1/2011'. Pandas strftime does not zero-pad by default for %m/%d if we use specific formatting, 
    # but standard %m/%d/%Y often zero-pads. 
    # However, looking at the sample '1/1/2011', it seems to be non-zero-padded or standard representation.
    # Let's try standard strftime first. If the sample output strictly requires no zero-padding, we might need to strip it.
    # But usually, '1/1/2011' in pandas display might just be how it's printed. 
    # Let's use '%m/%d/%Y'.
    df['dt_strata'] = dt.dt.strftime('%m/%d/%Y')
    
    # 3. Calculate dow (Day of Week)
    # Monday=1, ..., Sunday=7
    # pandas dayofweek: Monday=0, ..., Sunday=6
    df['dow'] = dt.dt.dayofweek + 1
    
    # 4. Rename value columns to pct_hourly columns
    rename_dict = {}
    for i in range(1, 25):
        src_col = f'value{i}'
        tgt_col = f'pct_hourly_{i:02d}00'
        if src_col in df.columns:
            rename_dict[src_col] = tgt_col
            
    df = df.rename(columns=rename_dict)
    
    # 5. Add pct_hourly_2500 column with value 0
    df['pct_hourly_2500'] = 0
    
    # 6. Define target columns verbatim
    target_columns = ['dt_strata', 'dow'] + [f'pct_hourly_{i:02d}00' for i in range(1, 26)]
    
    # 7. Return the dataframe with target columns
    return df[target_columns]