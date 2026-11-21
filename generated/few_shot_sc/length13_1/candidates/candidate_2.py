import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    df = source.copy()
    
    # 1. Parse and format datetime
    # Source 'time' is like '2012-07-02 00:15:00.000'
    # Target 'datetime' is '2012-01-01 00:15:00'
    dt = pd.to_datetime(df['time'])
    df['datetime'] = dt.dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # 2. Calculate HVAC
    # Includes heating, cooling, fans, and pumps associated with HVAC systems
    hvac_cols = [
        'electricity_heating_kwh',
        'electricity_central_system_heating_kwh',
        'electricity_cooling_kwh',
        'electricity_central_system_cooling_kwh',
        'electricity_fans_heating_kwh',
        'electricity_fans_cooling_kwh',
        'electricity_pumps_heating_kwh',
        'electricity_central_system_pumps_heating_kwh',
        'electricity_pumps_cooling_kwh',
        'electricity_central_system_pumps_cooling_kwh'
    ]
    df['hvac'] = df[hvac_cols].sum(axis=1)
    
    # 3. Calculate Domestic Water Heating
    df['domestic_water_heating'] = df['electricity_water_systems_kwh']
    
    # 4. Calculate Major Appliances
    major_appliance_cols = [
        'electricity_refrigerator_kwh',
        'electricity_clothes_washer_kwh',
        'electricity_clothes_dryer_kwh',
        'electricity_cooking_range_kwh',
        'electricity_dishwasher_kwh'
    ]
    df['major_appliances'] = df[major_appliance_cols].sum(axis=1)
    
    # 5. Calculate Lighting
    lighting_cols = [
        'electricity_interior_lighting_kwh',
        'electricity_exterior_lighting_kwh'
    ]
    df['lighting'] = df[lighting_cols].sum(axis=1)
    
    # 6. Calculate Miscellaneous Plug Loads
    # Includes plug loads, various fans, and pool/hot tub equipment
    misc_cols = [
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
    df['miscellaneous_plug_loads'] = df[misc_cols].sum(axis=1)
    
    # 7. Total
    df['total'] = df['net_site_electricity_kwh']
    
    # 8. Select and return target columns
    target_columns = [
        'datetime', 
        'hvac', 
        'domestic_water_heating', 
        'major_appliances', 
        'lighting', 
        'miscellaneous_plug_loads', 
        'total'
    ]
    
    return df[target_columns]