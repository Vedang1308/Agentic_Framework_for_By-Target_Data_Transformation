import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame with minute-level data into a target DataFrame
    with daily aggregates pivoted into hourly columns (Hr 1 to Hr 24).
    """
    df = source.copy()
    
    # 1. Parse the date column
    # The format is M/D/YYYY H:MM
    df['dt'] = pd.to_datetime(df['date'])
    
    # 2. Extract date and hour
    # Target Date format is MM/DD/YYYY
    df['Date'] = df['dt'].dt.strftime('%m/%d/%Y')
    
    # Extract hour (0-23)
    df['hour_int'] = df['dt'].dt.hour
    
    # 3. Map hour 0-23 to target column names 'Hr 1'-'Hr 24'
    # Based on sample: Source hour 0 (0:11) maps to Target 'Hr 1'
    df['hour_col_name'] = df['hour_int'].apply(lambda h: f'Hr {h + 1}')
    
    # 4. Aggregate
    # Group by Date and the new hour column name, then take the mean of zone_016
    # Using mean handles multiple rows per hour.
    aggregated = df.groupby(['Date', 'hour_col_name'])['zone_016'].mean().reset_index()
    
    # 5. Pivot
    # Rows: Date, Columns: hour_col_name, Values: zone_016
    pivoted = aggregated.pivot(index='Date', columns='hour_col_name', values='zone_016')
    
    # 6. Clean up column names and structure
    pivoted.columns.name = None
    pivoted = pivoted.reset_index()
    
    # 7. Ensure all 24 hour columns exist
    target_hour_cols = [f'Hr {i}' for i in range(1, 25)]
    
    # Add any missing hour columns with NaN
    for col in target_hour_cols:
        if col not in pivoted.columns:
            pivoted[col] = np.nan
            
    # 8. Select and order columns to match target schema exactly
    final_columns = ['Date'] + target_hour_cols
    result = pivoted[final_columns]
    
    # 9. Sort by Date to ensure consistent ordering (optional but good practice)
    # The target sample shows 01/02 then 01/01, which is reverse chronological or arbitrary.
    # Usually, we just return the rows. The prompt doesn't specify sort order, 
    # but typically preserving input order or sorting by date is standard. 
    # Given the target sample order (01/02, 01/01), it might be reverse chronological 
    # or just the order of appearance in the source if source was reverse.
    # However, without explicit instruction, standard pandas groupby preserves order of first appearance 
    # if sort=False (default in newer pandas) or sorted if sort=True.
    # Let's just return the columns as required.
    
    return result