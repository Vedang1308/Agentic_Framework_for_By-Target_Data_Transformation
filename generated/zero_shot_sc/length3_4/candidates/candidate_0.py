import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame with timestamped cooling setpoints 
    into a daily summary table with 24 hour columns.
    """
    # 1. Parse the date column
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract date string and hour
    # Format date as MM/DD/YYYY for the target index/column
    df['date_str'] = df['datetime'].dt.strftime('%m/%d/%Y')
    
    # Extract hour (0-23)
    df['hour_int'] = df['datetime'].dt.hour
    
    # Map hour_int to target hour label (1-24)
    # 0 -> 24, 1 -> 1, ..., 23 -> 23
    df['hour_label'] = df['hour_int'].apply(lambda h: 24 if h == 0 else h)
    
    # 3. Aggregate
    # We group by date_str and hour_label.
    # Since there are multiple readings per hour (5-min intervals), we take the mean.
    # If an hour is missing, it won't appear in the groupby, resulting in NaN after pivot.
    agg_df = df.groupby(['date_str', 'hour_label'])['zone_016_cooling_sp'].mean().reset_index()
    
    # 4. Pivot
    # Pivot so that each hour becomes a column
    pivot_df = agg_df.pivot(index='date_str', columns='hour_label', values='zone_016_cooling_sp')
    
    # 5. Ensure all 24 hours are present as columns
    expected_hours = list(range(1, 25))
    for h in expected_hours:
        if h not in pivot_df.columns:
            pivot_df[h] = np.nan
            
    # Sort columns by hour number
    pivot_df = pivot_df[expected_hours]
    
    # 6. Rename columns to match target schema "Hour 1", "Hour 2", ...
    pivot_df.columns = [f'Hour {h}' for h in expected_hours]
    
    # 7. Reset index to make date a column
    pivot_df = pivot_df.reset_index()
    
    # 8. Rename 'date_str' to 'date'
    pivot_df = pivot_df.rename(columns={'date_str': 'date'})
    
    # 9. Define target columns
    target_columns = ['date', 'Hour 1', 'Hour 2', 'Hour 3', 'Hour 4', 'Hour 5', 'Hour 6', 
                      'Hour 7', 'Hour 8', 'Hour 9', 'Hour 10', 'Hour 11', 'Hour 12', 
                      'Hour 13', 'Hour 14', 'Hour 15', 'Hour 16', 'Hour 17', 'Hour 18', 
                      'Hour 19', 'Hour 20', 'Hour 21', 'Hour 22', 'Hour 23', 'Hour 24']
    
    # 10. Ensure column order and selection
    result = pivot_df[target_columns]
    
    # Optional: Cast types to match target schema hints if possible without error
    # The target schema has int64 for some hours and float64 for others.
    # Since NaNs are present, we generally keep float64. 
    # If strict int64 is required for columns without NaNs, we could try:
    # But generally, returning floats is safer for generalization.
    
    return result