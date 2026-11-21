import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the datetime column
    # The source format is '%m/%d/%Y %H:%M'
    df['dt'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract date string for grouping and final output
    df['date_only'] = df['dt'].dt.strftime('%m/%d/%Y')
    
    # 3. Extract hour bucket
    # Target columns are 'Hour 1' to 'Hour 24'.
    # Hour 0 (0:00-0:59) maps to 'Hour 1'
    # Hour 1 (1:00-1:59) maps to 'Hour 2'
    # ...
    # Hour 23 (23:00-23:59) maps to 'Hour 24'
    df['hour_bucket'] = df['dt'].dt.hour + 1
    
    # 4. Aggregate data
    # We pivot the data to have dates as rows and hours as columns.
    # The aggregation function is likely 'mean' given the sub-hourly sampling.
    pivot_df = df.pivot_table(
        index='date_only', 
        columns='hour_bucket', 
        values='cerc_logger_1', 
        aggfunc='mean'
    )
    
    # 5. Rename columns to match target schema 'Hour 1', 'Hour 2', ...
    pivot_df.columns = [f'Hour {int(col)}' for col in pivot_df.columns]
    
    # 6. Reset index to make 'date_only' a column
    pivot_df = pivot_df.reset_index()
    pivot_df = pivot_df.rename(columns={'date_only': 'date'})
    
    # 7. Define target columns in the correct order
    target_columns = ['date'] + [f'Hour {i}' for i in range(1, 25)]
    
    # 8. Ensure all target columns exist (in case some hours are missing in data)
    for col in target_columns:
        if col not in pivot_df.columns:
            pivot_df[col] = pd.NA
            
    # 9. Return the final dataframe with exact column order
    return pivot_df[target_columns]