import pandas as pd
import calendar

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Melt the dataframe to convert hour columns into rows
    # Columns '1' through '24' become 'hour' variable
    hour_cols = [str(i) for i in range(1, 25)]
    df_melted = df.melt(
        id_vars=['Date', 'Class'],
        value_vars=hour_cols,
        var_name='hour',
        value_name='value'
    )
    
    # 2. Convert 'hour' to integer
    df_melted['hour'] = df_melted['hour'].astype(int)
    
    # 3. Parse 'Date' and extract month name
    df_melted['date_dt'] = pd.to_datetime(df_melted['Date'])
    df_melted['month_num'] = df_melted['date_dt'].dt.month
    # Map month number to lowercase month name
    month_map = {i: calendar.month_name[i].lower() for i in range(1, 13)}
    df_melted['month_name'] = df_melted['month_num'].map(month_map)
    
    # 4. Aggregate by hour and month
    # Calculate the mean value for each hour in each month
    df_agg = df_melted.groupby(['hour', 'month_name'])['value'].mean().reset_index()
    
    # 5. Pivot to get months as columns
    df_pivot = df_agg.pivot(index='hour', columns='month_name', values='value').reset_index()
    
    # 6. Define target columns
    target_columns = ['hour'] + [calendar.month_name[i].lower() for i in range(1, 13)]
    
    # 7. Ensure all target columns exist (fill missing with NaN if necessary)
    for col in target_columns:
        if col not in df_pivot.columns:
            df_pivot[col] = float('nan')
            
    # 8. Select and order columns verbatim
    result = df_pivot[target_columns]
    
    # 9. Ensure 'hour' is integer type
    result['hour'] = result['hour'].astype(int)
    
    return result