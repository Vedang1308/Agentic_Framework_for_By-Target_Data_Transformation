import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame into the target DataFrame by:
    1. Parsing the date column.
    2. Extracting the calendar date and hour.
    3. Mapping hours 0-23 to labels '1:00'-'24:00'.
    4. Summing the cooling setpoint values for each hour per day.
    5. Pivoting to wide format.
    6. Formatting the date column as required.
    """
    # 1. Parse the date column
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract calendar date and hour
    df['cst_date'] = df['datetime'].dt.date
    df['hour'] = df['datetime'].dt.hour
    
    # 3. Map hours to target column labels
    # Hypothesis: Hour 0 (00:xx) -> '1:00', Hour 1 (01:xx) -> '2:00', ..., Hour 23 (23:xx) -> '24:00'
    df['hour_label'] = (df['hour'] + 1).astype(str) + ':00'
    
    # 4. Aggregate by date and hour label
    # The target values (876) are 12 * 73. This implies a SUM aggregation.
    agg_df = df.groupby(['cst_date', 'hour_label'])['zone_016_cooling_sp'].sum().reset_index()
    
    # 5. Pivot to wide format
    pivot_df = agg_df.pivot(index='cst_date', columns='hour_label', values='zone_016_cooling_sp')
    
    # 6. Ensure all 24 hour columns exist, filling missing ones with 0 (or NaN if preferred, but 0 is safer for sums)
    # Generate expected column names
    expected_cols = [f"{h}:00" for h in range(1, 25)]
    
    # Reindex columns to ensure order and presence
    pivot_df = pivot_df.reindex(columns=expected_cols)
    
    # Fill NaNs with 0 if any hours are missing for a day
    pivot_df = pivot_df.fillna(0)
    
    # 7. Format the index as the 'cst' column string
    # Format: '%a %m/%d/%Y'
    pivot_df.index = pd.to_datetime(pivot_df.index).strftime('%a %m/%d/%Y')
    
    # 8. Reset index to make 'cst_date' a column named 'cst'
    pivot_df = pivot_df.reset_index()
    pivot_df = pivot_df.rename(columns={'index': 'cst'})
    
    # 9. Define target columns
    target_columns = ['cst'] + [f"{h}:00" for h in range(1, 25)]
    
    # 10. Select and return columns in the correct order
    # Ensure numeric columns are float64
    for col in target_columns[1:]:
        pivot_df[col] = pivot_df[col].astype(float)
        
    return pivot_df[target_columns]