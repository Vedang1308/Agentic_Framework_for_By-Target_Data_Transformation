import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame into the target DataFrame format.
    """
    # 1. Parse the Date column
    # The source date format is '%m/%d/%Y'
    df = source.copy()
    df['parsed_date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
    
    # 2. Create dt_strata column
    # Format back to '%m/%d/%Y'
    df['dt_strata'] = df['parsed_date'].dt.strftime('%m/%d/%Y')
    
    # 3. Create dow column
    # Mapping: Sunday=0, Monday=1, ..., Saturday=6
    # Pandas dayofweek: Monday=0, ..., Sunday=6
    # Formula: (dayofweek + 1) % 7
    df['dow'] = (df['parsed_date'].dt.dayofweek + 1) % 7
    
    # 4. Rename hourly columns 1-24 to pct_hourly_0100 - pct_hourly_2400
    # Source columns are integers 1 to 24
    hourly_cols = [str(i) for i in range(1, 25)]
    new_hourly_cols = [f'pct_hourly_{i:04d}' for i in range(1, 25)]
    
    # Create a mapping dictionary
    col_mapping = {old: new for old, new in zip(hourly_cols, new_hourly_cols)}
    df = df.rename(columns=col_mapping)
    
    # 5. Add pct_hourly_2500 column with NaN
    df['pct_hourly_2500'] = np.nan
    
    # 6. Define the target columns in the correct order
    target_columns = [
        'dt_strata', 'dow',
        'pct_hourly_0100', 'pct_hourly_0200', 'pct_hourly_0300', 'pct_hourly_0400',
        'pct_hourly_0500', 'pct_hourly_0600', 'pct_hourly_0700', 'pct_hourly_0800',
        'pct_hourly_0900', 'pct_hourly_1000', 'pct_hourly_1100', 'pct_hourly_1200',
        'pct_hourly_1300', 'pct_hourly_1400', 'pct_hourly_1500', 'pct_hourly_1600',
        'pct_hourly_1700', 'pct_hourly_1800', 'pct_hourly_1900', 'pct_hourly_2000',
        'pct_hourly_2100', 'pct_hourly_2200', 'pct_hourly_2300', 'pct_hourly_2400',
        'pct_hourly_2500'
    ]
    
    # 7. Select and return the target columns
    # Drop the helper column parsed_date
    df = df.drop(columns=['parsed_date'])
    
    return df[target_columns]