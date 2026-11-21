import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # Create a copy to avoid modifying the original
    df = source.copy()
    
    # Parse the time column
    df['time_dt'] = pd.to_datetime(df['time'])
    
    # Extract hour
    df['hour'] = df['time_dt'].dt.hour
    
    # Determine season based on month
    # Winter: Dec(12), Jan(1), Feb(2)
    # Spring: Mar(3), Apr(4), May(5)
    # Summer: Jun(6), Jul(7), Aug(8)
    # Fall: Sep(9), Oct(10), Nov(11)
    def get_season(month):
        if month in [12, 1, 2]:
            return 'Winter'
        elif month in [3, 4, 5]:
            return 'Spring'
        elif month in [6, 7, 8]:
            return 'Summer'
        else:
            return 'Fall'
            
    df['season'] = df['time_dt'].dt.month.apply(get_season)
    
    # Define the aggregation for each target column
    
    # HVAC: Heating, Cooling, Fans (heating/cooling), Pumps (heating/cooling)
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
    
    # Domestic Water Heating: Water systems, Pool heater, Hot tub heater
    dwh_cols = [
        'electricity_water_systems_kwh',
        'electricity_pool_heater_kwh',
        'electricity_hot_tub_heater_kwh'
    ]
    df['domestic_water_heating'] = df[dwh_cols].sum(axis=1)
    
    # Major Appliances: Refrigerator, Washer, Dryer, Range, Dishwasher
    major_appl_cols = [
        'electricity_refrigerator_kwh',
        'electricity_clothes_washer_kwh',
        'electricity_clothes_dryer_kwh',
        'electricity_cooking_range_kwh',
        'electricity_dishwasher_kwh'
    ]
    df['major_appliances'] = df[major_appl_cols].sum(axis=1)
    
    # Lighting: Interior, Exterior
    lighting_cols = [
        'electricity_interior_lighting_kwh',
        'electricity_exterior_lighting_kwh'
    ]
    df['lighting'] = df[lighting_cols].sum(axis=1)
    
    # Miscellaneous Plug Loads: Plug loads, House fan, Range fan, Bath fan, Ceiling fan, Pool pump, Hot tub pump
    misc_cols = [
        'electricity_plug_loads_kwh',
        'electricity_house_fan_kwh',
        'electricity_range_fan_kwh',
        'electricity_bath_fan_kwh',
        'electricity_ceiling_fan_kwh',
        'electricity_pool_pump_kwh',
        'electricity_hot_tub_pump_kwh'
    ]
    df['miscellaneous_plug_loads'] = df[misc_cols].sum(axis=1)
    
    # Total: Net site electricity
    df['total'] = df['net_site_electricity_kwh']
    
    # Group by season and hour, and sum the values
    # Note: The source has 15-min intervals, so summing 4 intervals gives the hourly total
    agg_df = df.groupby(['season', 'hour'], as_index=False).agg({
        'hvac': 'sum',
        'domestic_water_heating': 'sum',
        'major_appliances': 'sum',
        'lighting': 'sum',
        'miscellaneous_plug_loads': 'sum',
        'total': 'sum'
    })
    
    # Define target columns
    target_columns = [
        'season', 
        'hour', 
        'hvac', 
        'domestic_water_heating', 
        'major_appliances', 
        'lighting', 
        'miscellaneous_plug_loads', 
        'total'
    ]
    
    # Ensure column order and names match exactly
    result = agg_df[target_columns]
    
    # Clean up any intermediate columns if necessary (already handled by groupby selection)
    
    return result[target_columns]