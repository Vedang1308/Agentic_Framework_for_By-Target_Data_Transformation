import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Format datetime
    # The source 'time' column contains strings like '2012-07-02 00:15:00.000'
    dt = pd.to_datetime(df['time'])
    df['datetime'] = dt.dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # 2. Map and aggregate columns
    
    # hvac: Sum of heating, cooling, and associated fans/pumps
    hvac_cols = [
        'electricity_heating_kwh',
        'electricity_cooling_kwh',
        'electricity_fans_heating_kwh',
        'electricity_fans_cooling_kwh',
        'electricity_pumps_heating_kwh',
        'electricity_pumps_cooling_kwh',
        'electricity_central_system_heating_kwh',
        'electricity_central_system_cooling_kwh',
        'electricity_central_system_pumps_heating_kwh',
        'electricity_central_system_pumps_cooling_kwh'
    ]
    df['hvac'] = df[hvac_cols].sum(axis=1)
    
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
    
    # 3. Select target columns in the correct order
    target_columns = [
        'datetime', 'hvac', 'water_heating', 'refrigerator', 'clothes_washer', 
        'clothes_dryer', 'dishwasher', 'cooking_range', 'pool_spa_pumps', 
        'interior_lighting', 'exterior_lighting', 'lighting', 'plug', 'pool_spa_heater'
    ]
    
    return df[target_columns]