import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame into the target DataFrame by:
    1. Parsing and reformatting the date column.
    2. Renaming value columns to Hour columns.
    3. Selecting and ordering the final columns.
    """
    # Create a copy to avoid modifying the original source
    df = source.copy()
    
    # 1. Parse the date column and format it to 'YYYY-MM-DD HH:MM:SS'
    # The source date is in 'M/D/YYYY' format.
    # The target requires 'YYYY-MM-DD HH:MM:SS' with time 00:00:00.
    df['Date'] = pd.to_datetime(df['date'], format='%m/%d/%Y').dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # 2. Rename value columns to Hr columns
    # Mapping value1 -> Hr 1, value2 -> Hr 2, etc.
    rename_map = {}
    for i in range(1, 25):
        rename_map[f'value{i}'] = f'Hr {i}'
    
    df.rename(columns=rename_map, inplace=True)
    
    # 3. Define the target columns in the correct order
    target_columns = ['Date'] + [f'Hr {i}' for i in range(1, 25)]
    
    # 4. Select only the required columns
    # We drop the original metadata columns (class, Description, analysis, uom) and the original 'date' column
    df = df[target_columns]
    
    # 5. Ensure numeric columns are float64 (they likely already are, but explicit is safe)
    for col in [f'Hr {i}' for i in range(1, 25)]:
        df[col] = df[col].astype(float)
        
    return df[target_columns]