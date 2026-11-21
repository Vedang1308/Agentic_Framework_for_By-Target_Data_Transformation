import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Identify hourly columns to melt
    # The columns are PCT_HOURLY_0100 to PCT_HOURLY_2400
    hourly_cols = [f'PCT_HOURLY_{str(h).zfill(4)}' for h in range(1, 25)]
    
    # 2. Parse dates and extract month
    # Convert DT_STRATA to datetime
    source = source.copy()
    source['date'] = pd.to_datetime(source['DT_STRATA'], format='%m/%d/%Y')
    source['month_num'] = source['date'].dt.month
    
    # Map month number to lowercase name
    month_map = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april',
        5: 'may', 6: 'june', 7: 'july', 8: 'august',
        9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    source['month'] = source['month_num'].map(month_map)
    
    # 3. Melt the hourly columns
    # We keep 'month' as an identifier, and melt the hourly columns
    # id_vars should include 'month'
    df_melted = source.melt(
        id_vars=['month'],
        value_vars=hourly_cols,
        var_name='hour_col',
        value_name='value'
    )
    
    # 4. Extract hour integer from hour_col
    # PCT_HOURLY_0100 -> 1, PCT_HOURLY_1200 -> 12, etc.
    # The last 4 digits represent HHMM. Since they are always XX00, we can divide by 100 or parse the first two digits.
    # Safer: strip 'PCT_HOURLY_', convert to int, divide by 100.
    df_melted['hour'] = df_melted['hour_col'].str.extract('(\d{4})').astype(int) // 100
    
    # 5. Aggregate by hour and month
    # Calculate the mean value for each hour and month combination
    df_agg = df_melted.groupby(['hour', 'month'])['value'].mean().reset_index()
    
    # 6. Pivot to wide format
    # Index: hour, Columns: month, Values: value
    df_pivot = df_agg.pivot(index='hour', columns='month', values='value')
    
    # 7. Clean up
    # Reset index to make 'hour' a column
    df_result = df_pivot.reset_index()
    
    # Rename columns to remove the upper-level name if present (pivot sometimes adds it)
    df_result.columns.name = None
    
    # Ensure column order matches target: hour, january, february, ...
    target_columns = ['hour', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
    
    # Select and reorder columns
    df_result = df_result[target_columns]
    
    # Ensure hour is integer
    df_result['hour'] = df_result['hour'].astype(int)
    
    # Sort by hour to ensure correct order 1-24
    df_result = df_result.sort_values('hour').reset_index(drop=True)
    
    return df_result[target_columns]