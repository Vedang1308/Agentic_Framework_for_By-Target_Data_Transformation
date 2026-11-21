import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame with timestamped sensor readings into a 
    daily wide-format DataFrame with hourly averages.
    
    Source: 'date' (string), 'cerc_logger_1' (float)
    Target: 'date' (string MM/DD/YYYY), 'Hour 1'...'Hour 24' (float)
    """
    
    # 1. Parse the date column
    # The format is %m/%d/%Y %H:%M
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract date string and hour component
    # Target date format is %m/%d/%Y
    df['date_str'] = df['datetime'].dt.strftime('%m/%d/%Y')
    
    # Extract hour (0-23). Target hours are 1-24.
    # Hour 1 corresponds to 00:xx, Hour 2 to 01:xx, etc.
    df['hour_label'] = df['datetime'].dt.hour + 1
    
    # 3. Aggregate values for each date and hour
    # We calculate the mean of cerc_logger_1 for each date and hour combination
    df_agg = df.groupby(['date_str', 'hour_label'])['cerc_logger_1'].mean().reset_index()
    
    # 4. Pivot to wide format
    # Index: date_str, Columns: hour_label, Values: cerc_logger_1
    df_wide = df_agg.pivot(index='date_str', columns='hour_label', values='cerc_logger_1')
    
    # 5. Rename columns to match target schema 'Hour 1', 'Hour 2', ...
    df_wide.columns = [f'Hour {col}' for col in df_wide.columns]
    
    # 6. Reset index to make 'date' a column again
    df_wide.reset_index(inplace=True)
    df_wide.rename(columns={'date_str': 'date'}, inplace=True)
    
    # 7. Ensure all 24 hours are present, filling missing ones with NaN if necessary
    # This handles cases where a specific hour has no data
    target_hours = [f'Hour {i}' for i in range(1, 25)]
    df_wide = df_wide.reindex(columns=['date'] + target_hours)
    
    # 8. Sort by date for deterministic output (optional but good practice)
    # Converting back to datetime for sorting to ensure correct chronological order
    df_wide['date_dt'] = pd.to_datetime(df_wide['date'], format='%m/%d/%Y')
    df_wide.sort_values('date_dt', inplace=True)
    df_wide.drop(columns=['date_dt'], inplace=True)
    
    # 9. Define target columns verbatim
    target_columns = ['date', 'Hour 1', 'Hour 2', 'Hour 3', 'Hour 4', 'Hour 5', 'Hour 6', 
                      'Hour 7', 'Hour 8', 'Hour 9', 'Hour 10', 'Hour 11', 'Hour 12', 
                      'Hour 13', 'Hour 14', 'Hour 15', 'Hour 16', 'Hour 17', 'Hour 18', 
                      'Hour 19', 'Hour 20', 'Hour 21', 'Hour 22', 'Hour 23', 'Hour 24']
    
    return df_wide[target_columns]