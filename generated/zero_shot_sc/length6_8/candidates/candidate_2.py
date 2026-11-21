import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame from long format (timestamp, value) 
    to wide format (date, hourly averages).
    """
    # 1. Parse the date column into datetime objects
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract date and hour
    df['date_only'] = df['datetime'].dt.date
    df['hour'] = df['datetime'].dt.hour
    
    # 3. Aggregate by date and hour
    # We assume the target values are the mean of the readings within that hour.
    # Group by date_only and hour, then take the mean of cerc_logger_1
    agg_df = df.groupby(['date_only', 'hour'])['cerc_logger_1'].mean().reset_index()
    
    # 4. Pivot the data so that hours become columns
    # The pivot will create columns 0, 1, ..., 23
    pivot_df = agg_df.pivot(index='date_only', columns='hour', values='cerc_logger_1')
    
    # 5. Rename columns to match target schema 'Hr 1' to 'Hr 24'
    # Hour 0 -> Hr 1, Hour 1 -> Hr 2, ..., Hour 23 -> Hr 24
    pivot_df.columns = [f'Hr {i+1}' for i in pivot_df.columns]
    
    # 6. Reset index to make 'date_only' a column
    pivot_df = pivot_df.reset_index()
    
    # 7. Format the date column to '%m/%d/%Y'
    pivot_df['Date'] = pivot_df['date_only'].apply(lambda x: x.strftime('%m/%d/%Y'))
    
    # 8. Define the target columns in the correct order
    target_columns = ['Date', 'Hr 1', 'Hr 2', 'Hr 3', 'Hr 4', 'Hr 5', 'Hr 6', 'Hr 7', 'Hr 8', 'Hr 9', 'Hr 10', 'Hr 11', 'Hr 12', 'Hr 13', 'Hr 14', 'Hr 15', 'Hr 16', 'Hr 17', 'Hr 18', 'Hr 19', 'Hr 20', 'Hr 21', 'Hr 22', 'Hr 23', 'Hr 24']
    
    # 9. Ensure all hour columns exist (in case some hours are missing for some days, though unlikely with 10-min data)
    for col in target_columns[1:]:
        if col not in pivot_df.columns:
            pivot_df[col] = np.nan
            
    # 10. Select and order columns to match target exactly
    result_df = pivot_df[target_columns]
    
    # Optional: Sort by Date descending to match the sample visual order if required.
    # The sample shows 05/08/2019 then 05/07/2019. 
    # Converting Date back to datetime for sorting to ensure correct chronological order
    result_df['Date_dt'] = pd.to_datetime(result_df['Date'], format='%m/%d/%Y')
    result_df = result_df.sort_values(by='Date_dt', ascending=False).drop(columns=['Date_dt'])
    
    return result_df