import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the date column
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract date and hour for grouping and pivoting
    df['date_only'] = df['datetime'].dt.date
    df['hour'] = df['datetime'].dt.hour
    
    # 3. Pivot the table
    # We group by date and hour, then aggregate the sensor values.
    # Using 'mean' to aggregate multiple 10-minute readings into a single hourly value.
    pivot_df = df.pivot_table(
        index='date_only', 
        columns='hour', 
        values='cerc_logger_1', 
        aggfunc='mean'
    )
    
    # 4. Rename columns from 0-23 to value1-value24
    # The pivot columns are integers 0, 1, ..., 23
    pivot_df.columns = [f'value{i+1}' for i in range(24)]
    
    # 5. Reset index to make date_only a column
    pivot_df = pivot_df.reset_index()
    
    # 6. Format the date column to match target format '%m/%d/%Y'
    pivot_df['date'] = pd.to_datetime(pivot_df['date_only']).dt.strftime('%m/%d/%Y')
    
    # 7. Select and order columns to match target schema exactly
    target_columns = ['date'] + [f'value{i}' for i in range(1, 25)]
    
    # 8. Return the final dataframe
    return pivot_df[target_columns]