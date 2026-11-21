import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms source DataFrame with high-frequency data into a daily pivoted DataFrame
    with hourly columns formatted in 12-hour AM/PM style.
    """
    df = source.copy()
    
    # 1. Parse the datetime column
    df['datetime'] = pd.to_datetime(df['date'])
    
    # 2. Extract date string for grouping/index
    df['date_str'] = df['datetime'].dt.strftime('%m/%d/%Y')
    
    # 3. Extract hour (0-23)
    df['hour'] = df['datetime'].dt.hour
    
    # 4. Map hour to target column names
    def map_hour_to_label(h):
        if h == 0:
            return '12:00 AM'
        elif 1 <= h <= 11:
            return f'{h}:00 AM'
        elif h == 12:
            return '12:00 PM'
        else:
            return f'{h-12}:00 PM'
    
    df['hour_label'] = df['hour'].apply(map_hour_to_label)
    
    # 5. Pivot the data
    # We group by date_str and hour_label, aggregate the value (using 'first' as setpoints are constant),
    # then unstack to create columns.
    # Using pivot_table with aggfunc='first' handles duplicates within an hour.
    pivoted = df.pivot_table(
        index='date_str',
        columns='hour_label',
        values='zone_016_cooling_sp',
        aggfunc='first'
    )
    
    # 6. Define target columns in the required order
    target_columns = [
        '1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', '6:00 AM', 
        '7:00 AM', '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM', '12:00 PM', 
        '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', '6:00 PM', 
        '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM', '12:00 AM'
    ]
    
    # 7. Reset index to make 'date_str' a column, rename it to 'date'
    pivoted = pivoted.reset_index()
    pivoted = pivoted.rename(columns={'date_str': 'date'})
    
    # 8. Select and order columns to match target schema exactly
    # Ensure all target columns exist (missing ones will be NaN, which is correct)
    return pivoted[target_columns]