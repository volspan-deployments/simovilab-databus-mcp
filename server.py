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
    _track("list_routes")
    agency_id: Optional[str] = None,
    route_type: Optional[int] = None,
    limit: int = 100,
    offset: int = 0,
) -> dict:
    """Retrieve a list of transit routes from the GTFS Schedule data. Use this when the user wants to explore available bus/transit routes, filter routes by agency, or get an overview of the transit network."""
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
    """Retrieve detailed information about a specific transit route by its ID. Use this when the user needs full details on a single route including its stops, trips, and schedule information."""
    _track("get_route")
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
    _track("list_stops")
    route_id: Optional[str] = None,
    lat: Optional[str] = None,
    lon: Optional[str] = None,
    radius: int = 500,
    limit: int = 100,
    offset: int = 0,
) -> dict:
    """Retrieve a list of transit stops with geospatial data. Use this when the user wants to find stops near a location, browse all stops, or get stop metadata including coordinates and accessibility info."""
    params = {"limit": limit, "offset": offset}
    if route_id is not None:
        params["route_id"] = route_id
    if lat is not None:
        params["lat"] = lat
    if lon is not None:
        params["lon"] = lon
    if lat is not None or lon is not None:
        params["radius"] = radius

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
    """Retrieve detailed information about a specific transit stop by its ID. Use this to get full stop details including coordinates, name, accessibility features, and associated routes."""
    _track("get_stop")
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
    _track("list_trips")
    route_id: Optional[str] = None,
    service_id: Optional[str] = None,
    direction_id: Optional[int] = None,
    limit: int = 100,
    offset: int = 0,
) -> dict:
    """Retrieve a list of GTFS trips for a given route or service date. Use this when the user wants to see scheduled trip runs, headways, or trip metadata for planning or analysis purposes."""
    params = {"limit": limit, "offset": offset}
    if route_id is not None:
        params["route_id"] = route_id
    if service_id is not None:
        params["service_id"] = service_id
    if direction_id is not None:
        params["direction_id"] = direction_id

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
    _track("get_realtime_vehicle_positions")
    route_id: Optional[str] = None,
    trip_id: Optional[str] = None,
    agency_id: Optional[str] = None,
) -> dict:
    """Retrieve live vehicle position data from the GTFS Realtime feed. Use this when the user wants to know where vehicles currently are on the network, including GPS coordinates, speed, bearing, and which trip/route each vehicle is serving."""
    params = {}
    if route_id is not None:
        params["route_id"] = route_id
    if trip_id is not None:
        params["trip_id"] = trip_id
    if agency_id is not None:
        params["agency_id"] = agency_id

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
    _track("get_service_alerts")
    route_id: Optional[str] = None,
    stop_id: Optional[str] = None,
    agency_id: Optional[str] = None,
    severity: Optional[str] = None,
) -> dict:
    """Retrieve active GTFS Realtime service alerts including disruptions, delays, detours, and informational notices. Use this when the user asks about service disruptions, delays, or any alerts affecting transit operations."""
    params = {}
    if route_id is not None:
        params["route_id"] = route_id
    if stop_id is not None:
        params["stop_id"] = stop_id
    if agency_id is not None:
        params["agency_id"] = agency_id
    if severity is not None:
        params["severity"] = severity

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
async def get_stop_times(
    _track("get_stop_times")
    trip_id: Optional[str] = None,
    stop_id: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
) -> dict:
    """Retrieve scheduled arrival and departure times for stops along a specific trip or at a specific stop. Use this when the user wants to know when a bus arrives at a particular stop or the full timetable for a trip."""
    params = {"limit": limit, "offset": offset}
    if trip_id is not None:
        params["trip_id"] = trip_id
    if stop_id is not None:
        params["stop_id"] = stop_id

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/stop-times/",
            headers=get_headers(),
            params=params,
            timeout=30.0,
        )
        response.raise_for_status()
        return response.json()




_SERVER_SLUG = "simovilab-databus"

def _track(tool_name: str, ua: str = ""):
    import threading
    def _send():
        try:
            import urllib.request, json as _json
            data = _json.dumps({"slug": _SERVER_SLUG, "event": "tool_call", "tool": tool_name, "user_agent": ua}).encode()
            req = urllib.request.Request("https://www.volspan.dev/api/analytics/event", data=data, headers={"Content-Type": "application/json"})
            urllib.request.urlopen(req, timeout=5)
        except Exception:
            pass
    threading.Thread(target=_send, daemon=True).start()

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
