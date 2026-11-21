import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse the datetime column
    df = source.copy()
    df['parsed_date'] = pd.to_datetime(df['date'])
    
    # 2. Extract date string in target format and hour
    # Target Date format: %m/%d/%Y
    df['Date'] = df['parsed_date'].dt.strftime('%m/%d/%Y')
    
    # Extract hour (0-23). 
    # Based on analysis: Hr 1 corresponds to Clock Hour 0 (00:00-00:59)
    # So, Target Hr N = Clock Hour (N-1)
    # We will use Clock Hour for pivoting and rename later.
    df['Clock_Hour'] = df['parsed_date'].dt.hour
    
    # 3. Aggregate data
    # Group by Date and Clock_Hour, taking the mean of the cooling setpoint
    # Using mean handles multiple 5-min intervals per hour
    agg_df = df.groupby(['Date', 'Clock_Hour'])['zone_016_cooling_sp'].mean().reset_index()
    
    # 4. Pivot the data
    # Index: Date, Columns: Clock_Hour, Values: zone_016_cooling_sp
    pivot_df = agg_df.pivot(index='Date', columns='Clock_Hour', values='zone_016_cooling_sp')
    
    # 5. Rename columns to match target schema 'Hr 1' ... 'Hr 24'
    # Clock_Hour 0 -> 'Hr 1', Clock_Hour 1 -> 'Hr 2', ..., Clock_Hour 23 -> 'Hr 24'
    pivot_df.columns = [f'Hr {int(h)+1}' for h in pivot_df.columns]
    
    # 6. Reset index to make Date a column
    pivot_df = pivot_df.reset_index()
    
    # 7. Define target columns verbatim
    target_columns = ['Date'] + [f'Hr {i}' for i in range(1, 25)]
    
    # 8. Ensure all target columns exist (fill missing hours with NaN if necessary)
    # The pivot might not have all 24 hours for every date if data is missing.
    # We need to reindex columns to ensure the structure matches exactly.
    for col in target_columns:
        if col not in pivot_df.columns:
            pivot_df[col] = pd.NA
            
    # 9. Select and return columns in correct order
    return pivot_df[target_columns]