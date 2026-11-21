import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse Date and extract month number
    df['date_dt'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
    df['month_num'] = df['date_dt'].dt.month
    
    # 2. Map month number to month name (lowercase)
    month_map = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april',
        5: 'may', 6: 'june', 7: 'july', 8: 'august',
        9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    df['month_name'] = df['month_num'].map(month_map)
    
    # 3. Melt the hourly columns
    # Identify hourly columns
    hourly_cols = [f'Hr {i}' for i in range(1, 25)]
    
    df_melted = df.melt(
        id_vars=['month_name'],
        value_vars=hourly_cols,
        var_name='hour_str',
        value_name='rate'
    )
    
    # 4. Extract integer hour from 'Hr X'
    df_melted['hour'] = df_melted['hour_str'].str.extract(r'(\d+)').astype(int)
    
    # 5. Aggregate: Sum rates for each hour and month
    # Group by hour and month_name, sum the rate
    agg_df = df_melted.groupby(['hour', 'month_name'])['rate'].sum().reset_index()
    
    # 6. Pivot to wide format
    # Index: hour, Columns: month_name, Values: rate
    pivot_df = agg_df.pivot(index='hour', columns='month_name', values='rate')
    
    # 7. Format the final DataFrame
    # Reset index to make 'hour' a column
    result_df = pivot_df.reset_index()
    
    # Rename 'hour' column if needed (it should be 'hour' already)
    # Ensure column names are exactly as required
    target_months = [
        'january', 'february', 'march', 'april', 'may', 'june',
        'july', 'august', 'september', 'october', 'november', 'december'
    ]
    
    # Ensure all month columns exist (fill NaN with 0 if a month is missing for some reason)
    for m in target_months:
        if m not in result_df.columns:
            result_df[m] = 0
            
    # Select and order columns verbatim
    target_columns = ['hour'] + target_months
    result_df = result_df[target_columns]
    
    # Sort by hour to ensure order 1-24
    result_df = result_df.sort_values('hour').reset_index(drop=True)
    
    # Cast hour to int64 as per target schema
    result_df['hour'] = result_df['hour'].astype('int64')
    
    return result_df