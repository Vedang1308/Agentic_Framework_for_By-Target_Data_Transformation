import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # 1. Parse the date column
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract Date and Hour
    # Extract the calendar date
    df['date_only'] = df['datetime'].dt.date
    
    # Extract hour (0-23) and map to 1-24 for column names 'Hr 1' to 'Hr 24'
    df['hour_num'] = df['datetime'].dt.hour + 1
    df['hour_label'] = df['hour_num'].apply(lambda x: f'Hr {x}')
    
    # 3. Aggregate data
    # Group by date and hour label, then take the mean of zone_016
    # Using mean handles multiple minutes within an hour and ignores NaNs if skipna=True
    grouped = df.groupby(['date_only', 'hour_label'])['zone_016'].mean().reset_index()
    
    # 4. Pivot the data
    # Rows: date_only, Columns: hour_label, Values: zone_016
    pivoted = grouped.pivot_table(index='date_only', columns='hour_label', values='zone_016', aggfunc='mean')
    
    # 5. Ensure all 24 hour columns exist
    expected_hours = [f'Hr {i}' for i in range(1, 25)]
    pivoted = pivoted.reindex(columns=expected_hours)
    
    # 6. Format the Date column
    # Convert index back to a column
    pivoted = pivoted.reset_index()
    pivoted['Date'] = pivoted['date_only'].apply(lambda x: pd.Timestamp(x).strftime('%m/%d/%Y'))
    
    # 7. Select and order columns
    target_columns = ['Date'] + expected_hours
    
    # Ensure the final dataframe has exactly these columns
    df_result = pivoted[target_columns]
    
    return df_result