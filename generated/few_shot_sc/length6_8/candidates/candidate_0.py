import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # Parse the date column to datetime
    df['datetime'] = pd.to_datetime(df['date'])
    
    # Extract the date part formatted as MM/DD/YYYY
    df['Date'] = df['datetime'].dt.strftime('%m/%d/%Y')
    
    # Extract the hour and adjust to 1-24 range (0 -> 1, ..., 23 -> 24)
    df['Hour'] = df['datetime'].dt.hour + 1
    
    # Group by Date and Hour, and calculate the mean of cerc_logger_1
    # Using mean as a robust aggregation for sensor data over time intervals
    grouped = df.groupby(['Date', 'Hour'])['cerc_logger_1'].mean()
    
    # Pivot the data so that Hours become columns
    pivot_df = grouped.unstack('Hour')
    
    # Rename columns to match target schema: 'Hr 1', 'Hr 2', ...
    pivot_df.columns = [f'Hr {col}' for col in pivot_df.columns]
    
    # Ensure all 24 hours are present in the columns, filling missing with NaN
    target_hour_cols = [f'Hr {i}' for i in range(1, 25)]
    pivot_df = pivot_df.reindex(columns=target_hour_cols)
    
    # Reset index to bring 'Date' back as a column
    pivot_df = pivot_df.reset_index()
    
    # Define the exact target column order
    target_columns = ['Date'] + target_hour_cols
    
    # Return the dataframe with the correct columns
    return pivot_df[target_columns]