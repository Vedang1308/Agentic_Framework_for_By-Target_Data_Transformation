import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame containing date and cerc_logger_1 readings
    into a pivoted DataFrame aggregated by month, daytype (weekday/weekend),
    and hour of the day.
    """
    # 1. Parse the date column
    df = source.copy()
    df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract features
    df['month'] = df['date'].dt.strftime('%B') # Full month name
    df['hour'] = df['date'].dt.hour # 0-23
    
    # Determine daytype: weekday (Mon-Fri) or weekend (Sat-Sun)
    # dt.dayofweek: 0=Mon, ..., 4=Fri, 5=Sat, 6=Sun
    df['daytype'] = np.where(df['date'].dt.dayofweek < 5, 'weekday', 'weekend')
    
    # 3. Group by month, daytype, and hour, and calculate the mean of cerc_logger_1
    # We use mean as the aggregation function since we are collapsing multiple readings per hour
    agg_df = df.groupby(['month', 'daytype', 'hour'])['cerc_logger_1'].mean().reset_index()
    
    # 4. Pivot the table
    # Index: month, daytype
    # Columns: hour
    # Values: cerc_logger_1
    pivoted = agg_df.pivot_table(index=['month', 'daytype'], columns='hour', values='cerc_logger_1')
    
    # 5. Rename columns to match target schema (hr1 to hr24)
    # Mapping: Hour 0 -> hr1, Hour 1 -> hr2, ..., Hour 23 -> hr24
    pivoted.columns = [f'hr{i+1}' for i in pivoted.columns]
    
    # 6. Reset index to make month and daytype columns
    result = pivoted.reset_index()
    
    # 7. Define the exact target columns
    target_columns = ['month', 'daytype'] + [f'hr{i}' for i in range(1, 25)]
    
    # 8. Ensure all expected columns exist (in case some hours are missing for some groups)
    for col in target_columns:
        if col not in result.columns:
            result[col] = np.nan
            
    # 9. Return the DataFrame with the exact target columns
    return result[target_columns]