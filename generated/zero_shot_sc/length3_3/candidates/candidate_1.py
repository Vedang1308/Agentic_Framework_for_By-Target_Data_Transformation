import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # 1. Parse the date column
    # The source format is '%m/%d/%Y %H:%M'
    source['datetime'] = pd.to_datetime(source['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract the calendar date and format it as required by the target ('%m/%d/%Y')
    source['date_str'] = source['datetime'].dt.strftime('%m/%d/%Y')
    
    # 3. Extract the hour (0-23)
    source['hour_num'] = source['datetime'].dt.hour
    
    # 4. Map source hours to target column indices
    # Target columns are 'Hour 1' to 'Hour 24'.
    # Based on analysis:
    # Source Hour 1 -> Target 'Hour 1'
    # ...
    # Source Hour 23 -> Target 'Hour 23'
    # Source Hour 0  -> Target 'Hour 24'
    
    def map_hour_to_target_col(h):
        if h == 0:
            return 'Hour 24'
        else:
            return f'Hour {h}'
            
    source['target_hour_col'] = source['hour_num'].apply(map_hour_to_target_col)
    
    # 5. Aggregate
    # We group by date and the mapped target hour column, and calculate the mean of zone_016.
    # Using 'mean' to handle multiple entries per hour and ignore NaNs.
    grouped = source.groupby(['date_str', 'target_hour_col'])['zone_016'].mean().reset_index()
    
    # 6. Pivot the data
    # Index: date_str
    # Columns: target_hour_col
    # Values: zone_016
    pivoted = grouped.pivot(index='date_str', columns='target_hour_col', values='zone_016')
    
    # 7. Ensure all 24 hour columns are present
    target_hours = [f'Hour {i}' for i in range(1, 25)]
    pivoted = pivoted.reindex(columns=target_hours)
    
    # 8. Reset index to make 'date' a column again
    pivoted = pivoted.reset_index()
    pivoted.rename(columns={'date_str': 'date'}, inplace=True)
    
    # 9. Sort by date descending to match the sample order (01/02 before 01/01)
    # Note: String sorting of '%m/%d/%Y' works correctly for this format.
    pivoted = pivoted.sort_values(by='date', ascending=False).reset_index(drop=True)
    
    # 10. Define target columns
    target_columns = ['date'] + [f'Hour {i}' for i in range(1, 25)]
    
    # 11. Return the dataframe with exact target columns
    return pivoted[target_columns]