import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Transform the date column
    # Source format: '%m/%d/%Y' (e.g., '7/3/2015')
    # Target format: '%Y-%m-%d %H:%M:%S' (e.g., '2015-01-01 00:00:00')
    dt = pd.to_datetime(df['date'], format='%m/%d/%Y')
    df['date'] = dt.dt.strftime('%Y-%m-%d 00:00:00')
    
    # 2. Define the mapping from Source 'Hour N' to Target labels
    # The target columns are in a specific order that maps positionally to Hours 1-24
    target_hour_labels = [
        '1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', '6:00 AM', 
        '7:00 AM', '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM', '12:00 AM', 
        '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', '6:00 PM', 
        '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM', '12:00 PM'
    ]
    
    rename_dict = {}
    for i, label in enumerate(target_hour_labels, start=1):
        rename_dict[f'Hour {i}'] = label
        
    df = df.rename(columns=rename_dict)
    
    # 3. Define the target column order
    target_columns = ['date'] + target_hour_labels
    
    # 4. Ensure correct data types if necessary
    # Source Hour 9-16 are int64, Target 9:00 AM - 4:00 PM are int64.
    # Renaming preserves dtype, but let's explicitly cast to ensure strict compliance
    # with the target schema description if pandas inferred differently during operations.
    # However, since we only rename and format date, dtypes should be preserved.
    # Just to be safe for the 'date' column which is object/string.
    
    # Select and return
    return df[target_columns]