import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame to the target schema.
    
    Steps:
    1. Parse the 'date' column to datetime.
    2. Create 'dt_strata' column formatted as '%m/%d/%Y'.
    3. Create 'dow' column representing day of week (0=Sun, 1=Mon, ..., 6=Sat).
    4. Rename 'Hour X' columns to 'pct_hourly_XX00'.
    5. Add 'pct_hourly_2500' column with NaN values.
    6. Select and return columns in the target order.
    """
    df = source.copy()
    
    # Parse date
    dt = pd.to_datetime(df['date'])
    
    # Create dt_strata
    df['dt_strata'] = dt.dt.strftime('%m/%d/%Y')
    
    # Create dow (0=Sunday, 1=Monday, ..., 6=Saturday)
    # Using strftime('%w') which gives 0 for Sunday, 1 for Monday, etc.
    df['dow'] = dt.dt.strftime('%w').astype(int)
    
    # Rename hourly columns
    rename_dict = {f'Hour {i}': f'pct_hourly_{i:02d}00' for i in range(1, 25)}
    df = df.rename(columns=rename_dict)
    
    # Add the 25th hour column with NaN
    df['pct_hourly_2500'] = np.nan
    
    # Define target columns in order
    target_columns = ['dt_strata', 'dow'] + [f'pct_hourly_{i:02d}00' for i in range(1, 26)]
    
    # Return the transformed dataframe
    return df[target_columns]