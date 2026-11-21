import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame (sensor readings every 10 mins) into a daily hourly average DataFrame.
    """
    # 1. Parse the date column
    # The source format is '%m/%d/%Y %H:%M'
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract date and hour
    # We need the calendar date for grouping and the hour for pivoting
    df['date_only'] = df['datetime'].dt.date
    df['hour'] = df['datetime'].dt.hour
    
    # 3. Aggregate
    # Group by date and hour, then calculate the mean of cerc_logger_1
    # This reduces the ~144 readings per day (24*6) to 24 readings per day
    daily_hourly_avg = df.groupby(['date_only', 'hour'])['cerc_logger_1'].mean()
    
    # 4. Pivot
    # Unstack the hour level to create columns for each hour
    # daily_hourly_avg is a Series with MultiIndex (date_only, hour)
    # unstack() will move 'hour' to columns
    pivoted = daily_hourly_avg.unstack(level='hour')
    
    # 5. Rename Columns
    # The target columns are 'Hour 1' to 'Hour 24'
    # Our hours are 0 to 23. So Hour = hour + 1
    new_columns = []
    for h in range(24):
        new_columns.append(f'Hour {h + 1}')
    
    # Ensure we have all 24 columns, even if some hours are missing in the data
    # Create a full range of hours 0-23
    full_hours = pd.RangeIndex(0, 24)
    pivoted = pivoted.reindex(columns=full_hours)
    
    # Rename the columns to match the target schema
    pivoted.columns = new_columns
    
    # 6. Format the Date Column
    # The index is 'date_only' (which is a date object). We need to format it as MM/DD/YYYY string.
    pivoted.index.name = 'date'
    pivoted = pivoted.reset_index()
    
    # Convert date object to string in MM/DD/YYYY format
    pivoted['date'] = pivoted['date'].apply(lambda x: x.strftime('%m/%d/%Y'))
    
    # 7. Sort by date (ascending is standard)
    pivoted = pivoted.sort_values(by='date').reset_index(drop=True)
    
    # 8. Define target columns
    target_columns = ['date', 'Hour 1', 'Hour 2', 'Hour 3', 'Hour 4', 'Hour 5', 'Hour 6', 
                      'Hour 7', 'Hour 8', 'Hour 9', 'Hour 10', 'Hour 11', 'Hour 12', 
                      'Hour 13', 'Hour 14', 'Hour 15', 'Hour 16', 'Hour 17', 'Hour 18', 
                      'Hour 19', 'Hour 20', 'Hour 21', 'Hour 22', 'Hour 23', 'Hour 24']
    
    return pivoted[target_columns]