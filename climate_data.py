"""
climatedata.py

Data-integration and abstraction layer for EcoScreen Pakistan.
Provides live connections to climate APIs (World Bank CCKP), geographic
and topographic metadata for Pakistan, carbon accounting protocols, and 
documented stubs for advanced environmental datasets.
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple
import pandas as pd
import requests


# =====================================================================
# GEOSPATIAL & TOPOGRAPHIC METADATA (PAKISTAN)
# =====================================================================

PROVINCE_CENTROIDS: Dict[str, Dict[str, float]] = {
    "Punjab": {"lat": 31.1704, "lon": 72.7097},
    "Sindh": {"lat": 25.8943, "lon": 68.5247},
    "Khyber Pakhtunkhwa": {"lat": 34.9526, "lon": 72.3311},
    "Balochistan": {"lat": 28.4907, "lon": 65.0958},
    "Islamabad Capital Territory": {"lat": 33.6844, "lon": 73.0479},
    "Gilgit-Baltistan": {"lat": 35.8819, "lon": 74.4643},
    "Azad Jammu & Kashmir": {"lat": 33.9259, "lon": 73.7810},
}

MOUNTAIN_SYSTEM_MARKERS: Dict[str, Dict[str, Any]] = {
    "Himalayas": {
        "lat": 34.5000,
        "lon": 74.0000,
        "description": "High hazard risk from GLOF (Glacial Lake Outburst Floods) and landsliding.",
    },
    "Karakoram": {
        "lat": 35.8819,
        "lon": 76.5133,
        "description": "Extreme terrain, glacier dynamics, and high risk of isolated extreme events.",
    },
    "Hindu Kush": {
        "lat": 36.0000,
        "lon": 71.5000,
        "description": "Seismic vulnerability combined with flash flooding hazards.",
    },
    "Salt Range & Potohar Plateau": {
        "lat": 32.6500,
        "lon": 72.7500,
        "description": "Soil erosion, intense seasonal precipitation, and flash flooding risk.",
    },
    "Sulaiman & Kirthar Ranges": {
        "lat": 29.5000,
        "lon": 67.0000,
        "description": "Arid land degradation, flash flooding (hill torrents/rod-kohi), and drought stress.",
    },
    "Indus River Basin & Delta": {
        "lat": 24.5000,
        "lon": 67.5000,
        "description": "Downstream riverine flooding, sea-level rise, coastal erosion, and salinity intrusion.",
    },
}


# =====================================================================
# CARBON ACCOUNTING METADATA
# =====================================================================

@dataclass
class EmissionFactorMethodology:
    """Ipcc 2006 / GHG Protocol methodology context for carbon auditing."""
    framework: str = "IPCC Guidelines for National Greenhouse Gas Inventories (2006)"
    electricity_grid_ef_unit: str = "tCO2e / MWh"
    fuel_ef_unit: str = "kgCO2e / Liter"
    travel_ef_unit: str = "kgCO2e / km"
    note: str = (
        "Default emission factors are illustrative averages for Pakistan. "
        "Use verified project-specific or NEPRA/national grid factors for formal reporting."
    )


# =====================================================================
# LIVE INTEGRATIONS (WORLD BANK CCKP API)
# =====================================================================

def fetch_cckp_annual_climatology(
    country_iso3: str = "PAK",
    variable: str = "tas",
    period: str = "1995-2014",
    percentile: str = "median",
) -> Tuple[Optional[pd.DataFrame], Dict[str, Any], Optional[str]]:
    """Fetch gridded/aggregated climate stats from World Bank CCKP API v1.
    
    Returns standard tuple: (DataFrame or None, Data Provenance Dict, Error Message or None)
    """
    url = f"https://cckpapi.worldbank.org/cckp/v1/cmip6-x0.25_climatology_{variable}_climatology_annual_{period}_{percentile}_historical_ensemble_all_mean/{country_iso3}?_format=json"
    
    provenance = {
        "source": "World Bank Climate Change Knowledge Portal (CCKP) API v1",
        "url": url,
        "country": country_iso3,
        "variable": variable,
        "period": period,
        "status": "Attempted",
    }

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        json_data = response.json()

        # Handle API response parsing
        if isinstance(json_data, dict) and "data" in json_data:
            df = pd.DataFrame(json_data["data"])
        elif isinstance(json_data, list):
            df = pd.DataFrame(json_data)
        else:
            df = pd.DataFrame([json_data])

        provenance["status"] = "Success"
        return df, provenance, None

    except requests.exceptions.RequestException as req_err:
        provenance["status"] = "Failed"
        error_msg = f"Network or CCKP API response error: {str(req_err)}"
        return None, provenance, error_msg
    except Exception as err:
        provenance["status"] = "Failed"
        error_msg = f"Error processing CCKP response: {str(err)}"
        return None, provenance, error_msg


# =====================================================================
# DATASET STUBS (PLANNED / ADVANCED FEEDS)
# =====================================================================

def fetch_copernicus_era5_reanalysis(
    lat: float, lon: float, start_year: int = 1990, end_year: int = 2023
) -> Tuple[Optional[pd.DataFrame], Dict[str, Any], Optional[str]]:
    """Stub for retrieving Copernicus ERA5 high-resolution reanalysis data via CDS API."""
    provenance = {
        "source": "ECMWF / Copernicus Climate Change Service (C3S) ERA5",
        "status": "Not Implemented",
        "requires": "cdsapi package and ECMWF CDS User Key",
    }
    error_msg = (
        "ERA5 direct download requires ECMWF API registration (`cdsapi`). "
        "This function is a structured stub for production expansion."
    )
    return None, provenance, error_msg


def fetch_chirps_precipitation_grid(
    bbox: Tuple[float, float, float, float], start_date: str, end_date: str
) -> Tuple[Optional[pd.DataFrame], Dict[str, Any], Optional[str]]:
    """Stub for retrieving CHIRPS high-resolution precipitation raster data."""
    provenance = {
        "source": "CHIRPS (Climate Hazards Center UC Santa Barbara)",
        "status": "Not Implemented",
        "requires": "xarray, rasterio, and direct FTP/HTTP geotiff processing",
    }
    error_msg = (
        "CHIRPS processing requires spatial raster tools (`rasterio`/`xarray`). "
        "Use local regional averages or CCKP API for web screening."
    )
    return None, provenance, error_msg


def fetch_pmd_station_data(
    station_id: str, start_year: int, end_year: int
) -> Tuple[Optional[pd.DataFrame], Dict[str, Any], Optional[str]]:
    """Stub for Pakistan Meteorological Department (PMD) station observational records."""
    provenance = {
        "source": "Pakistan Meteorological Department (PMD)",
        "status": "Manual / Restricted",
        "requires": "Formal PMD data access request & manual CSV ingestion",
    }
    error_msg = (
        "PMD observational station data is not available via an open public REST API. "
        "Load local station CSV files manually into the dashboard."
    )
    return None, provenance, error_msg
