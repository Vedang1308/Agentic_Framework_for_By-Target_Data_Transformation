import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # 1. Parse the date column to datetime
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract date string and hour
    # Format date as MM/DD/YYYY
    df['date_str'] = df['datetime'].dt.strftime('%m/%d/%Y')
    # Extract hour (0-23)
    df['hour'] = df['datetime'].dt.hour
    
    # 3. Determine the order of dates to preserve if necessary
    # The target sample shows 01/02/2018 before 01/01/2018.
    # The source sample starts with 1/2/2018.
    # It is likely that the order of rows in the target corresponds to the 
    # order of first appearance of each date in the source data.
    # We can capture this order before dropping duplicates.
    unique_dates_ordered = df['date_str'].drop_duplicates().tolist()
    
    # 4. Aggregate data by date and hour
    # We use mean to aggregate values within each hour for each day.
    # If there's only one value, mean is that value.
    aggregated = df.groupby(['date_str', 'hour'])['zone_016'].mean().reset_index()
    
    # 5. Pivot the data
    # Index: date_str
    # Columns: hour (0-23)
    # Values: zone_016
    pivoted = aggregated.pivot(index='date_str', columns='hour', values='zone_016')
    
    # 6. Rename columns from 0-23 to value1-value24
    # Map hour h to value(h+1)
    pivoted.columns = [f'value{h+1}' for h in pivoted.columns]
    
    # 7. Ensure all 24 value columns exist
    # Pivot will only create columns for hours present in the data.
    # We need to ensure value1 to value24 exist, filling missing with NaN.
    target_value_cols = [f'value{i}' for i in range(1, 25)]
    for col in target_value_cols:
        if col not in pivoted.columns:
            pivoted[col] = np.nan
            
    # 8. Reset index to make date_str a column
    pivoted = pivoted.reset_index()
    pivoted.rename(columns={'date_str': 'date'}, inplace=True)
    
    # 9. Reorder rows to match the order of first appearance in source
    # Create a mapping from date to its rank in the source
    date_to_rank = {date: i for i, date in enumerate(unique_dates_ordered)}
    pivoted['date_rank'] = pivoted['date'].map(date_to_rank)
    pivoted = pivoted.sort_values('date_rank').drop('date_rank', axis=1)
    
    # 10. Select and order the final columns
    target_columns = ['date'] + [f'value{i}' for i in range(1, 25)]
    
    # Ensure float type for value columns
    for col in target_columns[1:]:
        pivoted[col] = pivoted[col].astype(float)
        
    return pivoted[target_columns]