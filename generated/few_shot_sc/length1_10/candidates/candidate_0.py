import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the date column
    df['datetime'] = pd.to_datetime(df['date'])
    
    # 2. Extract date and hour
    df['date_only'] = df['datetime'].dt.normalize()
    df['hour'] = df['datetime'].dt.hour
    
    # 3. Map hour to target column names
    # Target columns are 1:00 to 24:00
    # Standard 24h clock: 0-23.
    # Convention: 0 (midnight) -> 24:00, 1 -> 1:00, ..., 23 -> 23:00
    hour_map = {i: f'{i}:00' for i in range(1, 24)}
    hour_map[0] = '24:00'
    
    df['target_hour_col'] = df['hour'].map(hour_map)
    
    # 4. Aggregate
    # Group by date and the mapped hour column, take the mean of the value
    agg_df = df.groupby(['date_only', 'target_hour_col'])['zone_016_cooling_sp'].mean().reset_index()
    
    # 5. Pivot
    # Rows: date_only, Columns: target_hour_col, Values: zone_016_cooling_sp
    pivot_df = agg_df.pivot(index='date_only', columns='target_hour_col', values='zone_016_cooling_sp')
    
    # 6. Format the date column for 'cst'
    # Format: '%a %m/%d/%Y' (e.g., 'Sun 09/30/2018')
    pivot_df['cst'] = pivot_df.index.strftime('%a %m/%d/%Y')
    
    # 7. Prepare final columns
    # Ensure all 24 hour columns are present
    target_hours = [f'{i}:00' for i in range(1, 24)] + ['24:00']
    
    # Reindex columns to ensure order and presence, fill missing with NaN (or 0 if preferred, but NaN is standard for missing)
    # The sample shows no NaNs, but if data is missing for an hour, NaN is appropriate.
    pivot_df = pivot_df.reindex(columns=target_hours)
    
    # Reset index to make 'cst' a column
    pivot_df = pivot_df.reset_index(drop=True)
    
    # Define final column order: cst followed by hours
    final_cols = ['cst'] + target_hours
    
    # Select and return
    return pivot_df[final_cols]