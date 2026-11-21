import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # Parse the date column
    df['dt'] = pd.to_datetime(df['date'])
    
    # Extract date and hour for grouping
    df['day'] = df['dt'].dt.date
    df['hour'] = df['dt'].dt.hour
    
    # Aggregate by day and hour. Based on the magnitude of values (source ~24, target ~130)
    # and the granularity (10 mins -> 6 slots/hour), Sum is the appropriate aggregation.
    # 24 * 6 = 144, which is close to the target values (~130-145).
    aggregated = df.groupby(['day', 'hour'])['cerc_logger_1'].sum().reset_index()
    
    # Pivot to get hours as columns
    pivot_df = aggregated.pivot(index='day', columns='hour', values='cerc_logger_1')
    
    # Fill missing hours with 0
    pivot_df = pivot_df.fillna(0)
    
    # Rename columns to match target format: 1:00 to 23:00, and 0 (midnight) to 24:00
    rename_map = {h: f'{h}:00' if h != 0 else '24:00' for h in range(24)}
    pivot_df = pivot_df.rename(columns=rename_map)
    
    # Create the 'cst' column with format '%a %m/%d/%Y'
    # Convert index (date) back to datetime for formatting, then to string
    pivot_df = pivot_df.reset_index()
    pivot_df['day'] = pd.to_datetime(pivot_df['day'])
    pivot_df['cst'] = pivot_df['day'].dt.strftime('%a %m/%d/%Y')
    
    # Define target columns in correct order
    target_columns = ['cst'] + [f'{h}:00' for h in range(1, 25)]
    
    # Select and return only the required columns
    # Note: Ensure all columns exist. If some hours are missing from pivot, they are 0 due to fillna.
    # We need to make sure the columns are in the correct order and present.
    for col in target_columns:
        if col not in pivot_df.columns:
            pivot_df[col] = 0
            
    return pivot_df[target_columns]