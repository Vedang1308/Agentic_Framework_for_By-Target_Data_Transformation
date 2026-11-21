import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Make a copy to avoid modifying the original
    df = source.copy()
    
    # Parse the date column
    # Format in source: '%m/%d/%Y %H:%M' e.g., '7/28/2019 4:50'
    df['dt'] = pd.to_datetime(df['date'])
    
    # Extract the calendar date for grouping
    df['group_date'] = df['dt'].dt.date
    
    # Extract the hour (0-23) and map to 1-24
    # Hour 0 (00:00-00:59) -> Hr 1
    # Hour 23 (23:00-23:59) -> Hr 24
    df['hour_bucket'] = df['dt'].dt.hour + 1
    
    # Aggregate by date and hour bucket
    # Calculate the mean of cerc_logger_1 for each hour
    agg_df = df.groupby(['group_date', 'hour_bucket'])['cerc_logger_1'].mean().reset_index()
    
    # Pivot the table to get hours as columns
    pivot_df = agg_df.pivot(index='group_date', columns='hour_bucket', values='cerc_logger_1')
    
    # Ensure all hours 1-24 are present as columns, filling missing with NaN
    # This handles cases where some hours might not have data
    hours = range(1, 25)
    pivot_df = pivot_df.reindex(columns=hours)
    
    # Rename columns to match target schema: 1 -> 'Hr 1', etc.
    pivot_df.columns = [f'Hr {h}' for h in hours]
    
    # Convert the index (group_date) to the target format '%m/%d/%Y'
    # The index is currently datetime.date objects or similar
    pivot_df.index = pd.to_datetime(pivot_df.index).strftime('%m/%d/%Y')
    
    # Rename the index to 'Date' and reset it to become a column
    pivot_df.index.name = 'Date'
    pivot_df = pivot_df.reset_index()
    
    # Define the target columns in the exact order
    target_columns = ['Date'] + [f'Hr {i}' for i in range(1, 25)]
    
    # Return the DataFrame with the correct columns
    return pivot_df[target_columns]