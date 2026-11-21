import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse the date column to extract month
    df = source.copy()
    df['date'] = pd.to_datetime(df['DT_STRATA'])
    df['month'] = df['date'].dt.month
    
    # 2. Identify hourly columns (1 to 24)
    # Source columns are PCT_HOURLY_0100 ... PCT_HOURLY_2400
    hourly_cols = [f'PCT_HOURLY_{i:02d}00' for i in range(1, 25)]
    
    # 3. Melt the dataframe to long format
    # We only care about the hourly columns and the month derived from date
    df_melted = df.melt(
        id_vars=['month'], 
        value_vars=hourly_cols, 
        var_name='hour_col', 
        value_name='value'
    )
    
    # 4. Extract hour integer from column name
    # e.g., 'PCT_HOURLY_0100' -> 1
    df_melted['hour'] = df_melted['hour_col'].str.extract(r'(\d{2})00').astype(int)
    
    # 5. Aggregate by hour and month
    # Calculate the mean value for each hour-month combination
    df_agg = df_melted.groupby(['hour', 'month'])['value'].mean().reset_index()
    
    # 6. Pivot to wide format
    # Rows: hour, Columns: month, Values: mean value
    df_pivot = df_agg.pivot(index='hour', columns='month', values='value')
    
    # 7. Rename month columns to month names
    month_map = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april', 
        5: 'may', 6: 'june', 7: 'july', 8: 'august', 
        9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    df_pivot.rename(columns=month_map, inplace=True)
    
    # 8. Reset index to make 'hour' a column
    df_result = df_pivot.reset_index()
    
    # 9. Ensure correct column order
    target_columns = ['hour', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
    
    # 10. Return the dataframe with verbatim column names
    return df_result[target_columns]