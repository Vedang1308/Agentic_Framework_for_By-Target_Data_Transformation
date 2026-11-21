import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    df = source.copy()
    
    # 1. Parse the Date column to datetime to ensure correct formatting and sorting
    df['parsed_date'] = pd.to_datetime(df['Date'])
    
    # 2. Format the date as MM/DD/YYYY for the target 'date' column
    df['date'] = df['parsed_date'].dt.strftime('%m/%d/%Y')
    
    # 3. Rename the hour columns from '1'..'24' to 'Hour 1'..'Hour 24'
    # The source schema indicates columns 1-24. They might be int or str in column names.
    # We create a mapping for both possibilities to be safe, though str is common from CSV.
    rename_dict = {}
    for i in range(1, 25):
        if str(i) in df.columns:
            rename_dict[str(i)] = f'Hour {i}'
        if i in df.columns:
            rename_dict[i] = f'Hour {i}'
            
    df = df.rename(columns=rename_dict)
    
    # 4. Drop unnecessary columns: 'Date', 'Class', 'parsed_date'
    cols_to_drop = ['Date', 'Class', 'parsed_date']
    df = df.drop(columns=[c for c in cols_to_drop if c in df.columns])
    
    # 5. Sort by date to match the target's chronological order
    # We use the parsed_date for sorting if we kept it, but we dropped it. 
    # Let's re-parse or sort by the string 'date' if it's consistent (MM/DD/YYYY sorts correctly alphabetically).
    df = df.sort_values(by='date').reset_index(drop=True)
    
    # 6. Define target columns verbatim
    target_columns = ['date'] + [f'Hour {i}' for i in range(1, 25)]
    
    return df[target_columns]