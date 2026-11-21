import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    df = source.copy()
    
    # 1. Process datetime
    # Source 'time' is like '2012-07-02 00:15:00.000'
    # Target 'datetime' is like '2012-07-02 00:15:00'
    dt_series = pd.to_datetime(df['time'])
    df['datetime'] = dt_series.dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # 2. Define column groups for aggregation
    
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
    
    water_heating_cols = [
        'electricity_water_systems_kwh'
    ]
    
    major_appliance_cols = [
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
    
    misc_plug_cols = [
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
    
    # 3. Compute aggregated columns
    df['hvac'] = df[hvac_cols].sum(axis=1)
    df['domestic_water_heating'] = df[water_heating_cols].sum(axis=1)
    df['major_appliances'] = df[major_appliance_cols].sum(axis=1)
    df['lighting'] = df[lighting_cols].sum(axis=1)
    df['miscellaneous_plug_loads'] = df[misc_plug_cols].sum(axis=1)
    
    # 4. Map total
    df['total'] = df['net_site_electricity_kwh']
    
    # 5. Select and order target columns
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