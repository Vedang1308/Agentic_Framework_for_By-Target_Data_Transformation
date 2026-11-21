import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # 1. Parse the date column to extract date and hour
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'])
    df['date_only'] = df['datetime'].dt.strftime('%m/%d/%Y')
    df['hour'] = df['datetime'].dt.hour
    
    # 2. Map hour (0-23) to value column names (value1-value24)
    # Hour 0 -> value1, Hour 1 -> value2, ..., Hour 23 -> value24
    df['value_col'] = 'value' + (df['hour'] + 1).astype(str)
    
    # 3. Pivot the table to wide format
    # Group by date_only, spread across value_col, aggregate zone_016 using mean
    pivot_df = df.pivot_table(
        index='date_only', 
        columns='value_col', 
        values='zone_016', 
        aggfunc='mean'
    )
    
    # 4. Ensure all 24 columns exist and are in the correct order
    # Define the expected columns
    target_value_cols = [f'value{i}' for i in range(1, 25)]
    
    # Reindex columns to ensure all value1...value24 are present, filling missing with NaN
    pivot_df = pivot_df.reindex(columns=target_value_cols)
    
    # 5. Reset index to make date_only a column
    pivot_df = pivot_df.reset_index()
    
    # 6. Rename index column to 'date' if necessary (it is already 'date_only')
    pivot_df = pivot_df.rename(columns={'date_only': 'date'})
    
    # 7. Sort by date descending to match the sample output order (01/02 before 01/01)
    # The sample shows 01/02/2018 then 01/01/2018.
    # To sort strings in MM/DD/YYYY format correctly as dates, we might need to parse again or rely on the string sort if consistent.
    # Since the format is MM/DD/YYYY, string sort is NOT chronological.
    # 01/01 < 01/02. Descending string sort: 01/02 > 01/01. This matches the sample.
    # However, if dates span months, string sort fails (12/01 < 01/01).
    # It is safer to sort by the actual date value.
    pivot_df['date_parsed'] = pd.to_datetime(pivot_df['date'], format='%m/%d/%Y')
    pivot_df = pivot_df.sort_values(by='date_parsed', ascending=False)
    pivot_df = pivot_df.drop(columns=['date_parsed'])
    
    # 8. Select and return the target columns
    target_columns = ['date', 'value1', 'value2', 'value3', 'value4', 'value5', 'value6', 'value7', 'value8', 'value9', 'value10', 'value11', 'value12', 'value13', 'value14', 'value15', 'value16', 'value17', 'value18', 'value19', 'value20', 'value21', 'value22', 'value23', 'value24']
    
    return pivot_df[target_columns]