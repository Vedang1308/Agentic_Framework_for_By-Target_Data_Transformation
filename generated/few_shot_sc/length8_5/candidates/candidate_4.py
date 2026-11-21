import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Select the date and value columns
    # The value columns are value1 through value24
    value_cols = [f'value{i}' for i in range(1, 25)]
    melt_df = df[['date'] + value_cols]
    
    # 2. Melt the dataframe to long format
    # id_vars keeps 'date', value_vars are the hourly columns
    long_df = melt_df.melt(id_vars=['date'], value_vars=value_cols, 
                           var_name='hour_col', value_name='value')
    
    # 3. Extract hour from column name (e.g., 'value1' -> 1)
    long_df['hour'] = long_df['hour_col'].str.replace('value', '').astype(int)
    
    # 4. Parse date and extract month name
    dt = pd.to_datetime(long_df['date'])
    long_df['month_num'] = dt.dt.month
    
    # Map month numbers to lowercase month names as per target schema
    month_map = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april', 
        5: 'may', 6: 'june', 7: 'july', 8: 'august', 
        9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    long_df['month_name'] = long_df['month_num'].map(month_map)
    
    # 5. Aggregate: Group by hour and month_name, calculate mean
    # This handles the reduction from daily rows to monthly hourly averages
    agg_df = long_df.groupby(['hour', 'month_name'])['value'].mean().reset_index()
    
    # 6. Pivot to wide format
    # Rows: hour, Columns: month_name, Values: mean value
    pivot_df = agg_df.pivot(index='hour', columns='month_name', values='value')
    
    # 7. Clean up the result
    # Remove the 'columns' name attribute if present
    pivot_df.columns.name = None
    
    # Reset index to make 'hour' a column
    result_df = pivot_df.reset_index()
    
    # Ensure hour is integer type
    result_df['hour'] = result_df['hour'].astype(int)
    
    # 8. Define target columns in the correct order
    target_columns = ['hour', 'january', 'february', 'march', 'april', 'may', 'june', 
                      'july', 'august', 'september', 'october', 'november', 'december']
    
    # Select and reorder columns. If a month is missing from data, it will be NaN or missing.
    # We ensure all target columns exist by reindexing if necessary, though pivot usually creates them if they were in groups.
    # If a month had no data, it won't be in the pivot columns. We need to ensure they are present as NaN.
    for col in target_columns:
        if col not in result_df.columns:
            result_df[col] = float('nan')
            
    return result_df[target_columns]