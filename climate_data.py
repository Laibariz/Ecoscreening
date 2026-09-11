"""
Data-source integration layer for EcoScreen Pakistan.

This module is the single place that talks to external, verified climate
and environmental data services. Every function returns a
(dataframe_or_None, provenance_dict, error_message_or_None) tuple so the UI
can always show *where a number came from* and clearly label illustrative
fallback data as illustrative.

Live today
----------
- World Bank Climate Change Knowledge Portal (CCKP): public REST API,
  no API key required. Used for historical + CMIP6-projected temperature
  and precipitation. See https://climateknowledgeportal.worldbank.org/download-data

Documented but NOT wired up live (require credentials / heavy geospatial
tooling that a Streamlit Cloud deployment does not have by default)
-------------------------------------------------------------------
- PMD (Pakistan Meteorological Department): no open public API; station
  data requires a formal data request to PMD.
- ERA5 (Copernicus Climate Data Store): requires a free CDS API key
  (`cdsapi` package + `~/.cdsapirc` credentials file) and returns large
  NetCDF/GRIB files that need `xarray`/`cfgrib` to read.
- CHIRPS (rainfall): public, but distributed as GeoTIFF/NetCDF grids via
  UCSB/CHC or IRI Data Library; needs `rasterio`/`xarray` and a
  point/polygon extraction step.
- CMIP6 raw ensembles: distributed via ESGF nodes; large NetCDF files,
  needs `xarray` + an ESGF account for some nodes. CCKP (above) already
  ships CMIP6-derived, bias-corrected statistics without that overhead.

For each of these, `NotImplementedError` is raised with the setup steps
needed, so a team with the right access/credentials can implement the
fetch function without having to redesign the app around it.
"""

from __future__ import annotations

import datetime as _dt
from dataclasses import dataclass

import pandas as pd

try:
    import requests
    _HAS_REQUESTS = True
except ImportError:  # pragma: no cover
    _HAS_REQUESTS = False

CCKP_BASE_URL = "https://cckpapi.worldbank.org/cckp/v1"
CCKP_TIMEOUT_SECONDS = 8

# Approximate provincial/territorial centroids (degrees), for the
# geospatial context map. Coarse, project-siting-level precision only —
# replace with the actual project coordinates for real use.
PROVINCE_CENTROIDS = {
    "Punjab": (31.15, 72.70),
    "Sindh": (25.90, 68.90),
    "Khyber Pakhtunkhwa": (34.60, 72.20),
    "Balochistan": (28.49, 65.10),
    "Islamabad Capital Territory": (33.68, 73.05),
    "Gilgit-Baltistan": (35.80, 74.90),
    "Azad Jammu & Kashmir": (33.97, 73.77),
}

MOUNTAIN_SYSTEM_MARKERS = {
    "Himalayas": (34.5, 76.0),
    "Karakoram": (35.9, 76.4),
    "Hindu Kush": (36.2, 71.8),
    "Sulaiman / Koh-e-Suleman": (30.0, 69.8),
    "Spīn Ghar / Safed Koh": (34.0, 70.9),
    "Kirthar": (26.8, 67.2),
    "Salt Range": (32.6, 72.4),
}


def _provenance(**kwargs) -> dict:
    base = {"retrieved_at_utc": _dt.datetime.utcnow().isoformat(timespec="seconds") + "Z"}
    base.update(kwargs)
    return base


def fetch_cckp_annual_climatology(variable: str = "tas", scenario: str = "historical",
                                   geocode: str = "PAK"):
    """Fetch a spatially-aggregated annual climatology for Pakistan from the
    World Bank CCKP public API (no key required).

    variable: "tas" (mean temperature, °C) or "pr" (precipitation, mm/day).
    scenario: "historical" or a CMIP6 SSP code, e.g. "ssp245", "ssp585".

    Returns (dataframe_or_None, provenance, error_message_or_None).
    The dataframe has columns: Period, Value, Percentile_10, Percentile_90
    (percentiles are only populated when the API returns an ensemble range).
    """
    provenance = _provenance(
        source="World Bank Climate Change Knowledge Portal (CCKP)",
        collection="cmip6-x0.25 (downscaled CMIP6, 0.25°)" if scenario != "historical" else "cru (0.5°, 1901–2022 observed)",
        variable=variable,
        scenario=scenario,
        geocode=geocode,
        spatial_resolution="0.25° (~25 km) gridded, aggregated to country level",
        license="Public — World Bank Access to Information Classification Policy",
        citation="The World Bank Group, Climate Change Knowledge Portal, "
                 "https://climateknowledgeportal.worldbank.org",
        api_docs="https://climateknowledgeportal.worldbank.org/download-data",
    )

    if not _HAS_REQUESTS:
        return None, provenance, "The 'requests' package is not installed in this environment."

    period = "1995-2014" if scenario == "historical" else "2040-2059"
    facet = (
        f"cmip6-x0.25_climatology_{variable}_climatology_annual_{period}_median_"
        f"{scenario}_ensemble_all_mean"
    )
    url = f"{CCKP_BASE_URL}/{facet}/{geocode}?_format=json"
    provenance["url"] = url
    provenance["temporal_coverage"] = period

    try:
        resp = requests.get(url, timeout=CCKP_TIMEOUT_SECONDS)
        resp.raise_for_status()
        payload = resp.json()
    except Exception as exc:  # network unavailable, blocked, rate-limited, etc.
        return None, provenance, f"CCKP request failed ({type(exc).__name__}): {exc}"

    try:
        # The CCKP API nests results by facet -> geocode -> value. Shapes
        # vary slightly by endpoint/version, so parse defensively rather
        # than assuming one fixed structure.
        record = None
        if isinstance(payload, dict):
            inner = payload.get(facet, payload)
            if isinstance(inner, dict):
                record = inner.get(geocode, inner)
        if record is None:
            raise ValueError("Unexpected CCKP response shape.")
        value = record.get("value", record) if isinstance(record, dict) else record
        row = {"Period": period, "Value": float(value) if not isinstance(value, dict) else None}
        if isinstance(value, dict):
            row["Value"] = float(value.get("median", value.get("mean")))
            row["Percentile_10"] = value.get("p10")
            row["Percentile_90"] = value.get("p90")
        df = pd.DataFrame([row])
        return df, provenance, None
    except Exception as exc:
        return None, provenance, f"Could not parse CCKP response ({type(exc).__name__}): {exc}"


def fetch_era5(*_args, **_kwargs):
    raise NotImplementedError(
        "ERA5 requires a free Copernicus Climate Data Store (CDS) API key and the "
        "`cdsapi` + `xarray`/`cfgrib` packages to download and read NetCDF/GRIB grids. "
        "Register at https://cds.climate.copernicus.eu, save credentials to ~/.cdsapirc, "
        "then request the 'reanalysis-era5-single-levels' dataset for the project's "
        "coordinates and time range."
    )


def fetch_chirps(*_args, **_kwargs):
    raise NotImplementedError(
        "CHIRPS rainfall grids are distributed as GeoTIFF/NetCDF via UCSB/CHC "
        "(https://www.chc.ucsb.edu/data/chirps) or the IRI Data Library. Reading them "
        "needs `rasterio` or `xarray` plus a point/polygon extraction step for the "
        "project's coordinates."
    )


def fetch_cmip6_raw_ensemble(*_args, **_kwargs):
    raise NotImplementedError(
        "Raw CMIP6 model output is distributed via ESGF nodes as large NetCDF files and "
        "needs `xarray` (some nodes also require a free ESGF account). CCKP (used above) "
        "already serves bias-corrected, spatially aggregated CMIP6 statistics without this "
        "overhead — prefer it unless you specifically need individual model runs."
    )


def fetch_pmd(*_args, **_kwargs):
    raise NotImplementedError(
        "The Pakistan Meteorological Department does not publish a public API. Station "
        "and forecast data require a formal data-sharing request to PMD "
        "(https://www.pmd.gov.pk)."
    )


@dataclass
class EmissionFactorMethodology:
    """Documents the methodology behind the illustrative default emission
    factors shown in the GHG & Carbon tab, and holds whatever the user
    supplies to replace them with verified, cited figures."""

    framework: str = "IPCC 2006 Guidelines for National GHG Inventories, Vol. 2 (Energy); GHG Protocol Corporate Standard (Scope 1 & 2)"
    default_factor_note: str = (
        "The pre-filled electricity/fuel/travel emission factors in this app are generic "
        "illustrative placeholders, not Pakistan-specific verified figures. Grid emission "
        "factors vary by year and fuel mix — source a current figure from NEPRA's State of "
        "Industry Report, Pakistan's UNFCCC National Communications / Biennial Update "
        "Reports, or the IEA Emission Factors database, and record it below with its "
        "citation and as-of date."
    )
    user_source_citation: str = ""
    user_source_as_of_date: str = ""


SECTOR_INDICATOR_CATALOG_NOTE = (
    "Populate this table with indicators you have sourced and can cite (e.g. INFORM Risk "
    "Index, ND-GAIN Country Index, WRI Aqueduct Water Risk, national disaster-risk "
    "assessments). Values are not fetched automatically — enter the figure, its source, and "
    "the date it was published so the record stays auditable."
)
