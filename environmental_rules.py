"""
rules.py

Environmental and climate-risk configuration rules for EcoScreen Pakistan.
Defines administrative, geographic, sector-based categorization schemas,
resilience priority mappings, and screening regulatory disclaimers.
"""

from typing import Dict, List, Optional, Set, Tuple

# =====================================================================
# CATEGORY SCHEMAS & CONSTANTS
# =====================================================================

SECTORS: Tuple[str, ...] = (
    "Agriculture",
    "Energy",
    "Health",
    "Transportation",
    "Water",
    "Urban Development",
    "Industry",
    "Buildings",
    "Other",
)

HAZARDS: Tuple[str, ...] = (
    "Flood",
    "Extreme heat",
    "Drought",
    "Extreme precipitation",
    "Landslide",
    "Wildfire",
    "Storm",
    "Sea-level rise",
)

RISK_BANDS: Tuple[str, ...] = ("Low", "Moderate", "High", "Critical")

PAKISTAN_REGIONS: Tuple[str, ...] = (
    "Punjab",
    "Sindh",
    "Khyber Pakhtunkhwa",
    "Balochistan",
    "Islamabad Capital Territory",
    "Gilgit-Baltistan",
    "Azad Jammu & Kashmir",
)

MOUNTAIN_SYSTEMS: Tuple[str, ...] = (
    "Himalayas",
    "Karakoram",
    "Hindu Kush",
    "Sulaiman / Koh-e-Suleman",
    "Spīn Ghar / Safed Koh",
    "Kirthar",
    "Salt Range",
)

RESILIENCE_PRIORITIES: Tuple[str, ...] = (
    "drainage and flood protection",
    "heat resilience",
    "water availability",
    "slope stability",
    "asset protection",
    "emergency preparedness",
    "operational continuity",
    "climate-adaptive design",
)


# =====================================================================
# GEOGRAPHIC & REGIONAL RESILIENCE PRIORITIES
# =====================================================================

REGION_PRIORITIES: Dict[str, List[str]] = {
    "Punjab": [
        "drainage and flood protection",
        "heat resilience",
        "water availability",
        "asset protection",
        "emergency preparedness",
        "operational continuity",
        "climate-adaptive design",
    ],
    "Sindh": [
        "drainage and flood protection",
        "heat resilience",
        "water availability",
        "asset protection",
        "emergency preparedness",
        "operational continuity",
        "climate-adaptive design",
    ],
    "Khyber Pakhtunkhwa": [
        "drainage and flood protection",
        "slope stability",
        "heat resilience",
        "water availability",
        "asset protection",
        "emergency preparedness",
        "operational continuity",
        "climate-adaptive design",
    ],
    "Balochistan": [
        "water availability",
        "heat resilience",
        "drought resilience",
        "drainage and flood protection",
        "asset protection",
        "emergency preparedness",
        "operational continuity",
        "climate-adaptive design",
    ],
    "Islamabad Capital Territory": [
        "drainage and flood protection",
        "slope stability",
        "heat resilience",
        "asset protection",
        "emergency preparedness",
        "operational continuity",
        "climate-adaptive design",
    ],
    "Gilgit-Baltistan": [
        "slope stability",
        "flood and GLOF risk screening",
        "water availability",
        "asset protection",
        "emergency preparedness",
        "operational continuity",
        "climate-adaptive design",
    ],
    "Azad Jammu & Kashmir": [
        "slope stability",
        "drainage and flood protection",
        "landslide screening",
        "water availability",
        "asset protection",
        "emergency preparedness",
        "operational continuity",
        "climate-adaptive design",
    ],
}

MOUNTAIN_PRIORITIES: Dict[str, List[str]] = {
    "Himalayas": [
        "slope stability",
        "landslide screening",
        "drainage and flood protection",
        "water availability",
        "asset protection",
        "emergency preparedness",
        "operational continuity",
    ],
    "Karakoram": [
        "slope stability",
        "flood and GLOF risk screening",
        "water availability",
        "asset protection",
        "emergency preparedness",
        "operational continuity",
    ],
    "Hindu Kush": [
        "slope stability",
        "landslide screening",
        "flood and GLOF risk screening",
        "water availability",
        "asset protection",
        "emergency preparedness",
    ],
    "Sulaiman / Koh-e-Suleman": [
        "slope stability",
        "hill-torrent and flood drainage",
        "water availability",
        "asset protection",
        "emergency preparedness",
        "operational continuity",
    ],
    "Spīn Ghar / Safed Koh": [
        "slope stability",
        "landslide screening",
        "drainage and flood protection",
        "water availability",
        "asset protection",
        "emergency preparedness",
    ],
    "Kirthar": [
        "water availability",
        "drought resilience",
        "flash-flood drainage",
        "slope stability",
        "asset protection",
        "emergency preparedness",
    ],
    "Salt Range": [
        "slope stability",
        "drainage and flood protection",
        "water availability",
        "asset protection",
        "emergency preparedness",
        "operational continuity",
    ],
}


# =====================================================================
# SECTOR SPECIFIC PRIORITIES (FULL COVERAGE)
# =====================================================================

SECTOR_PRIORITIES: Dict[str, List[str]] = {
    "Agriculture": [
        "drought resilience",
        "heat resilience",
        "drainage and flood protection",
        "water availability",
        "crop resilience",
    ],
    "Energy": [
        "heat resilience",
        "water availability",
        "drainage and flood protection",
        "grid resilience",
        "cooling demand management",
    ],
    "Health": [
        "heat resilience",
        "vector-borne disease control",
        "water-borne disease prevention",
        "air quality monitoring",
        "health facility emergency readiness",
    ],
    "Transportation": [
        "drainage and flood protection",
        "heat resilience",
        "slope stability",
        "asset resilience",
        "supply chain disruption management",
    ],
    "Water": [
        "drought resilience",
        "drainage and flood protection",
        "water quality protection",
        "demand management",
        "catchment resilience",
    ],
    "Urban Development": [
        "urban heat island mitigation",
        "stormwater drainage and flood protection",
        "water availability",
        "asset protection",
        "emergency preparedness",
    ],
    "Industry": [
        "water availability",
        "effluent and waste management",
        "heat resilience",
        "operational continuity",
        "energy efficiency",
    ],
    "Buildings": [
        "thermal efficiency and insulation",
        "structural stability",
        "drainage and flood protection",
        "climate-adaptive design",
        "fire risk mitigation",
    ],
    "Other": [
        "climate-adaptive design",
        "asset protection",
        "operational continuity",
        "emergency preparedness",
    ],
}


# =====================================================================
# LEGAL & REGULATORY DISCLAIMERS
# =====================================================================

SCREENING_DISCLAIMER: str = (
    "This screening is an early-stage decision-support exercise. Use the results to identify "
    "issues that may need further investigation. It does not replace an Environmental Impact "
    "Assessment (EIA), Initial Environmental Examination (IEE), engineering design, hydrological "
    "study, health assessment, disaster-risk assessment, or regulatory review."
)


# =====================================================================
# HELPER / RESOLVER FUNCTIONS
# =====================================================================

def get_region_priorities(region: str) -> List[str]:
    """Retrieve resilience priorities for a region safely with defaults."""
    return REGION_PRIORITIES.get(
        region,
        ["drainage and flood protection", "asset protection", "climate-adaptive design"],
    )


def get_mountain_priorities(mountain_system: str) -> List[str]:
    """Retrieve priorities for a mountain system safely with defaults."""
    return MOUNTAIN_PRIORITIES.get(
        mountain_system,
        ["slope stability", "drainage and flood protection", "asset protection"],
    )


def get_sector_priorities(sector: str) -> List[str]:
    """Retrieve resilience priorities for a sector safely with defaults."""
    return SECTOR_PRIORITIES.get(
        sector,
        ["climate-adaptive design", "asset protection", "operational continuity"],
    )


def get_combined_priorities(
    region: str, sector: str, mountain_system: Optional[str] = None
) -> List[str]:
    """Synthesize deduplicated priority actions across region, sector, and mountain terrain."""
    priorities: List[str] = []
    seen: Set[str] = set()

    combined_sources = get_sector_priorities(sector) + get_region_priorities(region)
    if mountain_system:
        combined_sources.extend(get_mountain_priorities(mountain_system))

    for item in combined_sources:
        if item.lower() not in seen:
            seen.add(item.lower())
            priorities.append(item)

    return priorities













