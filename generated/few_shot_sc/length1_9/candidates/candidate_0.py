import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the date column
    # Format is '%m/%d/%Y %H:%M' based on sample '1/2/2018 0:11'
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract date for grouping and hour for pivoting
    df['date_only'] = df['datetime'].dt.date
    df['hour'] = df['datetime'].dt.hour
    
    # 3. Map hour 0-23 to target column labels '1:00'-'24:00'
    # Hour 0 -> '1:00', Hour 1 -> '2:00', ..., Hour 23 -> '24:00'
    df['hour_label'] = df['hour'].apply(lambda h: f"{h+1}:00")
    
    # 4. Group by date_only and hour_label, summing the zone_016 values
    # Using sum to aggregate minute-level data into hourly totals
    aggregated = df.groupby(['date_only', 'hour_label'])['zone_016'].sum().reset_index()
    
    # 5. Pivot the table so each hour_label becomes a column
    pivoted = aggregated.pivot_table(
        index='date_only', 
        columns='hour_label', 
        values='zone_016', 
        aggfunc='sum'
    ).reset_index()
    
    # 6. Fill missing values with 0
    # Some hours might not have data for a specific day
    numeric_cols = [c for c in pivoted.columns if c != 'date_only']
    pivoted[numeric_cols] = pivoted[numeric_cols].fillna(0)
    
    # 7. Format the date_only column into the target 'cst' format
    # '%a %m/%d/%Y' e.g., 'Mon 01/01/2018'
    pivoted['cst'] = pd.to_datetime(pivoted['date_only']).dt.strftime('%a %m/%d/%Y')
    
    # 8. Define the target columns in order
    target_columns = ['cst'] + [f"{i}:00" for i in range(1, 25)]
    
    # 9. Ensure all target columns exist (in case some hours are completely missing from source)
    for col in target_columns:
        if col not in pivoted.columns:
            pivoted[col] = 0
            
    # 10. Select and return the final columns
    return pivoted[target_columns]