import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame (date, cerc_logger_1) into a daily profile
    with columns 'date' and 'Hour 1' through 'Hour 24'.
    """
    df = source.copy()
    
    # 1. Parse the date column to datetime
    # The source format is '%m/%d/%Y %H:%M'
    df['datetime'] = pd.to_datetime(df['date'])
    
    # 2. Extract the date part for grouping and the hour part for pivoting
    df['date_str'] = df['datetime'].dt.strftime('%m/%d/%Y')
    df['hour'] = df['datetime'].dt.hour  # 0 to 23
    
    # 3. Aggregate by date and hour
    # We assume the value for a specific hour is the mean of all samples in that hour
    # Group by date_str and hour, then take the mean of cerc_logger_1
    aggregated = df.groupby(['date_str', 'hour'])['cerc_logger_1'].mean().reset_index()
    
    # 4. Pivot the data
    # Index: date_str, Columns: hour, Values: cerc_logger_1
    pivoted = aggregated.pivot(index='date_str', columns='hour', values='cerc_logger_1')
    
    # 5. Rename columns to match target schema ('Hour 1' to 'Hour 24')
    # Source hour 0 corresponds to Hour 1, ..., 23 corresponds to Hour 24
    pivoted.columns = [f'Hour {h + 1}' for h in pivoted.columns]
    
    # 6. Reset index to convert 'date_str' back to a column
    pivoted = pivoted.reset_index()
    pivoted = pivoted.rename(columns={'date_str': 'date'})
    
    # 7. Ensure all 24 hour columns exist and are in the correct order
    # In case some hours are missing for some dates, fill NaNs with 0 or interpolate?
    # The problem doesn't specify, but typically these logs are dense. 
    # We will sort the columns to ensure correct order.
    target_hour_cols = [f'Hour {i}' for i in range(1, 25)]
    
    # Re-index columns to ensure all 24 are present, filling missing with NaN (or 0 if preferred)
    # Using reindex ensures the column names match exactly
    pivoted = pivoted.reindex(columns=['date'] + target_hour_cols)
    
    # Optional: Fill NaNs if any hours are missing. 
    # Given the high density (6 samples/hour), missing hours are unlikely for a full day.
    # However, to be safe and deterministic, we can leave them as NaN or fill.
    # Looking at target sample, no NaNs. We'll assume data is complete.
    # If needed, pivoted[target_hour_cols] = pivoted[target_hour_cols].fillna(0)
    
    # 8. Select and return the final columns
    target_columns = ['date'] + target_hour_cols
    return pivoted[target_columns]