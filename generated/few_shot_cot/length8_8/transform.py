import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the date column to extract month information
    df['date_dt'] = pd.to_datetime(df['date'])
    df['month_num'] = df['date_dt'].dt.month
    
    # Map month numbers to lowercase month names
    month_map = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april',
        5: 'may', 6: 'june', 7: 'july', 8: 'august',
        9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    df['month_name'] = df['month_num'].map(month_map)
    
    # 2. Melt the hour columns from wide to long format
    # Identify hour columns
    hour_cols = [f'Hour {i}' for i in range(1, 25)]
    
    # Melt
    df_melted = df.melt(
        id_vars=['month_name'], 
        value_vars=hour_cols, 
        var_name='hour_col', 
        value_name='value'
    )
    
    # 3. Extract integer hour from the column name 'Hour X'
    df_melted['hour'] = df_melted['hour_col'].str.extract(r'(\d+)').astype(int)
    
    # 4. Group by hour and month, and aggregate
    # Using mean as the aggregation function. 
    # If values are constant per hour/month, mean equals the value.
    grouped = df_melted.groupby(['hour', 'month_name'])['value'].mean().reset_index()
    
    # 5. Pivot the data to get months as columns
    # Index: hour, Columns: month_name, Values: value
    df_pivot = grouped.pivot(index='hour', columns='month_name', values='value')
    
    # 6. Clean up the DataFrame
    df_pivot.reset_index(inplace=True)
    
    # Rename columns to match target schema exactly
    # The pivot creates a MultiIndex or simple columns depending on version, 
    # but here columns are the month names.
    # Ensure column names are strings and lowercase (they should be from the map)
    df_pivot.columns.name = None
    
    # Define target columns
    target_columns = ['hour', 'january', 'february', 'march', 'april', 'may', 'june', 
                      'july', 'august', 'september', 'october', 'november', 'december']
    
    # Ensure all target month columns exist, filling missing with NaN if necessary
    for col in target_columns[1:]:
        if col not in df_pivot.columns:
            df_pivot[col] = float('nan')
            
    # Select and order columns
    df_result = df_pivot[target_columns]
    
    # 7. Sort the rows
    # The sample target shows order: 1, 10, 11, 12, 6, 7, 8, 9
    # This corresponds to a string sort of the hour numbers.
    df_result['hour_str'] = df_result['hour'].astype(str)
    df_result = df_result.sort_values(by='hour_str').drop(columns=['hour_str'])
    
    # Ensure hour is int64 as per target schema
    df_result['hour'] = df_result['hour'].astype(int)
    
    return df_result