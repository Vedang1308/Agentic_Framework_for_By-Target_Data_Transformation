import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    df = source.copy()
    
    # Parse the date column
    dt = pd.to_datetime(df['date'])
    
    # Extract date string in the target format '%m/%d/%Y'
    df['date'] = dt.dt.strftime('%m/%d/%Y')
    
    # Extract the hour (0-23)
    df['hour'] = dt.dt.hour
    
    # Map hour to target column name: Hour 0 -> value1, Hour 23 -> value24
    df['target_col'] = 'value' + (df['hour'] + 1).astype(str)
    
    # Pivot the table to aggregate values by date and hour
    # Using mean as the aggregation function is standard for sensor readings
    pivot_df = df.pivot_table(
        index='date',
        columns='target_col',
        values='cerc_logger_1',
        aggfunc='mean'
    )
    
    # Reset index to make 'date' a column again
    pivot_df = pivot_df.reset_index()
    
    # Define the target column names
    target_columns = ['date'] + [f'value{i}' for i in range(1, 25)]
    
    # Ensure all target columns exist (in case some hours are missing in data)
    for col in target_columns[1:]:
        if col not in pivot_df.columns:
            pivot_df[col] = float('nan')
            
    # Select and return the columns in the correct order
    return pivot_df[target_columns]