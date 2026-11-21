import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms a high-frequency sensor log (10-minute intervals) into a daily summary
    with 24 hourly values (value1 to value24).
    """
    # 1. Parse the date column
    # The source format is '%m/%d/%Y %H:%M'
    df = source.copy()
    df['date_parsed'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract date (day) and hour
    df['day'] = df['date_parsed'].dt.normalize()
    df['hour'] = df['date_parsed'].dt.hour
    
    # 3. Aggregate by day and hour
    # We assume 'mean' aggregation for the 10-minute intervals within each hour.
    # Group by day and hour, then take the mean of cerc_logger_1
    hourly_agg = df.groupby(['day', 'hour'])['cerc_logger_1'].mean().reset_index()
    
    # 4. Pivot the data to wide format
    # Create a pivot table where rows are 'day', columns are 'hour', and values are the aggregated sensor data
    pivot_df = hourly_agg.pivot(index='day', columns='hour', values='cerc_logger_1')
    
    # 5. Ensure all 24 hours are present (0-23) and reorder columns
    # Create a complete index of hours 0-23
    all_hours = pd.RangeIndex(0, 24, name='hour')
    pivot_df = pivot_df.reindex(columns=all_hours)
    
    # 6. Rename columns to value1, value2, ..., value24
    # Hour 0 -> value1, Hour 1 -> value2, ..., Hour 23 -> value24
    pivot_df.columns = [f'value{i+1}' for i in pivot_df.columns]
    
    # 7. Reset index to make 'day' a column
    pivot_df = pivot_df.reset_index()
    
    # 8. Format the date column to MM/DD/YYYY
    pivot_df['date'] = pivot_df['day'].dt.strftime('%m/%d/%Y')
    
    # 9. Define target columns
    target_columns = [
        'date', 'value1', 'value2', 'value3', 'value4', 'value5', 'value6', 
        'value7', 'value8', 'value9', 'value10', 'value11', 'value12', 
        'value13', 'value14', 'value15', 'value16', 'value17', 'value18', 
        'value19', 'value20', 'value21', 'value22', 'value23', 'value24'
    ]
    
    # 10. Sort by date to ensure deterministic output
    pivot_df = pivot_df.sort_values('date').reset_index(drop=True)
    
    # 11. Return only the required columns
    return pivot_df[target_columns]