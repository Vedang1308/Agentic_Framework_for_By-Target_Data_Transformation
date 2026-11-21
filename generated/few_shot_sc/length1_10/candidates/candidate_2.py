import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    df = source.copy()
    
    # Parse the date column
    df['dt'] = pd.to_datetime(df['date'])
    
    # Extract date and hour
    # We use normalize() to get the date at 00:00:00 for grouping
    df['date_group'] = df['dt'].dt.normalize()
    
    # Map pandas hour (0-23) to target hour (1-24)
    # 0 -> 1, 1 -> 2, ..., 23 -> 24
    df['hour_group'] = df['dt'].dt.hour + 1
    
    # Group by date and hour, sum the cooling_sp values
    # This aggregates the 5-minute intervals into hourly totals
    aggregated = df.groupby(['date_group', 'hour_group'])['zone_016_cooling_sp'].sum()
    
    # Pivot the data to have hours as columns
    # Index: date_group, Columns: hour_group, Values: sum
    pivoted = aggregated.unstack(level='hour_group')
    
    # Ensure all 24 hours are present as columns, filling missing with 0 if necessary
    expected_hours = range(1, 25)
    pivoted = pivoted.reindex(columns=expected_hours, fill_value=0)
    
    # Rename columns to match target format '1:00', '2:00', ...
    pivoted.columns = [f'{h}:00' for h in pivoted.columns]
    
    # Format the index (date) as required: '%a %m/%d/%Y'
    pivoted.index = pivoted.index.strftime('%a %m/%d/%Y')
    
    # Rename the index to 'cst' and reset to make it a column
    pivoted.index.name = 'cst'
    result = pivoted.reset_index()
    
    # Define target columns verbatim
    target_columns = ['cst'] + [f'{h}:00' for h in range(1, 25)]
    
    # Return the dataframe with exact target columns
    return result[target_columns]