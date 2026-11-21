import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms high-frequency time series data (minute-level) into daily hourly aggregates.
    
    Steps:
    1. Parse the 'date' column into datetime objects.
    2. Extract the date (day) and hour from the datetime.
    3. Group by date and hour, and sum the 'zone_016' values.
    4. Pivot the data to have hours as columns and dates as rows.
    5. Rename hour columns from 0-23 to '1:00'-'24:00'.
    6. Format the date index into the 'cst' column format.
    7. Ensure all 24 hour columns exist, filling missing values with 0.
    8. Return the DataFrame with the specified target columns.
    """
    df = source.copy()
    
    # 1. Parse datetime
    df['datetime'] = pd.to_datetime(df['date'])
    
    # 2. Extract day and hour
    # We use normalize() to get the start of the day for grouping
    df['day'] = df['datetime'].dt.normalize()
    df['hour'] = df['datetime'].dt.hour
    
    # 3. Aggregate: Sum zone_016 for each day and hour
    # Using sum() ignores NaNs automatically
    aggregated = df.groupby(['day', 'hour'])['zone_016'].sum().reset_index()
    
    # 4. Pivot to create hourly columns
    # fill_value=0 ensures that if a day/hour combination is missing, it's 0
    pivot_df = aggregated.pivot_table(
        index='day', 
        columns='hour', 
        values='zone_016', 
        fill_value=0
    )
    
    # 5. Rename columns from 0-23 to '1:00'-'24:00'
    # Ensure all hours 0-23 are present in columns before renaming to avoid index errors
    # The pivot_table might not have all hours if they don't exist in the data, 
    # but fill_value=0 doesn't add columns, it fills values. 
    # We need to reindex columns to ensure 0-23 are present.
    all_hours = pd.RangeIndex(0, 24)
    pivot_df = pivot_df.reindex(columns=all_hours, fill_value=0)
    
    # Now rename
    pivot_df.columns = [f'{h+1}:00' for h in range(24)]
    
    # 6. Format the 'day' index into 'cst' column
    # The index is named 'day', we reset it to a column
    pivot_df = pivot_df.reset_index()
    pivot_df['cst'] = pivot_df['day'].dt.strftime('%a %m/%d/%Y')
    
    # 7. Define target columns
    target_columns = ['cst'] + [f'{i}:00' for i in range(1, 25)]
    
    # 8. Select and return
    return pivot_df[target_columns]