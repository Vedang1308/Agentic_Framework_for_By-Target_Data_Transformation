import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Create a copy to avoid modifying the original
    df = source.copy()
    
    # Parse the date column into datetime objects
    df['datetime'] = pd.to_datetime(df['date'])
    
    # Extract the date part for grouping
    df['date_only'] = df['datetime'].dt.date
    
    # Extract the hour and convert to 1-based index (0->1, ..., 23->24)
    df['hour'] = df['datetime'].dt.hour + 1
    
    # Group by date and hour, and calculate the mean of the sensor readings
    grouped = df.groupby(['date_only', 'hour'])['cerc_logger_1'].mean()
    
    # Pivot the table to have hours as columns
    pivoted = grouped.unstack('hour')
    
    # Rename columns to match the target format 'Hr 1', 'Hr 2', etc.
    pivoted.columns = [f'Hr {col}' for col in pivoted.columns]
    
    # Reset index to bring 'date_only' back as a column
    pivoted = pivoted.reset_index()
    
    # Format the date column to 'MM/DD/YYYY'
    pivoted['Date'] = pd.to_datetime(pivoted['date_only']).dt.strftime('%m/%d/%Y')
    
    # Define the exact target column order
    target_columns = ['Date'] + [f'Hr {i}' for i in range(1, 25)]
    
    # Ensure all expected hour columns exist (in case some hours had no data)
    for col in target_columns[1:]:
        if col not in pivoted.columns:
            pivoted[col] = pd.NA
            
    # Return the dataframe with the correct columns
    return pivoted[target_columns]