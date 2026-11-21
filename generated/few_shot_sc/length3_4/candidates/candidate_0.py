import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse the datetime column
    df = source.copy()
    df['parsed_date'] = pd.to_datetime(df['date'])
    
    # 2. Extract date string for grouping and target 'date' column
    df['date_str'] = df['parsed_date'].dt.strftime('%m/%d/%Y')
    
    # 3. Extract hour and map to 'Hour 1' ... 'Hour 24'
    # Standard mapping: 00:00-01:00 is Hour 1, ..., 23:00-00:00 is Hour 24
    df['hour_num'] = df['parsed_date'].dt.hour + 1
    df['hour_label'] = 'Hour ' + df['hour_num'].astype(str)
    
    # 4. Pivot the data
    # Aggregate using 'first' to handle multiple entries per hour (constant values expected)
    pivot_df = df.pivot_table(
        index='date_str',
        columns='hour_label',
        values='zone_016_cooling_sp',
        aggfunc='first'
    )
    
    # 5. Ensure all 24 hour columns are present, even if empty
    target_hour_cols = [f'Hour {i}' for i in range(1, 25)]
    pivot_df = pivot_df.reindex(columns=target_hour_cols)
    
    # 6. Reset index to make date a column again
    pivot_df = pivot_df.reset_index()
    pivot_df = pivot_df.rename(columns={'date_str': 'date'})
    
    # 7. Define final column order
    target_columns = ['date'] + target_hour_cols
    
    # 8. Return the dataframe with exact target columns
    return pivot_df[target_columns]