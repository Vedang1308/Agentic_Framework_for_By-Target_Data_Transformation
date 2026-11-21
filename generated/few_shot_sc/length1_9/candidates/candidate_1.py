import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the date column
    df['dt'] = pd.to_datetime(df['date'])
    
    # 2. Extract calendar date and hour
    df['day'] = df['dt'].dt.date
    df['hour'] = df['dt'].dt.hour
    
    # 3. Map hour to target column name
    # Hour 0 maps to '24:00', Hours 1-23 map to '1:00'...'23:00'
    def map_hour_to_col(h):
        if h == 0:
            return '24:00'
        else:
            return f'{h}:00'
            
    df['hour_col'] = df['hour'].apply(map_hour_to_col)
    
    # 4. Aggregate by day and hour_col, summing zone_016
    # Drop NA values in zone_016 before summing if necessary, though sum ignores NaN
    agg_df = df.groupby(['day', 'hour_col'])['zone_016'].sum().reset_index()
    
    # 5. Pivot to get hours as columns
    pivot_df = agg_df.pivot(index='day', columns='hour_col', values='zone_016')
    
    # 6. Define all target hour columns in order
    target_hours = [f'{h}:00' for h in range(1, 24)] + ['24:00']
    
    # 7. Reindex columns to ensure all hours are present, filling missing with 0
    pivot_df = pivot_df.reindex(columns=target_hours, fill_value=0)
    
    # 8. Format the date index into 'cst' column
    # The index is datetime.date objects. We need to format them as '%a %m/%d/%Y'
    # Convert index to datetime for formatting
    pivot_df.index = pd.to_datetime(pivot_df.index)
    pivot_df['cst'] = pivot_df.index.strftime('%a %m/%d/%Y')
    
    # 9. Reset index to make 'cst' a column and drop the old index
    pivot_df = pivot_df.reset_index(drop=True)
    
    # 10. Select and order columns: cst, 1:00, ..., 24:00
    target_columns = ['cst'] + target_hours
    df_result = pivot_df[target_columns]
    
    # 11. Sort by cst to ensure chronological order if needed (optional but good practice)
    # The problem doesn't specify sort order, but target sample is chronological.
    # Since we grouped by day, it might not be sorted if input was not.
    # Let's sort by the underlying date to be safe.
    df_result['sort_key'] = pd.to_datetime(df_result['cst'].str.split(' ').str[1:]) # This is tricky
    # Easier: just sort by the original day if we kept it, but we dropped it.
    # Let's reconstruct a sortable date from cst or just sort by the index if we hadn't reset.
    # Actually, pivot_df index was date. Let's just sort the final result by 'cst' string? 
    # No, string sort might fail for days. 
    # Better approach: Sort before resetting index.
    
    # Let's restart the end part to handle sorting cleanly
    pivot_df = agg_df.pivot(index='day', columns='hour_col', values='zone_016')
    pivot_df = pivot_df.reindex(columns=target_hours, fill_value=0)
    pivot_df.index = pd.to_datetime(pivot_df.index)
    pivot_df = pivot_df.sort_index() # Sort by date
    pivot_df['cst'] = pivot_df.index.strftime('%a %m/%d/%Y')
    df_result = pivot_df.reset_index(drop=True)
    
    return df_result[target_columns]