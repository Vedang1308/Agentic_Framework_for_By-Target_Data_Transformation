import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    df = source.copy()
    
    # 1. Parse the date column
    dt = pd.to_datetime(df['date'])
    
    # 2. Create dt_strata column
    # The target sample shows non-zero-padded dates (e.g., '1/1/2015').
    # We use %-m and %-d to remove leading zeros. 
    # Note: %-m is POSIX standard. On Windows, this might fail or behave differently.
    # A cross-platform safe way to get non-zero-padded month/day:
    # dt.strftime('%m/%d/%Y').replace('/0', '/').replace('/0', '/') ... this is risky.
    # Let's try the standard strftime first. If the benchmark expects non-padded, 
    # and the environment supports it, it will work.
    # Alternative: dt.strftime('%-m/%-d/%Y')
    
    # Let's look at the source again. '7/3/2015'.
    # If we just keep the original string, does it match?
    # The problem is we need to sort. If we sort by datetime, we lose the original string order.
    # But we can map the datetime back to the original string if we assume the original string is the canonical format.
    # However, the target sample '1/1/2015' suggests a specific format.
    
    # Let's try to format it as non-zero padded.
    try:
        df['dt_strata'] = dt.strftime('%-m/%-d/%Y')
    except ValueError:
        # Fallback for Windows which doesn't support %-
        # Format as zero padded, then strip leading zeros from month and day parts
        df['dt_strata'] = dt.strftime('%m/%d/%Y').apply(lambda x: '/'.join([part.lstrip('0') or '0' for part in x.split('/')]))

    # 3. Calculate dow
    # Monday=1, ..., Saturday=6, Sunday=0
    df['dow'] = (dt.dayofweek + 1) % 7
    
    # 4. Rename Hour columns
    rename_map = {}
    for i in range(1, 25):
        src_col = f'Hour {i}'
        tgt_col = f'pct_hourly_{i:02d}00'
        if src_col in df.columns:
            rename_map[src_col] = tgt_col
            
    df = df.rename(columns=rename_map)
    
    # 5. Add pct_hourly_2500 as NaN
    df['pct_hourly_2500'] = np.nan
    
    # 6. Sort by date to ensure deterministic order (matching target sample order)
    df = df.sort_values(by='dt_strata', key=lambda x: pd.to_datetime(x, format='%-m/%-d/%Y' if hasattr(pd.to_datetime, 'format') else None)).reset_index(drop=True)
    # The sort key above is tricky. Better to sort by the datetime object we already have.
    # We need to attach the datetime to the df to sort, then drop it?
    # Or just sort by the string if the format allows lexicographical sort? 
    # '1/1/2015' vs '1/10/2015'. Lexicographical sort fails.
    # We must sort by the parsed datetime.
    
    # Re-assigning dt to df for sorting
    df['_dt'] = dt
    df = df.sort_values(by='_dt').reset_index(drop=True)
    df.drop(columns=['_dt'], inplace=True)

    # 7. Define target columns
    target_cols = ['dt_strata', 'dow'] + [f'pct_hourly_{i:02d}00' for i in range(1, 26)]
    
    return df[target_cols]