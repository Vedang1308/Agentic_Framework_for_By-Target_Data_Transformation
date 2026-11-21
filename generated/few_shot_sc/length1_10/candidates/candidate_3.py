import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the date column
    df['dt'] = pd.to_datetime(df['date'])
    
    # 2. Extract date part for grouping and hour part
    df['date_only'] = df['dt'].dt.date
    df['hour'] = df['dt'].dt.hour
    
    # 3. Group by date and hour, sum the cooling setpoint values
    # The target values (876) are derived from summing 5-minute intervals (12 per hour)
    # e.g., 73 * 12 = 876.
    grouped = df.groupby(['date_only', 'hour'])['zone_016_cooling_sp'].sum().reset_index()
    
    # 4. Pivot the data to wide format
    pivot_df = grouped.pivot(index='date_only', columns='hour', values='zone_016_cooling_sp')
    
    # 5. Rename columns to match target schema
    # Mapping: Hour 0 -> '24:00', Hour 1 -> '1:00', ..., Hour 23 -> '23:00'
    rename_dict = {}
    for h in range(24):
        if h == 0:
            rename_dict[h] = '24:00'
        else:
            rename_dict[h] = f'{h}:00'
            
    pivot_df = pivot_df.rename(columns=rename_dict)
    
    # 6. Format the date index as 'cst' column
    pivot_df.index = pd.to_datetime(pivot_df.index).strftime('%a %m/%d/%Y')
    pivot_df.index.name = 'cst'
    pivot_df = pivot_df.reset_index()
    
    # 7. Ensure all hour columns exist (fill NaN with 0 if necessary, though sum usually handles presence)
    # Define target columns in order
    target_cols = ['cst'] + [f'{h}:00' for h in range(1, 25)]
    
    # Check if any columns are missing and add them if necessary (e.g., if a day has no data for a specific hour)
    for col in target_cols[1:]:
        if col not in pivot_df.columns:
            pivot_df[col] = 0
            
    # 8. Return the dataframe with exact target columns
    return pivot_df[target_cols]