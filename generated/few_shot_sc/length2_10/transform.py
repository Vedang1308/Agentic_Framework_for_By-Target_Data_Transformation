import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # Parse date
    dt = pd.to_datetime(df['date'])
    
    # Create dt_strata column
    df['dt_strata'] = dt.dt.strftime('%m/%d/%y')
    
    # Create dow column (Monday=1, ..., Sunday=0 based on analysis)
    # Standard pandas dayofweek: Mon=0, ..., Sun=6
    # Target: Thu=4, Fri=5, Mon=1, Sun=0
    # Mapping: (dayofweek + 1) % 7
    df['dow'] = (dt.dt.dayofweek + 1) % 7
    
    # Create hour column (1-24)
    df['hour'] = dt.dt.hour + 1
    
    # Group by date and hour, sum the values
    # We sum the 'zone_016_cooling_sp' column
    grouped = df.groupby(['dt_strata', 'hour'])['zone_016_cooling_sp'].sum().unstack(fill_value=0)
    
    # Rename columns to match target format pct_hourly_HH00
    rename_map = {h: f'pct_hourly_{h:02d}00' for h in range(1, 25)}
    grouped = grouped.rename(columns=rename_map)
    
    # Add pct_hourly_2500 column with 0
    grouped['pct_hourly_2500'] = 0
    
    # Reset index to make dt_strata a column
    grouped = grouped.reset_index()
    
    # Map dow back to the grouped dataframe
    # Create a mapping from dt_strata to dow
    dow_map = df[['dt_strata', 'dow']].drop_duplicates().set_index('dt_strata')['dow']
    grouped['dow'] = grouped['dt_strata'].map(dow_map)
    
    # Ensure correct column order
    target_cols = ['dt_strata', 'dow'] + [f'pct_hourly_{i:02d}00' for i in range(1, 26)]
    
    # Cast numeric columns to int64
    for col in [f'pct_hourly_{i:02d}00' for i in range(1, 26)]:
        grouped[col] = grouped[col].astype(int)
    grouped['dow'] = grouped['dow'].astype(int)
    
    return grouped[target_cols]