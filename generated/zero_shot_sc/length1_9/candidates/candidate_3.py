import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # Define target columns verbatim
    target_columns = ['cst', '1:00', '2:00', '3:00', '4:00', '5:00', '6:00', '7:00', '8:00', '9:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00', '24:00']
    
    # 1. Parse the date column
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract hour and create bucket index
    # Source hour 0 (00:xx) -> Target column "1:00"
    # Source hour 23 (23:xx) -> Target column "24:00"
    df['hour_bucket'] = df['datetime'].dt.hour + 1
    
    # 3. Format the date for the 'cst' column
    # Format: %a %m/%d/%Y (e.g., Mon 01/01/2018)
    df['cst'] = df['datetime'].dt.strftime('%a %m/%d/%Y')
    
    # 4. Create column names for the pivot
    df['time_col'] = df['hour_bucket'].apply(lambda h: f"{h}:00")
    
    # 5. Aggregate by summing zone_016 for each date and hour bucket
    # Group by 'cst' and 'time_col', sum 'zone_016'
    agg_df = df.groupby(['cst', 'time_col'])['zone_016'].sum().reset_index()
    
    # 6. Pivot the table
    pivot_df = agg_df.pivot(index='cst', columns='time_col', values='zone_016')
    
    # 7. Fill missing values with 0
    pivot_df = pivot_df.fillna(0)
    
    # 8. Ensure all 24 hour columns exist and are in the correct order
    # Create a list of expected column names
    expected_hour_cols = [f"{h}:00" for h in range(1, 25)]
    
    # Reindex columns to ensure all expected hours are present, filling missing ones with 0
    pivot_df = pivot_df.reindex(columns=expected_hour_cols, fill_value=0)
    
    # 9. Reset index to make 'cst' a column
    pivot_df = pivot_df.reset_index()
    
    # 10. Rename 'cst' if necessary (it should already be 'cst')
    # Ensure column names match exactly
    pivot_df = pivot_df.rename(columns={col: col for col in pivot_df.columns})
    
    # 11. Select and order columns as per target_schema
    result_df = pivot_df[target_columns]
    
    return result_df