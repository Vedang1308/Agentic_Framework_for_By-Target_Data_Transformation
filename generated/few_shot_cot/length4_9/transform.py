import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the date column
    # Source format: '%m/%d/%Y %H:%M'
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract date for grouping and formatting
    # Target date format: '%m/%d/%Y'
    df['date_only'] = df['datetime'].dt.strftime('%m/%d/%Y')
    
    # 3. Extract hour and map to target column names
    # Mapping 24-hour clock to 12-hour AM/PM format
    def map_hour_to_label(hour):
        if hour == 0:
            return '12:00 AM'
        elif hour < 12:
            return f'{hour}:00 AM'
        elif hour == 12:
            return '12:00 PM'
        else:
            return f'{hour - 12}:00 PM'
    
    df['hour_label'] = df['datetime'].dt.hour.apply(map_hour_to_label)
    
    # 4. Pivot the data
    # We group by date_only and hour_label, aggregating zone_016.
    # Using 'mean' to aggregate multiple readings within the same hour.
    # If there's only one reading, mean returns that value.
    pivot_df = df.pivot_table(
        index='date_only', 
        columns='hour_label', 
        values='zone_016', 
        aggfunc='mean'
    )
    
    # 5. Reset index to make 'date_only' a column
    pivot_df = pivot_df.reset_index()
    
    # 6. Rename the index column to 'date' to match target
    pivot_df = pivot_df.rename(columns={'date_only': 'date'})
    
    # 7. Define the exact target column order
    target_columns = [
        'date', 
        '1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', '6:00 AM', 
        '7:00 AM', '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM', '12:00 PM', 
        '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', '6:00 PM', 
        '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM', '12:00 AM'
    ]
    
    # 8. Ensure all target columns exist (fill missing with NaN if necessary)
    for col in target_columns:
        if col not in pivot_df.columns:
            pivot_df[col] = np.nan
            
    # 9. Select and order columns verbatim
    result_df = pivot_df[target_columns]
    
    return result_df