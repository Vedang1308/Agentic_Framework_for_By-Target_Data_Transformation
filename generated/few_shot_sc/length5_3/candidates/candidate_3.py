import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse the date column
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract date for grouping and hour for mapping
    df['date_key'] = df['datetime'].dt.date
    df['hour'] = df['datetime'].dt.hour
    
    # 3. Map hour to target column names
    # Assuming standard 1-24 mapping where 1=01:00...23=23:00 and 24=00:00 (midnight)
    # This aligns with the previous examples where 24:00 was the last column.
    def map_hour_to_col(h):
        if h == 0:
            return 'value24'
        else:
            return f'value{h}'
            
    df['value_col'] = df['hour'].apply(map_hour_to_col)
    
    # 4. Aggregate by date and value column
    # We take the mean of cerc_logger_1 for each date and hour bucket
    grouped = df.groupby(['date_key', 'value_col'])['cerc_logger_1'].mean()
    
    # 5. Pivot/Unstack to get columns value1..value24
    pivot_df = grouped.unstack(fill_value=0)
    
    # Ensure all 24 columns exist, even if some hours have no data
    expected_cols = [f'value{i}' for i in range(1, 25)]
    for col in expected_cols:
        if col not in pivot_df.columns:
            pivot_df[col] = 0
            
    # Sort columns to ensure order value1, value2, ... value24
    pivot_df = pivot_df[expected_cols]
    
    # 6. Format the date index as required
    pivot_df.index = pivot_df.index.strftime('%m/%d/%Y')
    pivot_df.index.name = 'date'
    
    # 7. Reset index to make 'date' a column
    result = pivot_df.reset_index()
    
    # 8. Select and order columns verbatim
    target_columns = ['date'] + [f'value{i}' for i in range(1, 25)]
    return result[target_columns]