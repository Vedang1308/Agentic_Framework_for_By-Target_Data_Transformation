import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # 1. Parse the date column
    df = source.copy()
    df['parsed_date'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract components for grouping
    # The target 'cst' format is '%a %m/%d/%Y'
    df['cst'] = df['parsed_date'].dt.strftime('%a %m/%d/%Y')
    
    # Extract hour (0-23)
    df['hour'] = df['parsed_date'].dt.hour
    
    # 3. Map hours to target column labels
    # Hour 0 maps to '24:00', Hours 1-23 map to '1:00'-'23:00'
    def get_hour_label(h):
        if h == 0:
            return '24:00'
        else:
            return f'{h}:00'
            
    df['hour_label'] = df['hour'].apply(get_hour_label)
    
    # 4. Group by 'cst' and 'hour_label' and sum the values
    # Using sum() to aggregate the zone_016 values
    grouped = df.groupby(['cst', 'hour_label'])['zone_016'].sum().reset_index()
    
    # 5. Pivot the data to wide format
    # Index: cst, Columns: hour_label, Values: zone_016
    pivoted = grouped.pivot(index='cst', columns='hour_label', values='zone_016')
    
    # 6. Handle missing combinations (fill with 0)
    pivoted = pivoted.fillna(0)
    
    # 7. Ensure all required columns exist and are in the correct order
    target_columns = ['cst', '1:00', '2:00', '3:00', '4:00', '5:00', '6:00', '7:00', '8:00', '9:00', 
                      '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', 
                      '19:00', '20:00', '21:00', '22:00', '23:00', '24:00']
    
    # Extract the hour columns from the target list (excluding 'cst')
    hour_cols = target_columns[1:]
    
    # Ensure all hour columns exist in the pivoted dataframe, adding missing ones with 0
    for col in hour_cols:
        if col not in pivoted.columns:
            pivoted[col] = 0
            
    # Reset index to make 'cst' a column
    pivoted = pivoted.reset_index()
    
    # 8. Sort by date (optional but ensures consistent ordering)
    # Parse cst back to datetime for sorting, then drop the helper
    pivoted['sort_key'] = pd.to_datetime(pivoted['cst'], format='%a %m/%d/%Y')
    pivoted = pivoted.sort_values('sort_key').drop('sort_key', axis=1)
    
    # 9. Select and return only the required columns in the exact order
    return pivoted[target_columns]