import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse Date and extract month
    df = source.copy()
    df['Date'] = pd.to_datetime(df['Date'])
    df['month_num'] = df['Date'].dt.month
    
    # 2. Melt the hourly columns
    # Columns 1 through 24 represent hours
    hour_cols = [str(i) for i in range(1, 25)]
    
    melted = df.melt(
        id_vars=['month_num'],
        value_vars=hour_cols,
        var_name='hour',
        value_name='value'
    )
    
    # 3. Clean up the 'hour' column to integer
    melted['hour'] = melted['hour'].astype(int)
    
    # 4. Aggregate by hour and month
    # We calculate the mean value for each hour in each month across all days/classes
    agg_df = melted.groupby(['hour', 'month_num'])['value'].mean().reset_index()
    
    # 5. Pivot to get hours as rows and months as columns
    pivot_df = agg_df.pivot(index='hour', columns='month_num', values='value')
    
    # 6. Map month numbers to lowercase month names
    month_map = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april',
        5: 'may', 6: 'june', 7: 'july', 8: 'august',
        9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    pivot_df.rename(columns=month_map, inplace=True)
    
    # 7. Ensure all month columns exist (fill missing months with NaN)
    target_month_cols = [month_map[i] for i in range(1, 13)]
    for col in target_month_cols:
        if col not in pivot_df.columns:
            pivot_df[col] = float('nan')
            
    # 8. Reset index to make 'hour' a column
    pivot_df.reset_index(inplace=True)
    
    # 9. Select and order the final columns
    target_columns = ['hour'] + target_month_cols
    df_result = pivot_df[target_columns]
    
    # Ensure hour is int64
    df_result['hour'] = df_result['hour'].astype(int)
    
    return df_result