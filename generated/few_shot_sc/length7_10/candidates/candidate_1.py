import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the date column
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract features
    # Month name (e.g., 'August')
    df['month'] = df['datetime'].dt.strftime('%B')
    
    # Hour of the day (0-23)
    df['hour'] = df['datetime'].dt.hour
    
    # Day type: weekday (Mon-Fri) or weekend (Sat-Sun)
    # dayofweek: Monday=0, ..., Friday=4, Saturday=5, Sunday=6
    df['daytype'] = df['datetime'].dt.dayofweek.apply(lambda x: 'weekday' if x < 5 else 'weekend')
    
    # 3. Aggregate by month, daytype, and hour
    # We want the mean of cerc_logger_1 for each group
    grouped = df.groupby(['month', 'daytype', 'hour'])['cerc_logger_1'].mean().reset_index()
    
    # 4. Pivot the data to create columns for each hour
    # Current hours are 0-23. Target columns are hr1-hr24.
    # hr1 corresponds to hour 0, hr2 to hour 1, ..., hr24 to hour 23.
    pivoted = grouped.pivot(index=['month', 'daytype'], columns='hour', values='cerc_logger_1')
    
    # 5. Rename columns from 0-23 to hr1-hr24
    pivoted.columns = [f'hr{i+1}' for i in pivoted.columns]
    
    # 6. Reset index to get month and daytype back as columns
    result = pivoted.reset_index()
    
    # 7. Define target columns in the correct order
    target_cols = ['month', 'daytype'] + [f'hr{i}' for i in range(1, 25)]
    
    # Ensure all target columns exist (some might be missing if no data for a specific hour/type)
    # Fill any missing columns with NaN if necessary, though groupby/pivot usually handles structure
    for col in target_cols:
        if col not in result.columns:
            result[col] = pd.NA
            
    # 8. Select and return only the target columns
    return result[target_cols]