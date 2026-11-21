import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # 1. Parse the date column
    df = source.copy()
    df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract features
    # Month as full name (e.g., 'August')
    df['month'] = df['date'].dt.strftime('%B')
    
    # Day type: weekday (Mon-Fri) vs weekend (Sat-Sun)
    # dayofweek: 0=Monday, ..., 4=Friday, 5=Saturday, 6=Sunday
    df['daytype'] = df['date'].dt.dayofweek.apply(lambda x: 'weekday' if x < 5 else 'weekend')
    
    # Hour index for pivoting (1-24)
    # Source hours are 0-23. Target columns are hr1-hr24.
    df['hour_idx'] = df['date'].dt.hour + 1
    
    # 3. Aggregate and Pivot
    # We want the mean of cerc_logger_1 for each month, daytype, and hour
    pivot_df = df.pivot_table(
        index=['month', 'daytype'],
        columns='hour_idx',
        values='cerc_logger_1',
        aggfunc='mean'
    )
    
    # 4. Rename columns to hr1, hr2, ..., hr24
    pivot_df.columns = [f'hr{col}' for col in pivot_df.columns]
    
    # 5. Reset index to make month and daytype columns
    result_df = pivot_df.reset_index()
    
    # 6. Define target columns
    target_columns = ['month', 'daytype'] + [f'hr{i}' for i in range(1, 25)]
    
    # Ensure all hour columns exist (some hours might be missing in data, though unlikely for 24h data)
    # If an hour is missing, it will be NaN. The target schema expects float64.
    # We should ensure the columns are present even if NaN.
    for col in target_columns:
        if col not in result_df.columns:
            result_df[col] = pd.NA
            
    # Sort for deterministic output (alphabetical by month, then daytype)
    result_df = result_df.sort_values(by=['month', 'daytype']).reset_index(drop=True)
    
    # Return only the target columns
    return result_df[target_columns]