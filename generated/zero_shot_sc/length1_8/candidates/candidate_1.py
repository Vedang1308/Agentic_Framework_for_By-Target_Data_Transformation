import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # 1. Parse the date column
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'])
    
    # 2. Extract date and hour components
    df['day'] = df['datetime'].dt.date
    df['hour'] = df['datetime'].dt.hour
    
    # 3. Map source hours (0-23) to target column labels (1:00 - 24:00)
    # Hypothesis: Hour 0 (12am-1am) -> '1:00', Hour 23 (11pm-12am) -> '24:00'
    df['target_hour'] = df['hour'] + 1
    df['target_hour_str'] = df['target_hour'].apply(lambda x: f"{x}:00")
    
    # 4. Aggregate data: Group by day and target hour, calculate mean
    # Using mean as it's the standard aggregation for sensor readings over time intervals
    agg_df = df.groupby(['day', 'target_hour_str'])['cerc_logger_1'].mean()
    
    # 5. Pivot to wide format
    # Index: day, Columns: target_hour_str, Values: mean of cerc_logger_1
    pivot_df = agg_df.unstack(level='target_hour_str')
    
    # 6. Handle missing values
    # The target sample shows a row with all 0s. This implies that if data is missing for a day/hour,
    # it should be filled with 0, or the source had 0s. Given the ambiguity, filling NaNs with 0
    # is the safest bet to match the visual structure of the target sample (specifically the all-zero row).
    pivot_df = pivot_df.fillna(0)
    
    # 7. Format the date index to match target 'cst' column format: '%a %m/%d/%Y'
    # Convert the date index to a datetime object for formatting, then to string
    pivot_df.index = pd.to_datetime(pivot_df.index)
    pivot_df.index = pivot_df.index.strftime('%a %m/%d/%Y')
    
    # 8. Rename the index to 'cst' and reset index to make it a column
    pivot_df.index.name = 'cst'
    pivot_df = pivot_df.reset_index()
    
    # 9. Define the target columns in the correct order
    target_columns = ['cst'] + [f"{h}:00" for h in range(1, 25)]
    
    # 10. Ensure all target columns exist (in case some hours are missing entirely from source)
    for col in target_columns[1:]:
        if col not in pivot_df.columns:
            pivot_df[col] = 0
            
    # 11. Select and order columns verbatim
    return pivot_df[target_columns]