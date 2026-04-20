"""Tests for the GET / redirect endpoint."""


class TestRedirect:
    """Test suite for root path redirect."""

    def test_root_redirects_to_static_index(self, client):
        """
        Test that GET / redirects to /static/index.html.
        
        AAA Pattern:
        - ARRANGE: Use test client
        - ACT: Send GET request to root path
        - ASSERT: Verify redirect response and location
        """
        # ARRANGE: Test client is set up

        # ACT: Request root path with follow_redirects=False to see the redirect
        response = client.get("/", follow_redirects=False)

        # ASSERT: Verify redirect response
        assert response.status_code in [301, 302, 303, 307, 308]
        assert "/static/index.html" in response.headers.get("location", "")

    def test_root_redirect_location_header(self, client):
        """
        Test that redirect location header is properly set.
        
        AAA Pattern:
        - ARRANGE: Use test client
        - ACT: Get root path without following redirects
        - ASSERT: Verify location header contains static/index.html
        """
        # ARRANGE: Test client is set up

        # ACT: Request root path
        response = client.get("/", follow_redirects=False)

        # ASSERT: Verify location header
        location = response.headers.get("location")
        assert location is not None
        assert "static/index.html" in location or "index.html" in location

    def test_root_redirect_following_redirects(self, client):
        """
        Test that following the redirect leads to index.html.
        
        AAA Pattern:
        - ARRANGE: Use test client
        - ACT: Send GET request with follow_redirects=True
        - ASSERT: Verify final response is successful HTML
        """
        # ARRANGE: Test client is set up

        # ACT: Request root path following redirects
        response = client.get("/", follow_redirects=True)

        # ASSERT: Verify we get the HTML
        assert response.status_code == 200
        assert "Mergington High School" in response.text or "Activities" in response.text
