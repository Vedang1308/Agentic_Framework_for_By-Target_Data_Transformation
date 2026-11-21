import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms source DataFrame with 'date' and 'cerc_logger_1' into a target DataFrame
    with 'cst' and hourly columns '1:00' through '24:00'.
    """
    # 1. Parse the date column
    # Format is %m/%d/%Y %H:%M
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract day and hour
    df['day'] = df['datetime'].dt.date
    df['hour'] = df['datetime'].dt.hour
    
    # 3. Map hour 0 to 24 to match target column '24:00'
    # Target columns are 1:00 to 24:00. 
    # Standard hour 0 (00:00-00:59) corresponds to the 24th hour of the previous day or start of day.
    # Given the column '24:00' exists and '0:00' does not, we map hour 0 -> 24.
    df['hour_mapped'] = df['hour'].replace(0, 24)
    
    # 4. Aggregate
    # Group by day and mapped hour, sum the values.
    # Based on target values (~130-140) vs source values (~24), and ~6 readings/hour,
    # Sum is the likely aggregation. Mean would be ~24.
    agg_df = df.groupby(['day', 'hour_mapped'])['cerc_logger_1'].sum().reset_index()
    
    # 5. Pivot
    # Pivot so days are rows and hours are columns
    pivot_df = agg_df.pivot(index='day', columns='hour_mapped', values='cerc_logger_1')
    
    # 6. Handle missing values
    # If an hour has no data, it should be 0 (as seen in the sample row with all 0s)
    pivot_df = pivot_df.fillna(0)
    
    # 7. Format Columns
    # Convert column integers to strings like "1:00", "2:00", ..., "24:00"
    pivot_df.columns = [f"{h}:00" for h in pivot_df.columns]
    
    # 8. Ensure column order: 1:00 to 24:00
    # The columns might not be sorted if we just used the mapped hours directly without sorting
    # We need to explicitly order them 1..23, then 24
    ordered_hours = [f"{h}:00" for h in range(1, 24)] + ["24:00"]
    pivot_df = pivot_df[ordered_hours]
    
    # 9. Format Index
    # Convert the date index to the required string format: '%a %m/%d/%Y'
    # Example: Sat 07/20/2019
    pivot_df.index = pd.to_datetime(pivot_df.index).strftime('%a %m/%d/%Y')
    
    # 10. Reset index to make 'cst' a column
    pivot_df = pivot_df.reset_index()
    pivot_df = pivot_df.rename(columns={'index': 'cst'})
    
    # 11. Define target columns
    target_columns = ['cst', '1:00', '2:00', '3:00', '4:00', '5:00', '6:00', '7:00', '8:00', '9:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00', '24:00']
    
    # 12. Return with exact column names
    return pivot_df[target_columns]