import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the date column to datetime
    df['datetime'] = pd.to_datetime(df['date'])
    
    # 2. Extract date and hour for grouping
    df['date_only'] = df['datetime'].dt.date
    df['hour'] = df['datetime'].dt.hour  # 0-23
    
    # 3. Group by date and hour, and calculate the mean of cerc_logger_1
    # We use groupby and aggregate to get the average value for each hour of each day
    grouped = df.groupby(['date_only', 'hour'])['cerc_logger_1'].mean().reset_index()
    
    # 4. Pivot the table to have hours as columns
    # index='date_only', columns='hour', values='cerc_logger_1'
    pivot_df = grouped.pivot_table(index='date_only', columns='hour', values='cerc_logger_1')
    
    # 5. Rename hour columns from 0-23 to 'Hour 1'-'Hour 24'
    # Map 0 -> 'Hour 1', 1 -> 'Hour 2', ..., 23 -> 'Hour 24'
    pivot_df.columns = [f'Hour {h + 1}' for h in pivot_df.columns]
    
    # 6. Reset index to bring 'date_only' back as a column
    pivot_df = pivot_df.reset_index()
    
    # 7. Format the date column as '%m/%d/%Y'
    pivot_df['date'] = pd.to_datetime(pivot_df['date_only']).dt.strftime('%m/%d/%Y')
    
    # 8. Drop the intermediate 'date_only' column
    pivot_df = pivot_df.drop(columns=['date_only'])
    
    # 9. Define target columns verbatim
    target_columns = ['date'] + [f'Hour {i}' for i in range(1, 25)]
    
    # 10. Ensure correct column order and return
    # Note: pivot_table sorts columns by default, so Hour 1..24 should be in order.
    # We explicitly select them to be safe.
    return pivot_df[target_columns]