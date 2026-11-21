import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse Date column
    # Source format: 'Thu 10/01/2009' -> We need to extract the date part '10/01/2009'
    # Split by whitespace and take the last element
    date_str = df['Date'].str.split(' ').str[-1]
    dt = pd.to_datetime(date_str, format='%m/%d/%Y')
    
    # 2. Create dt_strata column in format 'MM/DD/YY'
    df['dt_strata'] = dt.dt.strftime('%m/%d/%y')
    
    # 3. Create dow column (Monday=1, ..., Sunday=7)
    # dayofweek: Monday=0, ..., Sunday=6
    df['dow'] = dt.dt.dayofweek + 1
    
    # 4. Rename hourly columns
    # Source: '1:00', '2:00', ..., '23:00', '24:00:00'
    # Target: 'pct_hourly_0100', ..., 'pct_hourly_2400'
    
    rename_dict = {}
    for i in range(1, 24):
        rename_dict[f'{i}:00'] = f'pct_hourly_{i:02d}00'
    
    # Handle hour 24 specifically as it has ':00:00' in source
    if '24:00:00' in df.columns:
        rename_dict['24:00:00'] = 'pct_hourly_2400'
    elif '24:00' in df.columns:
        rename_dict['24:00'] = 'pct_hourly_2400'
        
    df = df.rename(columns=rename_dict)
    
    # 5. Add pct_hourly_2500 column with NaN values
    df['pct_hourly_2500'] = np.nan
    
    # 6. Define target columns verbatim
    target_columns = ['dt_strata', 'dow'] + [f'pct_hourly_{i:02d}00' for i in range(1, 26)]
    
    # 7. Return the transformed dataframe with correct column order
    return df[target_columns]