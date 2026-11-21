import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the date column
    df['datetime'] = pd.to_datetime(df['date'])
    
    # 2. Extract date string for grouping and formatting
    df['Date'] = df['datetime'].dt.strftime('%m/%d/%Y')
    
    # 3. Extract hour and map to target column names (0->Hr 1, ..., 23->Hr 24)
    df['HourLabel'] = 'Hr ' + (df['datetime'].dt.hour + 1).astype(str)
    
    # 4. Group by Date and HourLabel, calculate mean of cerc_logger_1
    # We use mean because the sample data suggests averaging multiple 10-min intervals per hour
    grouped = df.groupby(['Date', 'HourLabel'])['cerc_logger_1'].mean()
    
    # 5. Unstack to pivot hours into columns
    df_pivot = grouped.unstack('HourLabel')
    
    # 6. Reset index to bring Date back as a column
    df_pivot = df_pivot.reset_index()
    
    # 7. Rename columns to ensure exact match (unstack might produce tuples or slight variations if not careful, 
    # but here HourLabel is string so it should be fine. However, we need to ensure order).
    # The columns from unstack will be the HourLabels. We need to ensure they are named exactly 'Hr 1', etc.
    # Since we constructed HourLabel as 'Hr ' + str(h+1), they should be correct.
    
    # Define target columns verbatim
    target_columns = ['Date'] + [f'Hr {i}' for i in range(1, 25)]
    
    # Ensure all target columns exist (in case some hours are missing in data, fill with NaN or 0 if needed, 
    # but usually unstack handles this by creating NaNs. The prompt doesn't specify fillna, so we keep as is or let pandas handle).
    # Re-index to ensure column order and existence
    df_pivot = df_pivot.reindex(columns=target_columns)
    
    # Return the result
    return df_pivot[target_columns]