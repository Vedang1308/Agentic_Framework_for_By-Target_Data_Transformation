import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame from long format (timestamped readings) 
    to wide format (daily hourly aggregates).
    """
    # 1. Parse the date column
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract date and hour
    # Format date as MM/DD/YYYY
    df['date'] = df['datetime'].dt.strftime('%m/%d/%Y')
    # Extract hour (0-23) and convert to 1-24 index
    df['hour_idx'] = df['datetime'].dt.hour + 1
    
    # 3. Aggregate by date and hour
    # We calculate the mean of cerc_logger_1 for each date and hour
    # Using groupby and mean handles the multiple readings per hour
    aggregated = df.groupby(['date', 'hour_idx'])['cerc_logger_1'].mean().reset_index()
    
    # 4. Pivot the table
    # Index: date, Columns: hour_idx, Values: cerc_logger_1
    pivoted = aggregated.pivot(index='date', columns='hour_idx', values='cerc_logger_1')
    
    # 5. Rename columns to match target format "Hour X"
    # The pivot columns are integers 1-24. We need strings "Hour 1", "Hour 2", etc.
    pivoted.columns = [f'Hour {i}' for i in pivoted.columns]
    
    # 6. Reset index to make 'date' a column again
    result = pivoted.reset_index()
    
    # 7. Ensure correct column order and names
    target_columns = ['date', 'Hour 1', 'Hour 2', 'Hour 3', 'Hour 4', 'Hour 5', 'Hour 6', 
                      'Hour 7', 'Hour 8', 'Hour 9', 'Hour 10', 'Hour 11', 'Hour 12', 'Hour 13', 
                      'Hour 14', 'Hour 15', 'Hour 16', 'Hour 17', 'Hour 18', 'Hour 19', 'Hour 20', 
                      'Hour 21', 'Hour 22', 'Hour 23', 'Hour 24']
    
    # Select only the target columns. If some hours are missing in the data, 
    # they will be NaN, which is standard for this type of transformation.
    # We reindex to ensure all expected columns exist, filling missing ones with NaN if necessary.
    result = result.reindex(columns=target_columns)
    
    return result[target_columns]