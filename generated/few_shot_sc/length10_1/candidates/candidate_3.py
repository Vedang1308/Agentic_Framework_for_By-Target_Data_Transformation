import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    df = source.copy()
    
    # 1. Parse and format datetime
    # Source 'time' is like '2012-07-02 00:15:00.000'
    # Target 'datetime' is '2012-01-01 00:15:00'
    df['datetime'] = pd.to_datetime(df['time']).dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # 2. Map and compute target columns
    
    # hvac: Sum of heating and cooling electricity
    df['hvac'] = df['electricity_heating_kwh'] + df['electricity_cooling_kwh']
    
    # water_heating: Direct mapping
    df['water_heating'] = df['electricity_water_systems_kwh']
    
    # refrigerator: Direct mapping
    df['refrigerator'] = df['electricity_refrigerator_kwh']
    
    # clothes_washer: Direct mapping
    df['clothes_washer'] = df['electricity_clothes_washer_kwh']
    
    # clothes_dryer: Direct mapping
    df['clothes_dryer'] = df['electricity_clothes_dryer_kwh']
    
    # dishwasher: Direct mapping
    df['dishwasher'] = df['electricity_dishwasher_kwh']
    
    # cooking_range: Direct mapping
    df['cooking_range'] = df['electricity_cooking_range_kwh']
    
    # pool_spa_pumps: Sum of pool pump and hot tub pump
    df['pool_spa_pumps'] = df['electricity_pool_pump_kwh'] + df['electricity_hot_tub_pump_kwh']
    
    # interior_lighting: Direct mapping
    df['interior_lighting'] = df['electricity_interior_lighting_kwh']
    
    # exterior_lighting: Direct mapping
    df['exterior_lighting'] = df['electricity_exterior_lighting_kwh']
    
    # lighting: Sum of interior and exterior
    df['lighting'] = df['interior_lighting'] + df['exterior_lighting']
    
    # plug: Direct mapping
    df['plug'] = df['electricity_plug_loads_kwh']
    
    # pool_spa_heater: Sum of pool heater and hot tub heater
    df['pool_spa_heater'] = df['electricity_pool_heater_kwh'] + df['electricity_hot_tub_heater_kwh']
    
    # 3. Select target columns verbatim
    target_columns = [
        'datetime', 'hvac', 'water_heating', 'refrigerator', 'clothes_washer', 
        'clothes_dryer', 'dishwasher', 'cooking_range', 'pool_spa_pumps', 
        'interior_lighting', 'exterior_lighting', 'lighting', 'plug', 'pool_spa_heater'
    ]
    
    return df[target_columns]