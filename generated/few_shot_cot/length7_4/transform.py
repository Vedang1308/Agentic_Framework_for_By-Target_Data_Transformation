import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the date column
    df['date_parsed'] = pd.to_datetime(df['date'], format='%m/%d/%Y')
    
    # 2. Create 'month' column with full month name
    df['month'] = df['date_parsed'].dt.strftime('%B')
    
    # 3. Create 'daytype' column: 'weekday' for Mon-Fri, 'weekend' for Sat-Sun
    # dayofweek: 0=Mon, 1=Tue, 2=Wed, 3=Thu, 4=Fri, 5=Sat, 6=Sun
    df['daytype'] = df['date_parsed'].dt.dayofweek.apply(lambda x: 'weekday' if x < 5 else 'weekend')
    
    # 4. Rename value columns to hr columns
    rename_dict = {f'value{i}': f'hr{i}' for i in range(1, 25)}
    df = df.rename(columns=rename_dict)
    
    # 5. Define target columns
    target_columns = ['month', 'daytype'] + [f'hr{i}' for i in range(1, 25)]
    
    # 6. Return the transformed dataframe with only target columns
    return df[target_columns]