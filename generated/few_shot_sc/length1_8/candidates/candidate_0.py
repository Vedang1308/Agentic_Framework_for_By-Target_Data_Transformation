import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse the date column
    df = source.copy()
    df['dt'] = pd.to_datetime(df['date'])
    
    # 2. Create the target date string 'cst'
    df['cst'] = df['dt'].dt.strftime('%a %m/%d/%Y')
    
    # 3. Determine the hour label for grouping
    # Mapping: Hour 0 (midnight) -> '24:00', Hours 1-23 -> '1:00'...'23:00'
    # This assumes '24:00' represents the midnight hour (00:00-00:59)
    # and '1:00' represents 1 AM (01:00-01:59), etc.
    def get_hour_label(h):
        if h == 0:
            return '24:00'
        else:
            return f'{h}:00'
    
    df['hour_label'] = df['dt'].dt.hour.apply(get_hour_label)
    
    # 4. Aggregate
    # Group by date ('cst') and hour_label, calculate mean of cerc_logger_1
    grouped = df.groupby(['cst', 'hour_label'])['cerc_logger_1'].mean().reset_index()
    
    # 5. Pivot to wide format
    # Index: cst, Columns: hour_label, Values: cerc_logger_1
    pivoted = grouped.pivot(index='cst', columns='hour_label', values='cerc_logger_1')
    
    # 6. Clean up and reorder columns
    # Remove multiindex name if present
    pivoted.columns.name = None
    
    # Ensure all 24 hour columns exist, filling missing with 0
    target_hour_cols = [f'{h}:00' for h in range(1, 25)] # 1:00 to 24:00
    
    # Check if columns match, if not, reindex
    # Note: The mapping above creates '24:00' for hour 0, and '1:00'..'23:00' for hours 1-23.
    # This matches the target list [1:00, ..., 24:00].
    
    for col in target_hour_cols:
        if col not in pivoted.columns:
            pivoted[col] = 0.0
            
    # Fill any NaNs with 0 (for hours that might be missing in some days)
    pivoted = pivoted.fillna(0)
    
    # Reorder columns to match target exactly
    pivoted = pivoted[target_hour_cols]
    
    # Reset index to make 'cst' a column
    result = pivoted.reset_index()
    
    # Define final target columns
    target_columns = ['cst'] + target_hour_cols
    
    return result[target_columns]