import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the date column
    df['dt'] = pd.to_datetime(df['date'])
    
    # 2. Create the date string for grouping and output
    df['date_str'] = df['dt'].dt.strftime('%m/%d/%Y')
    
    # 3. Extract hour (0-23) and map to value1-value24
    # Hour 0 -> value1, Hour 1 -> value2, ..., Hour 23 -> value24
    df['hour_idx'] = df['dt'].dt.hour + 1
    df['target_col'] = 'value' + df['hour_idx'].astype(str)
    
    # 4. Aggregate and Pivot
    # We group by date and target column, then take the mean (or first/last) of the value.
    # Using mean to handle any minor floating point variations if present, though values seem constant.
    agg_df = df.groupby(['date_str', 'target_col'])['zone_016_cooling_sp'].mean().reset_index()
    
    # Pivot to wide format
    pivot_df = agg_df.pivot(index='date_str', columns='target_col', values='zone_016_cooling_sp')
    
    # 5. Ensure all 24 value columns exist
    expected_cols = [f'value{i}' for i in range(1, 25)]
    
    # Reindex columns to ensure all value1...value24 are present, filling missing with NaN
    pivot_df = pivot_df.reindex(columns=expected_cols)
    
    # 6. Reset index to make date a column
    pivot_df = pivot_df.reset_index()
    pivot_df.rename(columns={'date_str': 'date'}, inplace=True)
    
    # 7. Select and order columns verbatim
    target_columns = ['date'] + expected_cols
    
    return pivot_df[target_columns]