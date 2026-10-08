"""
Weather tools for MCP Agent Hub.
Interacts with the National Weather Service (NWS) API.
Supports httpx if installed, with standard library urllib fallback.
"""
from typing import Any, Dict, List
import json
import logging
import urllib.request
import urllib.error
import asyncio

logger = logging.getLogger(__name__)

NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "mcp-agent-hub/1.0 (contact@rapoleramsai4.dev)"

def _fetch_url_sync(url: str) -> Dict[str, Any] | None:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/geo+json"
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read().decode("utf-8")
            return json.loads(data)
    except Exception as e:
        logger.warning(f"Error fetching {url}: {e}")
        return None

async def make_nws_request(url: str) -> Dict[str, Any] | None:
    # Use loop.run_in_executor to avoid blocking the event loop
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, _fetch_url_sync, url)

async def get_alerts_tool(state: str) -> str:
    """Get active severe weather alerts for a US state code (e.g. CA, NY, TX)."""
    state_code = state.strip().upper()
    url = f"{NWS_API_BASE}/alerts/active/area/{state_code}"
    data = await make_nws_request(url)

    if not data or "features" not in data:
        return f"Unable to fetch active alerts for state: {state_code}"

    features = data["features"]
    if not features:
        return f"No active severe weather alerts for {state_code}."

    alerts: List[str] = []
    for feature in features[:10]:
        props = feature.get("properties", {})
        event = props.get("event", "Unknown Event")
        headline = props.get("headline", "No headline")
        severity = props.get("severity", "Unknown")
        description = props.get("description", "No description provided.")
        alerts.append(f"[{severity.upper()}] {event}\nHeadline: {headline}\nDetails: {description[:250]}...\n")

    return "\n---\n".join(alerts)

async def get_forecast_tool(latitude: float, longitude: float) -> str:
    """Get weather forecast for latitude and longitude coordinates."""
    points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
    points_data = await make_nws_request(points_url)

    if not points_data or "properties" not in points_data:
        return f"Unable to fetch point metadata for ({latitude}, {longitude})"

    forecast_url = points_data["properties"].get("forecast")
    if not forecast_url:
        return f"Forecast URL unavailable for coordinates ({latitude}, {longitude})"

    forecast_data = await make_nws_request(forecast_url)
    if not forecast_data or "properties" not in forecast_data:
        return f"Forecast data not accessible for coordinates ({latitude}, {longitude})"

    periods = forecast_data["properties"].get("periods", [])
    if not periods:
        return "No forecast periods available."

    lines: List[str] = [f"Forecast for ({latitude}, {longitude}):"]
    for p in periods[:5]:
        name = p.get("name", "Unknown")
        temp = p.get("temperature", "N/A")
        unit = p.get("temperatureUnit", "F")
        wind = p.get("windSpeed", "N/A")
        short = p.get("shortForecast", "")
        lines.append(f"- {name}: {temp}°{unit}, Wind: {wind} | {short}")

    return "\n".join(lines)
