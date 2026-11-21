import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    df = source.copy()
    
    # 1. Parse the date column
    df['datetime'] = pd.to_datetime(df['date'])
    
    # 2. Extract date string for grouping and final output
    df['date_out'] = df['datetime'].dt.strftime('%m/%d/%Y')
    
    # 3. Extract hour (0-23)
    df['hour'] = df['datetime'].dt.hour
    
    # 4. Map hour to target column name
    # Hour 0 -> Hour 24, Hour 1 -> Hour 1, ..., Hour 23 -> Hour 23
    def map_hour_name(h):
        if h == 0:
            return 'Hour 24'
        else:
            return f'Hour {h}'
            
    df['hour_col'] = df['hour'].apply(map_hour_name)
    
    # 5. Pivot the data
    # Aggregate using mean. If values are constant, mean equals that value.
    # If a date-hour combo is missing, it will be NaN.
    pivot_df = df.pivot_table(
        index='date_out', 
        columns='hour_col', 
        values='zone_016_cooling_sp', 
        aggfunc='mean'
    )
    
    # 6. Reset index to make date a column
    pivot_df = pivot_df.reset_index()
    
    # 7. Rename the date column to 'date'
    pivot_df = pivot_df.rename(columns={'date_out': 'date'})
    
    # 8. Define target columns in order
    target_cols = ['date'] + [f'Hour {i}' for i in range(1, 25)]
    
    # 9. Ensure all target columns exist (some might be missing if no data for that hour)
    for col in target_cols[1:]:
        if col not in pivot_df.columns:
            pivot_df[col] = float('nan')
            
    # 10. Select and order columns
    result_df = pivot_df[target_cols]
    
    # 11. Cast columns to int64 if they contain no NaNs, to match target schema types
    for col in target_cols[1:]:
        if not result_df[col].isna().any():
            result_df[col] = result_df[col].astype(int)
            
    return result_df