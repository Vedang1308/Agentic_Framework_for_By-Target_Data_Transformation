import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    df = source.copy()
    
    # Identify numeric columns to clean
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    
    # Replace sentinel value 32767 with 0
    df[numeric_cols] = df[numeric_cols].replace(32767, 0)
    
    # Define HVAC components
    hvac_cols = [
        'AC COMPRESSOR WHS [emon ch3,4]',
        'AIR HANDLER WHS [emon ch5,6]',
        'Minisplit WHS (2-CTs) [xpod chA-7,8]'
    ]
    df['hvac'] = df[hvac_cols].sum(axis=1)
    
    # Define Domestic Water Heating
    df['domestic_water_heating'] = df['WATER HEATER WHS [emon ch7,8]']
    
    # Define Major Appliances
    major_appliance_cols = [
        'DRYER WHS (1-CT) [emon ch9]',
        'RANGE WHS (1-CT) [emon ch10]',
        'DISH WASHER WHS [emon ch11]',
        'Primary Fridge WHS [emon ch12]',
        '2nd Fridge WHS [emon ch13]',
        'Dryer WHS (2-CTs) [xpod chA-9,10]'
    ]
    df['major_appliances'] = df[major_appliance_cols].sum(axis=1)
    
    # Define Lighting (Assumed 0 based on target sample and lack of source column)
    df['lighting'] = 0
    
    # Define Miscellaneous Plug Loads
    df['miscellaneous_plug_loads'] = df['Calculated Unmeasured loads (Whr)']
    
    # Define Total
    df['total'] = df['TOTAL BLDG WHS [emon ch1,2]']
    
    # Group by timestamp and sum
    # Note: timestamp is object, so we group by the string value
    agg_df = df.groupby('timestamp', as_index=False).agg({
        'hvac': 'sum',
        'domestic_water_heating': 'sum',
        'major_appliances': 'sum',
        'lighting': 'sum',
        'miscellaneous_plug_loads': 'sum',
        'total': 'sum'
    })
    
    # Rename timestamp to datetime
    agg_df = agg_df.rename(columns={'timestamp': 'datetime'})
    
    # Ensure datetime is formatted correctly as string if it isn't already
    # The source is object, likely already 'YYYY-MM-DD HH:MM:SS'
    # Just to be safe, we can ensure it's a string
    agg_df['datetime'] = agg_df['datetime'].astype(str)
    
    # Define target columns
    target_columns = ['datetime', 'hvac', 'domestic_water_heating', 'major_appliances', 'lighting', 'miscellaneous_plug_loads', 'total']
    
    # Ensure correct dtypes as per target schema
    # hvac, domestic_water_heating, major_appliances, lighting, total are int64
    # miscellaneous_plug_loads is float64
    agg_df['hvac'] = agg_df['hvac'].astype('int64')
    agg_df['domestic_water_heating'] = agg_df['domestic_water_heating'].astype('int64')
    agg_df['major_appliances'] = agg_df['major_appliances'].astype('int64')
    agg_df['lighting'] = agg_df['lighting'].astype('int64')
    agg_df['total'] = agg_df['total'].astype('int64')
    # miscellaneous_plug_loads remains float64
    
    return agg_df[target_columns]