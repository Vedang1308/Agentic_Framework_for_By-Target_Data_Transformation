import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the date column
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract grouping features
    # Month name (e.g., 'August')
    df['month'] = df['datetime'].dt.strftime('%B')
    
    # Day type: weekday (Mon-Fri) or weekend (Sat-Sun)
    # dayofweek: 0=Mon, ..., 4=Fri, 5=Sat, 6=Sun
    df['daytype'] = df['datetime'].dt.dayofweek.apply(lambda x: 'weekend' if x >= 5 else 'weekday')
    
    # Hour: 0-23. Target uses 1-24 (hr1 is hour 0, hr24 is hour 23)
    df['hour_idx'] = df['datetime'].dt.hour + 1
    
    # 3. Pivot the data
    # We group by month and daytype, and spread the hours into columns
    # Using mean to aggregate multiple readings for the same hour/month/daytype
    pivot_df = df.pivot_table(
        index=['month', 'daytype'],
        columns='hour_idx',
        values='cerc_logger_1',
        aggfunc='mean'
    )
    
    # 4. Rename columns to hr1, hr2, ..., hr24
    pivot_df.columns = [f'hr{col}' for col in pivot_df.columns]
    
    # 5. Reset index to make month and daytype columns
    pivot_df = pivot_df.reset_index()
    
    # 6. Define target columns in the exact order
    target_columns = ['month', 'daytype'] + [f'hr{i}' for i in range(1, 25)]
    
    # Ensure all expected columns exist (in case some hours are missing in data, though unlikely for full dataset)
    for col in target_columns:
        if col not in pivot_df.columns:
            pivot_df[col] = 0.0
            
    # Return the dataframe with columns in the correct order
    return pivot_df[target_columns]