"""Tests for the root endpoint (GET /)"""

import pytest


class TestRootEndpoint:
    """Tests for GET / endpoint"""

    def test_root_redirect_to_static_index(self, client):
        """Test that GET / redirects to /static/index.html"""
        response = client.get("/", follow_redirects=False)
        assert response.status_code in (301, 302, 307, 308)
        assert "/static/index.html" in response.headers["location"]

    def test_root_redirect_location_header(self, client):
        """Test that redirect Location header is correctly set"""
        response = client.get("/", follow_redirects=False)
        assert "location" in response.headers
        assert response.headers["location"] == "/static/index.html"
