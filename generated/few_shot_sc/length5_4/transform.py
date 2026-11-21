import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the date column to datetime
    df['datetime'] = pd.to_datetime(df['date'])
    
    # 2. Extract the date string for grouping and output
    df['date_out'] = df['datetime'].dt.strftime('%m/%d/%Y')
    
    # 3. Extract the hour and map to target column names (value1 to value24)
    # Hour 0 -> value1, Hour 1 -> value2, ..., Hour 23 -> value24
    df['target_col'] = 'value' + (df['datetime'].dt.hour + 1).astype(str)
    
    # 4. Pivot the table
    # Index: date_out
    # Columns: target_col (value1, value2, ...)
    # Values: zone_016
    # Aggregation: mean (to handle multiple minutes per hour)
    pivot_df = df.pivot_table(
        index='date_out',
        columns='target_col',
        values='zone_016',
        aggfunc='mean'
    )
    
    # 5. Reset index to make date_out a column
    pivot_df = pivot_df.reset_index()
    
    # 6. Rename 'date_out' to 'date'
    pivot_df = pivot_df.rename(columns={'date_out': 'date'})
    
    # 7. Ensure all expected value columns exist (value1 to value24)
    # Pivot might miss columns if no data exists for certain hours/dates
    expected_value_cols = [f'value{i}' for i in range(1, 25)]
    for col in expected_value_cols:
        if col not in pivot_df.columns:
            pivot_df[col] = pd.NA
            
    # 8. Select and order columns verbatim
    target_columns = ['date'] + expected_value_cols
    result_df = pivot_df[target_columns]
    
    return result_df