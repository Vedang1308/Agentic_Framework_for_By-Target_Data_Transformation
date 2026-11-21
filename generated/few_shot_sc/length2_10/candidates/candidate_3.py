import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms source DataFrame with high-frequency cooling setpoint data 
    into a daily aggregated DataFrame with hourly sums.
    """
    df = source.copy()
    
    # 1. Parse date and extract components
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    df['dt_strata'] = df['datetime'].dt.strftime('%m/%d/%y')
    
    # Calculate dow: Mon=1, Tue=2, ..., Sat=6, Sun=0
    # Python weekday(): Mon=0, ..., Sun=6
    # Formula: (weekday + 1) % 7
    df['dow'] = (df['datetime'].dt.weekday + 1) % 7
    
    # Extract hour (0-23)
    df['hour'] = df['datetime'].dt.hour
    
    # 2. Aggregate by date and hour
    # We sum the cooling setpoint values for each hour of each day
    agg_df = df.groupby(['dt_strata', 'hour'])['zone_016_cooling_sp'].sum().reset_index()
    
    # 3. Pivot to create hourly columns
    # Map hour 0 -> 1, hour 1 -> 2, ..., hour 23 -> 24
    # Column names will be integers 1..24 initially
    pivot_df = agg_df.pivot(index='dt_strata', columns='hour', values='zone_016_cooling_sp')
    
    # 4. Rename columns to match target schema
    # Target columns: pct_hourly_0100 ... pct_hourly_2400
    # Pivot columns are 0..23. We want 0->0100, 1->0200... 23->2400
    rename_map = {h: f'pct_hourly_{h+1:02d}00' for h in range(24)}
    pivot_df = pivot_df.rename(columns=rename_map)
    
    # Reset index to bring dt_strata back as a column
    pivot_df = pivot_df.reset_index()
    
    # 5. Get dow for each date
    # Since dow is constant for a date, we can map it from the original dataframe or recalculate
    # We'll create a mapping from dt_strata to dow from the grouped data
    dow_map = df.groupby('dt_strata')['dow'].first()
    pivot_df['dow'] = pivot_df['dt_strata'].map(dow_map)
    
    # 6. Ensure all hourly columns exist and fill missing with 0
    for i in range(1, 25):
        col_name = f'pct_hourly_{i:02d}00'
        if col_name not in pivot_df.columns:
            pivot_df[col_name] = 0
            
    # 7. Add pct_hourly_2500 with 0
    pivot_df['pct_hourly_2500'] = 0
    
    # 8. Convert hourly columns to int
    hourly_cols = [f'pct_hourly_{i:02d}00' for i in range(1, 25)]
    for col in hourly_cols:
        pivot_df[col] = pivot_df[col].astype(int)
        
    # 9. Select and order columns
    target_columns = ['dt_strata', 'dow'] + hourly_cols + ['pct_hourly_2500']
    
    return pivot_df[target_columns]