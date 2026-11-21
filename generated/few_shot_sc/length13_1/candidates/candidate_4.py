import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    df = source.copy()
    
    # 1. Format datetime
    df['datetime'] = pd.to_datetime(df['time']).dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # 2. Define column groups for aggregation
    
    hvac_cols = [
        'electricity_heating_kwh',
        'electricity_cooling_kwh',
        'electricity_central_system_heating_kwh',
        'electricity_central_system_cooling_kwh',
        'electricity_fans_heating_kwh',
        'electricity_fans_cooling_kwh',
        'electricity_pumps_heating_kwh',
        'electricity_pumps_cooling_kwh',
        'electricity_central_system_pumps_heating_kwh',
        'electricity_central_system_pumps_cooling_kwh'
    ]
    
    domestic_water_heating_cols = [
        'electricity_water_systems_kwh'
    ]
    
    major_appliances_cols = [
        'electricity_refrigerator_kwh',
        'electricity_clothes_washer_kwh',
        'electricity_clothes_dryer_kwh',
        'electricity_cooking_range_kwh',
        'electricity_dishwasher_kwh'
    ]
    
    lighting_cols = [
        'electricity_interior_lighting_kwh',
        'electricity_exterior_lighting_kwh'
    ]
    
    miscellaneous_plug_loads_cols = [
        'electricity_plug_loads_kwh',
        'electricity_house_fan_kwh',
        'electricity_range_fan_kwh',
        'electricity_bath_fan_kwh',
        'electricity_ceiling_fan_kwh',
        'electricity_pool_heater_kwh',
        'electricity_pool_pump_kwh',
        'electricity_hot_tub_heater_kwh',
        'electricity_hot_tub_pump_kwh'
    ]
    
    # 3. Perform aggregations
    df['hvac'] = df[hvac_cols].sum(axis=1)
    df['domestic_water_heating'] = df[domestic_water_heating_cols].sum(axis=1)
    df['major_appliances'] = df[major_appliances_cols].sum(axis=1)
    df['lighting'] = df[lighting_cols].sum(axis=1)
    df['miscellaneous_plug_loads'] = df[miscellaneous_plug_loads_cols].sum(axis=1)
    
    # 4. Calculate total as sum of the categories
    df['total'] = (df['hvac'] + df['domestic_water_heating'] + df['major_appliances'] + 
                   df['lighting'] + df['miscellaneous_plug_loads'])
    
    # 5. Select target columns
    target_columns = ['datetime', 'hvac', 'domestic_water_heating', 'major_appliances', 
                      'lighting', 'miscellaneous_plug_loads', 'total']
    
    return df[target_columns]