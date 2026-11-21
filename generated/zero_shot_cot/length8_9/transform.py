import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source electricity rate data into a monthly hourly summary.
    
    Steps:
    1. Parse the 'Date' column to datetime.
    2. Extract the month name from the date.
    3. Melt the 'Hr 1'...'Hr 24' columns into a long format with 'hour' and 'value'.
    4. Group by 'hour' and 'month_name' and sum the values.
    5. Pivot the data so that months are columns and hours are rows.
    6. Format the output to match the target schema.
    """
    
    # 1. Parse Date
    df = source.copy()
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
    
    # 2. Extract Month Name
    # Map month numbers to lowercase month names
    month_map = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april',
        5: 'may', 6: 'june', 7: 'july', 8: 'august',
        9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    df['month_name'] = df['Date'].dt.month.map(month_map)
    
    # 3. Melt Hour Columns
    # Identify hour columns
    hour_cols = [f'Hr {i}' for i in range(1, 25)]
    
    # Melt the dataframe
    # id_vars keeps 'month_name' (and Date if needed, but we only need month_name for grouping)
    # We need to keep the month_name associated with each row
    df_melted = df.melt(
        id_vars=['month_name'], 
        value_vars=hour_cols, 
        var_name='hour_col', 
        value_name='value'
    )
    
    # Extract hour number from 'Hr 1' -> 1
    df_melted['hour'] = df_melted['hour_col'].str.extract(r'(\d+)').astype(int)
    
    # 4. Aggregate
    # Group by hour and month_name, sum the values
    # Note: The target values look like sums of the rates across all rate types/companies for that hour/month.
    agg_df = df_melted.groupby(['hour', 'month_name'])['value'].sum().reset_index()
    
    # 5. Pivot
    # Pivot so that 'month_name' becomes columns and 'hour' is the index
    pivot_df = agg_df.pivot(index='hour', columns='month_name', values='value')
    
    # 6. Format Output
    # Reset index to make 'hour' a column
    pivot_df = pivot_df.reset_index()
    
    # Ensure column order and names match target
    target_columns = ['hour', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
    
    # Fill any missing months with 0 if necessary (though data seems complete)
    pivot_df = pivot_df.fillna(0)
    
    # Ensure hour is integer
    pivot_df['hour'] = pivot_df['hour'].astype(int)
    
    # Select and order columns
    result_df = pivot_df[target_columns]
    
    # Sort by hour to ensure 1-24 order
    result_df = result_df.sort_values('hour').reset_index(drop=True)
    
    return result_df