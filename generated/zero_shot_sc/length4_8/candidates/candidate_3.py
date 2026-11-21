import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame with hourly sensor readings into a daily 
    summary DataFrame with columns for each hour of the day in 12-hour format.
    """
    
    # 1. Parse the date column
    # Source format: '%m/%d/%Y %H:%M'
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract Date and Hour
    df['date_only'] = df['datetime'].dt.date
    df['hour_24'] = df['datetime'].dt.hour
    
    # 3. Map 24-hour format to 12-hour format strings as per target columns
    def map_hour_to_label(h):
        if h == 0:
            return '12:00 AM'
        elif h < 12:
            return f'{h}:00 AM'
        elif h == 12:
            return '12:00 PM'
        else:
            return f'{h - 12}:00 PM'
            
    df['hour_label'] = df['hour_24'].apply(map_hour_to_label)
    
    # 4. Aggregate
    # Group by date and hour_label, then take the mean of cerc_logger_1
    # This reduces multiple readings per hour to a single value per hour
    aggregated = df.groupby(['date_only', 'hour_label'])['cerc_logger_1'].mean().reset_index()
    
    # 5. Pivot
    # Create a wide table where rows are dates and columns are hour labels
    pivoted = aggregated.pivot(index='date_only', columns='hour_label', values='cerc_logger_1')
    
    # 6. Format Date Column
    # Reset index to make 'date_only' a column again
    pivoted = pivoted.reset_index()
    # Format the date as MM/DD/YYYY
    pivoted['date'] = pivoted['date_only'].apply(lambda x: x.strftime('%m/%d/%Y'))
    
    # 7. Define Target Columns in the exact required order
    target_columns = [
        'date', 
        '1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', '6:00 AM', '7:00 AM', 
        '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM', '12:00 PM', '1:00 PM', '2:00 PM', 
        '3:00 PM', '4:00 PM', '5:00 PM', '6:00 PM', '7:00 PM', '8:00 PM', '9:00 PM', 
        '10:00 PM', '11:00 PM', '12:00 AM'
    ]
    
    # Ensure the dataframe has the correct columns in the correct order
    # Note: If a specific hour is missing for a day, it will be NaN. 
    # The pivot creates columns based on existing data, so we select from target_columns.
    result_df = pivoted[target_columns]
    
    # Rename columns to match exactly if there are any dtype mismatches or extra spaces (though pivot should handle names correctly)
    # The pivot column names are strings from our mapping, so they should match.
    
    return result_df