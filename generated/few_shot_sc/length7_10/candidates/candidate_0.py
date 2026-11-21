import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the date column
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract features
    # Month name (e.g., 'August')
    df['month'] = df['datetime'].dt.strftime('%B')
    
    # Day type: 'weekday' (Mon-Fri) or 'weekend' (Sat-Sun)
    # dayofweek: Monday=0, ..., Friday=4, Saturday=5, Sunday=6
    df['daytype'] = df['datetime'].dt.dayofweek.apply(lambda x: 'weekday' if x < 5 else 'weekend')
    
    # Hour mapping: Source hour 0 -> hr1, 1 -> hr2, ..., 23 -> hr24
    df['hr_label'] = 'hr' + (df['datetime'].dt.hour + 1).astype(str)
    
    # 3. Aggregate
    # Group by month, daytype, and hr_label, then calculate the mean of cerc_logger_1
    grouped = df.groupby(['month', 'daytype', 'hr_label'])['cerc_logger_1'].mean().reset_index()
    
    # 4. Pivot to wide format
    # Rows: month, daytype
    # Columns: hr_label (hr1, hr2, ..., hr24)
    # Values: mean cerc_logger_1
    pivot_df = grouped.pivot_table(index=['month', 'daytype'], columns='hr_label', values='cerc_logger_1', aggfunc='mean')
    
    # Reset index to make month and daytype columns again
    pivot_df = pivot_df.reset_index()
    
    # Rename columns to remove potential multi-index level names if any
    pivot_df.columns.name = None
    
    # 5. Ensure correct column order and names
    # Generate expected hour columns
    hr_columns = [f'hr{i}' for i in range(1, 25)]
    
    # Define final target columns
    target_columns = ['month', 'daytype'] + hr_columns
    
    # Select and order columns. 
    # Note: pivot_table might not have all hr columns if data is missing for some hours.
    # We should reindex to ensure all hr1-hr24 exist, filling NaN if necessary.
    pivot_df = pivot_df.reindex(columns=target_columns)
    
    return pivot_df[target_columns]