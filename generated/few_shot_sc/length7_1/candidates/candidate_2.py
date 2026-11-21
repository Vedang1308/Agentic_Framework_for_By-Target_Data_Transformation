import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    df = source.copy()
    
    # 1. Parse the CST column
    # Format is 'Sat 12/01/2012' -> '%a %m/%d/%Y'
    df['dt'] = pd.to_datetime(df['CST'], format='%a %m/%d/%Y')
    
    # 2. Extract Month Name
    df['month'] = df['dt'].dt.strftime('%B')
    
    # 3. Determine Day Type (weekday vs weekend)
    # dayofweek: Monday=0, ..., Sunday=6
    # Weekend is Saturday (5) and Sunday (6)
    df['daytype'] = df['dt'].dt.dayofweek.apply(lambda x: 'weekend' if x >= 5 else 'weekday')
    
    # 4. Rename Hour Columns
    # Source: '1:00', '2:00', ..., '23:00', '24:00:00'
    # Target: 'hr1', 'hr2', ..., 'hr23', 'hr24'
    rename_dict = {}
    for i in range(1, 24):
        rename_dict[f'{i}:00'] = f'hr{i}'
    # Handle the last column specifically as it might be '24:00:00' or '24:00'
    if '24:00:00' in df.columns:
        rename_dict['24:00:00'] = 'hr24'
    elif '24:00' in df.columns:
        rename_dict['24:00'] = 'hr24'
        
    df = df.rename(columns=rename_dict)
    
    # 5. Aggregate
    # Group by month and daytype, and take the mean of the hourly columns
    # This collapses multiple days into a single "typical" profile per month/daytype
    hourly_cols = [f'hr{i}' for i in range(1, 25)]
    
    # Select only the necessary columns for grouping and aggregation to avoid issues with other columns
    agg_df = df.groupby(['month', 'daytype'])[hourly_cols].mean()
    
    # 6. Reset Index and Format Output
    agg_df = agg_df.reset_index()
    
    # Define target columns in correct order
    target_columns = ['month', 'daytype'] + [f'hr{i}' for i in range(1, 25)]
    
    # Return only the target columns
    return agg_df[target_columns]