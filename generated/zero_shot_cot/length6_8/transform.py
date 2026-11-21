import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame with 'date' and 'cerc_logger_1' into a target DataFrame
    with 'Date' and hourly aggregated columns 'Hr 1' through 'Hr 24'.
    """
    # 1. Parse the date column
    # The format is '%m/%d/%Y %H:%M'
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract Date and Hour
    # Target Date format is '%m/%d/%Y'
    df['Date'] = df['datetime'].dt.strftime('%m/%d/%Y')
    
    # Target Hours are 1-indexed (Hr 1 corresponds to hour 0, Hr 24 to hour 23)
    df['Hour_Index'] = df['datetime'].dt.hour + 1
    
    # 3. Aggregate
    # Group by Date and Hour_Index, and calculate the mean of cerc_logger_1
    # Using mean as it's the standard aggregation for sensor data over time intervals
    aggregated = df.groupby(['Date', 'Hour_Index'])['cerc_logger_1'].mean().reset_index()
    
    # 4. Pivot
    # Pivot the table so that Hour_Index becomes columns
    pivoted = aggregated.pivot(index='Date', columns='Hour_Index', values='cerc_logger_1')
    
    # 5. Rename Columns
    # The columns are currently integers 1-24. We need to rename them to 'Hr 1', 'Hr 2', etc.
    pivoted.columns = [f'Hr {col}' for col in pivoted.columns]
    
    # 6. Reset Index to make Date a column
    result = pivoted.reset_index()
    
    # 7. Define target columns
    target_columns = ['Date'] + [f'Hr {i}' for i in range(1, 25)]
    
    # 8. Ensure all target columns exist (in case some hours are missing in data)
    # Fill missing hours with NaN if necessary, though pivot usually handles this by creating NaNs
    for col in target_columns:
        if col not in result.columns:
            result[col] = np.nan
            
    # 9. Select and order columns
    result = result[target_columns]
    
    # 10. Sort by Date? The target sample seems sorted by Date descending or arbitrary.
    # The problem doesn't specify sort order, but usually, we preserve the order of appearance or sort.
    # Looking at the target sample: 05/08, 05/07, 03/10... it's not strictly sorted.
    # However, groupby usually preserves the order of first appearance or sorts.
    # To be safe and deterministic, we can sort by Date descending or just return as is.
    # Given the "general" requirement, standard groupby/pivot behavior is acceptable.
    # Let's sort by Date descending to match the sample's apparent trend (newer dates first)?
    # Sample: 05/08/2019, 05/07/2019, 03/10/2018...
    # It looks like it might be sorted by Date descending.
    # Let's parse the Date back to datetime for sorting if needed, but string sort works for MM/DD/YYYY if consistent.
    # Actually, MM/DD/YYYY string sort is NOT chronological.
    # 05/08/2019 vs 03/10/2018.
    # Let's just return the result. The specific row order in the target sample might just be a subset.
    # I will sort by Date descending to match the visual pattern of the sample (latest first).
    
    # Convert Date to datetime for proper sorting
    result['Date_dt'] = pd.to_datetime(result['Date'], format='%m/%d/%Y')
    result = result.sort_values('Date_dt', ascending=False).drop(columns=['Date_dt'])
    
    return result[target_columns]