import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the timestamp column
    source['timestamp'] = pd.to_datetime(source['timestamp'], format='%Y-%m-%d %H:%M:%S')
    
    # Extract the hour
    source['hour'] = source['timestamp'].dt.hour
    
    # Determine the season based on the month
    def get_season(month):
        if month in [6, 7, 8]:
            return 'Summer'
        elif month in [9, 10, 11]:
            return 'Fall'
        elif month in [12, 1, 2]:
            return 'Winter'
        else:
            return 'Spring'
    
    source['season'] = source['timestamp'].dt.month.apply(get_season)
    
    # Map source columns to target columns
    source['hvac'] = source['AC COMPRESSOR WHS [emon ch3,4]'] + source['AIR HANDLER WHS [emon ch5,6]']
    source['water_heating'] = source['WATER HEATER WHS [emon ch7,8]']
    source['refrigerator'] = source['Primary Fridge WHS [emon ch12]'] + source['2nd Fridge WHS [emon ch13]']
    source['clothes_washer'] = source['Wattsup Energy Washer (WHS)']
    source['clothes_dryer'] = source['DRYER WHS (1-CT) [emon ch9]'] + source['Dryer WHS (2-CTs) [xpod chA-9,10]']
    source['dishwasher'] = source['DISH WASHER WHS [emon ch11]']
    source['cooking_range'] = source['RANGE WHS (1-CT) [emon ch10]']
    source['pool_spa_pumps'] = source['POOL PUMP WHS (2-CTs) [xpod chA-3,4]']
    source['interior_lighting'] = 0
    source['exterior_lighting'] = 0
    source['lighting'] = source['interior_lighting'] + source['exterior_lighting']
    source['plug'] = 0
    source['pool_spa_heater'] = 0
    
    # Define the target columns
    target_columns = ['season', 'hour', 'hvac', 'water_heating', 'refrigerator', 'clothes_washer', 'clothes_dryer', 'dishwasher', 'cooking_range', 'pool_spa_pumps', 'interior_lighting', 'exterior_lighting', 'lighting', 'plug', 'pool_spa_heater']
    
    # Select the target columns
    df = source[target_columns]
    
    return df