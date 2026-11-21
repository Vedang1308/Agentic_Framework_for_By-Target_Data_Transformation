import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    df = source.copy()
    
    # 1. Parse Date
    df['Date'] = pd.to_datetime(df['Date'])
    
    # 2. Extract Month Name
    # Map month numbers to lowercase names
    month_map = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april',
        5: 'may', 6: 'june', 7: 'july', 8: 'august',
        9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    df['month_name'] = df['Date'].dt.month.map(month_map)
    
    # 3. Melt the dataframe to long format
    # Identify hour columns
    hour_cols = [f'Hr {i}' for i in range(1, 25)]
    df_melted = df.melt(
        id_vars=['month_name'], 
        value_vars=hour_cols, 
        var_name='hour_col', 
        value_name='value'
    )
    
    # 4. Extract Hour number from column name 'Hr 1' -> 1
    df_melted['hour'] = df_melted['hour_col'].str.extract(r'(\d+)').astype(int)
    
    # 5. Group by hour and month_name, and aggregate
    # Using mean as the aggregation function
    grouped = df_melted.groupby(['hour', 'month_name'])['value'].mean()
    
    # 6. Pivot to wide format
    # Index: hour, Columns: month_name, Values: mean value
    df_pivot = grouped.unstack(level='month_name')
    
    # 7. Reset index to make 'hour' a column
    df_result = df_pivot.reset_index()
    
    # 8. Ensure column order and names match target
    target_columns = ['hour', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
    
    # Rename columns if necessary (unstack might have named the axis)
    df_result.columns.name = None
    
    # Select and order columns
    return df_result[target_columns]