import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame into the target DataFrame.
    
    Steps:
    1. Parse the 'date' column into datetime.
    2. Extract the calendar date and the hour of the day.
    3. Map source hours to target column indices (Hour 1-24).
       - Source Hour 0 (midnight) -> Target 'Hour 24'
       - Source Hour 1-23 -> Target 'Hour 1'-'Hour 23'
    4. Group by calendar date and mapped hour, aggregating 'zone_016' with mean.
    5. Pivot the data to create columns for each hour.
    6. Format the date column as 'MM/DD/YYYY'.
    7. Reorder columns to match the target schema.
    """
    
    # Create a copy to avoid modifying the original
    df = source.copy()
    
    # 1. Parse dates
    # Format: '%m/%d/%Y %H:%M'
    df['parsed_date'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract components
    df['calendar_date'] = df['parsed_date'].dt.date
    df['source_hour'] = df['parsed_date'].dt.hour
    
    # 3. Map source hour to target hour column name
    # Logic derived from sample:
    # Source 1/2/2018 0:11 (Hour 0) -> Target 01/02/2018 Hour 24
    # Assumption: Source Hour 1 -> Target Hour 1, ..., Source Hour 23 -> Target Hour 23
    def map_hour(h):
        if h == 0:
            return 24
        else:
            return h
            
    df['target_hour'] = df['source_hour'].apply(map_hour)
    
    # 4. Aggregate
    # Group by calendar_date and target_hour, take the mean of zone_016
    aggregated = df.groupby(['calendar_date', 'target_hour'])['zone_016'].mean().reset_index()
    
    # 5. Pivot
    # Index: calendar_date, Columns: target_hour, Values: zone_016
    pivoted = aggregated.pivot_table(index='calendar_date', columns='target_hour', values='zone_016')
    
    # Reset index to make date a column again
    pivoted = pivoted.reset_index()
    
    # Rename columns: target_hour ints become 'Hour X' strings
    pivoted.columns.name = None # Remove column name index
    new_cols = []
    for col in pivoted.columns:
        if col == 'calendar_date':
            new_cols.append('date')
        else:
            new_cols.append(f'Hour {int(col)}')
    pivoted.columns = new_cols
    
    # 6. Format date column
    # Convert calendar_date (date object) to string MM/DD/YYYY
    pivoted['date'] = pd.to_datetime(pivoted['date']).dt.strftime('%m/%d/%Y')
    
    # 7. Define target columns and reorder
    target_columns = ['date', 'Hour 1', 'Hour 2', 'Hour 3', 'Hour 4', 'Hour 5', 'Hour 6', 'Hour 7', 'Hour 8', 'Hour 9', 'Hour 10', 'Hour 11', 'Hour 12', 'Hour 13', 'Hour 14', 'Hour 15', 'Hour 16', 'Hour 17', 'Hour 18', 'Hour 19', 'Hour 20', 'Hour 21', 'Hour 22', 'Hour 23', 'Hour 24']
    
    # Ensure all target columns exist, filling missing ones with NaN if necessary (though pivot should handle structure)
    for col in target_columns:
        if col not in pivoted.columns:
            pivoted[col] = np.nan
            
    # Select and return
    return pivoted[target_columns]