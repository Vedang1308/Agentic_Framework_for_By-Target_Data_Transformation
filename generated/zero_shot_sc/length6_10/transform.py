import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse date
    df = source.copy()
    df['parsed_date'] = pd.to_datetime(df['date'])
    
    # 2. Extract date string and hour index
    df['Date'] = df['parsed_date'].dt.strftime('%m/%d/%Y')
    df['Hour_Index'] = df['parsed_date'].dt.hour + 1 # 1-based index
    
    # 3. Create column name mapping
    df['Col_Name'] = 'Hr ' + df['Hour_Index'].astype(str)
    
    # 4. Pivot
    # We pivot on Date, Col_Name, with values from zone_016_cooling_sp
    pivot_df = df.pivot_table(
        index='Date', 
        columns='Col_Name', 
        values='zone_016_cooling_sp', 
        aggfunc='mean'
    )
    
    # 5. Reset index to make Date a column
    pivot_df = pivot_df.reset_index()
    
    # 6. Ensure all 24 hour columns exist
    target_hour_cols = [f'Hr {i}' for i in range(1, 25)]
    
    # Reindex columns to ensure order and presence of all 24 hours
    # Note: pivot_df columns will be ['Date', 'Hr 1', 'Hr 2', ...] potentially missing some if not in data
    # We need to make sure the final dataframe has all target columns
    
    all_target_cols = ['Date'] + target_hour_cols
    
    # Reindex the dataframe to add missing hour columns (filled with NaN)
    pivot_df = pivot_df.reindex(columns=all_target_cols)
    
    return pivot_df