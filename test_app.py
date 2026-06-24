
import json
import sys
import pytest

# Make sure the app module is importable from this directory
sys.path.insert(0, ".")
from app import app


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def client():
    """Return a Flask test client for the Dash server."""
    app.server.config["TESTING"] = True
    with app.server.test_client() as c:
        yield c


@pytest.fixture(scope="module")
def layout(client):
    """Fetch and parse the Dash layout JSON once for all tests."""
    response = client.get("/_dash-layout")
    assert response.status_code == 200, (
        f"/_dash-layout returned HTTP {response.status_code}"
    )
    return json.loads(response.data)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def find_components(node, type_name: str, results: list | None = None) -> list:
    """
    Recursively walk the Dash layout tree and collect every component
    whose ``type`` field matches *type_name* (e.g. ``"H1"``, ``"Graph"``).
    """
    if results is None:
        results = []

    if isinstance(node, dict):
        if node.get("type") == type_name:
            results.append(node)
        for child in node.get("props", {}).get("children", []) or []:
            find_components(child, type_name, results)

    elif isinstance(node, list):
        for item in node:
            find_components(item, type_name, results)

    return results


def find_by_id(node, component_id: str) -> dict | None:
    """
    Recursively search for the first component whose ``id`` prop
    matches *component_id*.
    """
    if isinstance(node, dict):
        if node.get("props", {}).get("id") == component_id:
            return node
        for child in node.get("props", {}).get("children", []) or []:
            result = find_by_id(child, component_id)
            if result is not None:
                return result

    elif isinstance(node, list):
        for item in node:
            result = find_by_id(item, component_id)
            if result is not None:
                return result

    return None


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestDashboardLayout:
    """Verify that the three key UI elements are present in the layout."""

    def test_header_is_present(self, layout):
        """
        The page must contain an <h1> element whose text includes the
        product name 'Soul Foods'.
        """
        h1_elements = find_components(layout, "H1")
        assert h1_elements, "No H1 component found in the layout."

        header_text = " ".join(
            el.get("props", {}).get("children", "") or ""
            for el in h1_elements
        )
        assert "Soul Foods" in header_text, (
            f"Expected 'Soul Foods' in H1 text, got: {header_text!r}"
        )

    def test_visualisation_is_present(self, layout):
        """
        The layout must contain a dcc.Graph component with
        id='sales-chart'.
        """
        graph = find_by_id(layout, "sales-chart")
        assert graph is not None, (
            "No component with id='sales-chart' found in the layout."
        )
        assert graph.get("type") == "Graph", (
            f"Component with id='sales-chart' has unexpected type: "
            f"{graph.get('type')!r}"
        )

    def test_region_picker_is_present(self, layout):
        """
        The layout must contain a dcc.RadioItems component with
        id='region-filter' and options for all four regions plus 'all'.
        """
        radio = find_by_id(layout, "region-filter")
        assert radio is not None, (
            "No component with id='region-filter' found in the layout."
        )
        assert radio.get("type") == "RadioItems", (
            f"Component with id='region-filter' has unexpected type: "
            f"{radio.get('type')!r}"
        )

        option_values = {
            opt["value"]
            for opt in radio.get("props", {}).get("options", [])
        }
        expected = {"all", "north", "east", "south", "west"}
        assert expected == option_values, (
            f"Region picker options mismatch.\n"
            f"  Expected: {expected}\n"
            f"  Got:      {option_values}"
        )
