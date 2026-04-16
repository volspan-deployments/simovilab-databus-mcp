from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.responses import JSONResponse
import uvicorn
import threading
from fastmcp import FastMCP
import httpx
import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

mcp = FastMCP("Databús")

BASE_URL = "http://localhost:8000/api"
API_TOKEN = os.environ.get("API_TOKEN", "")


def get_headers() -> dict:
    return {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


@mcp.tool()
async def list_routes(
    agency_id: Optional[str] = None,
    route_type: Optional[int] = None,
    limit: int = 100,
    offset: int = 0,
) -> dict:
    """Retrieve a list of all transit routes available in the system. Use this when the user wants to explore available bus/transit lines, filter routes by agency, or get an overview of the transit network."""
    params = {"limit": limit, "offset": offset}
    if agency_id is not None:
        params["agency_id"] = agency_id
    if route_type is not None:
        params["route_type"] = route_type

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/routes/",
            headers=get_headers(),
            params=params,
            timeout=30.0,
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_route(route_id: str) -> dict:
    """Retrieve detailed information about a specific transit route by its ID, including route name, type, color, and associated agency. Use when the user asks about a specific route."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/routes/{route_id}/",
            headers=get_headers(),
            timeout=30.0,
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def list_stops(
    agency_id: Optional[str] = None,
    route_id: Optional[str] = None,
    latitude: Optional[str] = None,
    longitude: Optional[str] = None,
    radius_meters: int = 500,
    limit: int = 100,
    offset: int = 0,
) -> dict:
    """Retrieve a list of transit stops, optionally filtered by location (geospatial radius), route, or agency. Use when the user wants to find stops near a location or explore all stops in the network."""
    params = {"limit": limit, "offset": offset}
    if agency_id is not None:
        params["agency_id"] = agency_id
    if route_id is not None:
        params["route_id"] = route_id
    if latitude is not None:
        params["latitude"] = latitude
    if longitude is not None:
        params["longitude"] = longitude
    if latitude is not None and longitude is not None:
        params["radius_meters"] = radius_meters

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/stops/",
            headers=get_headers(),
            params=params,
            timeout=30.0,
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_stop(stop_id: str) -> dict:
    """Retrieve detailed information about a specific transit stop by its ID, including name, location coordinates, and associated routes. Use when the user asks about a specific stop."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/stops/{stop_id}/",
            headers=get_headers(),
            timeout=30.0,
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def list_trips(
    route_id: Optional[str] = None,
    service_id: Optional[str] = None,
    agency_id: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
) -> dict:
    """Retrieve trips (scheduled service runs) for a route or service day. Use this when the user wants to know the schedule, trip times, or service patterns for a particular route or agency."""
    params = {"limit": limit, "offset": offset}
    if route_id is not None:
        params["route_id"] = route_id
    if service_id is not None:
        params["service_id"] = service_id
    if agency_id is not None:
        params["agency_id"] = agency_id

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/trips/",
            headers=get_headers(),
            params=params,
            timeout=30.0,
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_realtime_vehicle_positions(
    route_id: Optional[str] = None,
    agency_id: Optional[str] = None,
    trip_id: Optional[str] = None,
    vehicle_id: Optional[str] = None,
) -> dict:
    """Retrieve live vehicle positions for the transit network using GTFS Realtime data. Use this when the user asks where vehicles are right now, wants to track a specific vehicle, or needs real-time location data."""
    params = {}
    if route_id is not None:
        params["route_id"] = route_id
    if agency_id is not None:
        params["agency_id"] = agency_id
    if trip_id is not None:
        params["trip_id"] = trip_id
    if vehicle_id is not None:
        params["vehicle_id"] = vehicle_id

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/realtime/vehicle-positions/",
            headers=get_headers(),
            params=params,
            timeout=30.0,
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_service_alerts(
    agency_id: Optional[str] = None,
    route_id: Optional[str] = None,
    stop_id: Optional[str] = None,
    active_only: bool = True,
) -> dict:
    """Retrieve active GTFS Realtime service alerts such as disruptions, delays, detours, or cancellations. Use this when the user asks about current service disruptions, incidents, or any active notices affecting transit service."""
    params = {"active_only": active_only}
    if agency_id is not None:
        params["agency_id"] = agency_id
    if route_id is not None:
        params["route_id"] = route_id
    if stop_id is not None:
        params["stop_id"] = stop_id

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/realtime/alerts/",
            headers=get_headers(),
            params=params,
            timeout=30.0,
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_trip_updates(
    stop_id: Optional[str] = None,
    trip_id: Optional[str] = None,
    route_id: Optional[str] = None,
    agency_id: Optional[str] = None,
) -> dict:
    """Retrieve GTFS Realtime trip updates including real-time arrival and departure predictions, delays, and schedule deviations for stops. Use this when the user wants to know the next arrivals at a stop or whether a specific trip is running on time."""
    params = {}
    if stop_id is not None:
        params["stop_id"] = stop_id
    if trip_id is not None:
        params["trip_id"] = trip_id
    if route_id is not None:
        params["route_id"] = route_id
    if agency_id is not None:
        params["agency_id"] = agency_id

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/realtime/trip-updates/",
            headers=get_headers(),
            params=params,
            timeout=30.0,
        )
        response.raise_for_status()
        return response.json()




_SERVER_SLUG = "simovilab-databus"

def _track(tool_name: str, ua: str = ""):
    try:
        import urllib.request, json as _json
        data = _json.dumps({"slug": _SERVER_SLUG, "event": "tool_call", "tool": tool_name, "user_agent": ua}).encode()
        req = urllib.request.Request("https://www.volspan.dev/api/analytics/event", data=data, headers={"Content-Type": "application/json"})
        urllib.request.urlopen(req, timeout=1)
    except Exception:
        pass

async def health(request):
    return JSONResponse({"status": "ok", "server": mcp.name})

async def tools(request):
    registered = await mcp.list_tools()
    tool_list = [{"name": t.name, "description": t.description or ""} for t in registered]
    return JSONResponse({"tools": tool_list, "count": len(tool_list)})

sse_app = mcp.http_app(transport="sse")

app = Starlette(
    routes=[
        Route("/health", health),
        Route("/tools", tools),
        Mount("/", sse_app),
    ],
    lifespan=sse_app.lifespan,
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
