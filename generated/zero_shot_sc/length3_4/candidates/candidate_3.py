import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame with high-frequency time-series data 
    into a daily aggregated DataFrame with hourly columns.
    """
    # 1. Parse the date column
    df = source.copy()
    df['parsed_date'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract date string and hour index (1-based)
    # Target date format is MM/DD/YYYY
    df['date_only'] = df['parsed_date'].dt.strftime('%m/%d/%Y')
    # Hour 1 corresponds to 00:00, Hour 24 corresponds to 23:00
    df['hour_num'] = df['parsed_date'].dt.hour + 1
    
    # 3. Aggregate data per day and hour
    # We use 'first' to get the value for that hour. 
    # If multiple values exist per hour, 'first' takes the earliest.
    # If the setpoint changes within an hour, 'mean' or 'last' might be alternatives, 
    # but 'first' is standard for initial state or if data is constant.
    agg_df = df.groupby(['date_only', 'hour_num'])['zone_016_cooling_sp'].first().reset_index()
    
    # 4. Pivot the data
    # Create a pivot table where rows are dates, columns are hours, values are the setpoints
    pivot_df = agg_df.pivot(index='date_only', columns='hour_num', values='zone_016_cooling_sp')
    
    # 5. Rename columns to match target schema 'Hour 1', 'Hour 2', ...
    pivot_df.columns = [f'Hour {int(col)}' for col in pivot_df.columns]
    
    # 6. Ensure all 24 hours are present, even if empty (NaN)
    all_hours = [f'Hour {i}' for i in range(1, 25)]
    pivot_df = pivot_df.reindex(columns=all_hours)
    
    # 7. Reset index to make 'date' a column
    pivot_df = pivot_df.reset_index()
    pivot_df = pivot_df.rename(columns={'date_only': 'date'})
    
    # 8. Define target columns
    target_columns = ['date', 'Hour 1', 'Hour 2', 'Hour 3', 'Hour 4', 'Hour 5', 'Hour 6', 
                      'Hour 7', 'Hour 8', 'Hour 9', 'Hour 10', 'Hour 11', 'Hour 12', 'Hour 13', 
                      'Hour 14', 'Hour 15', 'Hour 16', 'Hour 17', 'Hour 18', 'Hour 19', 'Hour 20', 
                      'Hour 21', 'Hour 22', 'Hour 23', 'Hour 24']
    
    # 9. Return the dataframe with exact column order
    return pivot_df[target_columns]