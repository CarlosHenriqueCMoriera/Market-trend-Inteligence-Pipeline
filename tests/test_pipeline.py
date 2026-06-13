"""Tests for the Market Trends Pipeline."""
import pytest
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class TestFetchTrends:
    """Tests for fetch_trends module."""
    
    @patch("src.ingestion.fetch_trends.psycopg2")
    def test_fetch_to_database(self, mock_psycopg2):
        """Test fetch_to_database method."""
        from src.ingestion.fetch_trends import GoogleTrendsFetcher
        
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_psycopg2.connect.return_value = mock_conn
        
        with patch.object(GoogleTrendsFetcher, "fetch", return_value={"iphone": {}}):
            fetcher = GoogleTrendsFetcher()
            fetcher.fetch_to_database(["iphone"])
            
            mock_psycopg2.connect.assert_called_once()


class TestTransform:
    """Tests for transformation module."""
    
    @patch("src.transformation.transform.psycopg2")
    def test_clean_null_values(self, mock_psycopg2):
        """Test clean_null_values function."""
        from src.transformation.transform import clean_null_values
        
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 0
        mock_conn.cursor.return_value = mock_cursor
        mock_psycopg2.connect.return_value = mock_conn
        
        result = clean_null_values()
        assert result == 0

    @patch("src.transformation.transform.psycopg2")
    def test_deduplicate(self, mock_psycopg2):
        """Test deduplicate function."""
        from src.transformation.transform import deduplicate
        
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 0
        mock_conn.cursor.return_value = mock_cursor
        mock_psycopg2.connect.return_value = mock_conn
        
        result = deduplicate()
        assert result == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
