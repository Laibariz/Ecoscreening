# 🌍 EcoScreen Pakistan
## Pakistan Climate & Environmental Decision-Support Platform

EcoScreen Pakistan is a Streamlit prototype for early-stage climate-risk screening and climate-resilient development planning.

### Core question
> **What climate risks could affect this development, and what should we investigate next?**

### Hazards screened
- 🌊 Flooding
- 🌡️ Extreme heat
- 🌧️ Extreme precipitation
- 💧 Drought
- ⛰️ Landslides
- 🔥 Wildfire
- 🌪️ Storms
- 🌊 Sea-level rise

### Pakistan geographic coverage
Provinces/territories:
- Punjab
- Sindh
- Khyber Pakhtunkhwa
- Balochistan
- Islamabad Capital Territory
- Gilgit-Baltistan
- Azad Jammu & Kashmir

Mountain/geographic systems:
- Himalayas
- Karakoram
- Hindu Kush
- Sulaiman / Koh-e-Suleman
- Spīn Ghar / Safed Koh
- Kirthar
- Salt Range

### Climate-resilient infrastructure priorities
The screening highlights issues that may need additional attention, including:
- drainage and flood protection
- heat resilience
- water availability
- slope stability
- asset protection
- emergency preparedness
- operational continuity
- climate-adaptive design

### Features
- Climate/disaster risk scoring: Low → Moderate → High → Critical
- Illustrative temperature and precipitation simulations
- Project-level CHRI proxy
- GHG accounting
- Illustrative shadow carbon calculation
- Climate co-benefit score
- Sector in-depth screening
- Groq-powered AI screening explanation
- CSV export of project screening inputs

### Groq API key
You **must create your own Groq API key**. The developer cannot provide a private API key for your account.

The app is configured for `openai/gpt-oss-120b`, a currently supported Groq production model. See Groq's current model list before deployment.

For Streamlit Community Cloud:
1. Open your app in Streamlit Community Cloud.
2. Open **Settings / Secrets**.
3. Add:

```toml
GROQ_API_KEY = "your-real-key"
```

Do not put the key in `app.py`, `workflow.py`, GitHub, or `requirements.txt`.

### Local setup
```bash
python -m venv .venv
```

Windows:
```bash
.venv\\Scripts\\activate
```

Install:
```bash
pip install -r requirements.txt
```

Run:
```bash
streamlit run app.py
```

### Second app: Pakistan Climate Resilience Hub
This repo also includes `climate_resilience_hub.py`, a separate, standalone companion dashboard (region-based drivers, a matplotlib temperature-trend chart with a mitigation-investment slider, and a mitigation action-plan tab). It has its own `st.set_page_config` and is not a page of EcoScreen Pakistan — run it as its own app:
```bash
streamlit run climate_resilience_hub.py
```
Like the rest of this repo, its temperature trend and the "+18% monsoon variation" / "<500 m³ per capita" figures shown are illustrative placeholders for demonstrating the UI, not sourced measurements — replace them with verified data (e.g. via the same CCKP/PMD/ERA5/CHIRPS pattern described below) before using it for real decisions.

### GitHub + Streamlit Community Cloud
1. Create a GitHub repository, for example `ecoscreen-pakistan`.
2. Upload all files from this folder.
3. In Streamlit Community Cloud, create a new app.
4. Select the GitHub repository and branch.
5. Set main file to `app.py`.
6. Add `GROQ_API_KEY` in Streamlit Secrets.
7. Deploy.

### Important scope
This is an early-stage decision-support prototype. It does not replace EIA/IEE, engineering design, hydrological or geotechnical studies, health assessment, disaster-risk assessment, regulatory review, or official climate forecasts. Simulation values are illustrative unless replaced with verified datasets and documented methods.

The CHRI component is explicitly a project-level proxy and does not reproduce the official World Bank CHRI methodology.

### Architecture
```text
User
  ↓
Streamlit UI
  ↓
Project + geography inputs
  ↓
Risk scoring engine
  ↓
Regional / mountain-system resilience priorities
  ↓
GHG + CHRI proxy + co-benefits
  ↓
Groq AI explanation
  ↓
Dashboard + CSV export
```

### Future production upgrades
Replace illustrative simulations with validated CCKP, PMD, ERA5, CHIRPS, CMIP6 and/or verified national datasets as legally and technically appropriate. Add data provenance, dates, uncertainty, geospatial layers, validated sector indicators, and documented emission/carbon methodologies.

**Status of this upgrade path in the current codebase** (`climate_data.py`):
- ✅ **CCKP (World Bank)** — live, working integration (`fetch_cckp_annual_climatology`) against the public CCKP REST API (no key required). Tab 2 has a "Try live climate data" panel: click to fetch, and the app shows either 🟢 live data with full provenance (source, dataset, URL, resolution, license, retrieval timestamp) or 🟡 a clear fallback notice with the failure reason if the request fails (e.g. no outbound internet from the host, or the endpoint rate-limits/blocks the request — CCKP's `robots.txt` disallows generic bot traffic, so confirm your deployment's requests succeed).
- 📝 **PMD, ERA5, CHIRPS, CMIP6 raw ensembles** — documented stub functions (`fetch_pmd`, `fetch_era5`, `fetch_chirps`, `fetch_cmip6_raw_ensemble`) that raise a clear `NotImplementedError` listing exactly what credentials/packages each needs (PMD: formal data-sharing request; ERA5: free CDS API key + `cdsapi`/`xarray`; CHIRPS: `rasterio`/`xarray` + a GeoTIFF/NetCDF extraction step; CMIP6 raw: `xarray` + an ESGF node/account). They are intentionally not faked — wire in real credentials before using them.
- ✅ **Data provenance & dates** — every live fetch returns a provenance dict (source, dataset/collection, geocode, URL, spatial resolution, license, citation, retrieval timestamp) shown in an expander next to the data.
- ✅ **Uncertainty** — the CCKP fetch parses ensemble 10th/90th percentiles when the API returns them; the illustrative simulation is explicitly labeled 🟡 illustrative (no quantified uncertainty) rather than presented as if it were.
- ✅ **Geospatial layer** — Tab 2 now shows a province-level (and mountain-system) location map; still only a coarse centroid, not the real project site or hazard-layer overlays.
- ✅ **Validated sector indicators** — Tab 6 has an editable, citable indicator log (indicator, value, source, as-of date) instead of only illustrative sliders; exportable as CSV.
- ✅ **Documented emission/carbon methodology** — Tab 4 states the IPCC 2006 Guidelines Vol. 2 / GHG Protocol framework, flags that the pre-filled emission factors are generic placeholders, and lets you record your verified source + as-of date, which is included in the CSV export.
