import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # 1. Parse the date column
    # The source format is '%m/%d/%Y %H:%M'
    df = source.copy()
    df['parsed_date'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract date part and hour
    df['date_only'] = df['parsed_date'].dt.date
    df['hour'] = df['parsed_date'].dt.hour
    
    # 3. Define the mapping from hour (0-23) to target column names
    # 0 -> 12:00 AM (Midnight)
    # 1 -> 1:00 AM
    # ...
    # 11 -> 11:00 AM
    # 12 -> 12:00 PM (Noon)
    # 13 -> 1:00 PM
    # ...
    # 23 -> 11:00 PM
    
    hour_to_col = {}
    # AM hours: 1-11
    for h in range(1, 12):
        hour_to_col[h] = f"{h}:00 AM"
    # Noon
    hour_to_col[12] = "12:00 PM"
    # PM hours: 1-11 (which are 13-23)
    for h in range(1, 12):
        hour_to_col[h + 12] = f"{h}:00 PM"
    # Midnight
    hour_to_col[0] = "12:00 AM"
    
    # 4. Map the integer hour to the string column name
    df['hour_col'] = df['hour'].map(hour_to_col)
    
    # 5. Group by date and hour column, and aggregate.
    # Using mean() as a robust aggregation for the minute-level data.
    # If there are multiple entries for the same hour on the same day, average them.
    agg_df = df.groupby(['date_only', 'hour_col'])['zone_016'].mean().reset_index()
    
    # 6. Pivot the table
    # Index: date_only, Columns: hour_col, Values: zone_016
    pivot_df = agg_df.pivot(index='date_only', columns='hour_col', values='zone_016')
    
    # 7. Reset index to make date_only a column
    pivot_df = pivot_df.reset_index()
    
    # 8. Format the date column to '%m/%d/%Y'
    # The target requires strings like '01/02/2018'
    pivot_df['date'] = pivot_df['date_only'].apply(lambda x: x.strftime('%m/%d/%Y'))
    
    # 9. Define the target columns in the exact order specified
    target_columns = [
        'date',
        '1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', '6:00 AM', '7:00 AM', '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM',
        '12:00 PM',
        '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', '6:00 PM', '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM',
        '12:00 AM'
    ]
    
    # 10. Select and reorder columns. 
    # If a column is missing (e.g., no data for that hour), it will be NaN, which is correct.
    # We need to ensure all target columns exist in the dataframe for selection.
    for col in target_columns:
        if col not in pivot_df.columns:
            pivot_df[col] = np.nan
            
    # Final selection
    result_df = pivot_df[target_columns]
    
    return result_df