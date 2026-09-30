from unittest.mock import MagicMock, patch

import pytest
from rest_framework.test import APIClient


@pytest.mark.parametrize("path,method", [('scoreboard/', 'get_live_scoreboard'), ('games/0022500001/boxscore/', 'get_live_boxscore'), ('games/0022500001/plays/', 'get_live_play_by_play')])
def test_live_routes(path, method):
    with patch("apps.core.upstream.NBAClient") as factory:
        client = factory.return_value
        client.__enter__.return_value = client
        getattr(client, method).return_value = MagicMock(data={"fixture": True})
        response = APIClient().get("/api/v1/live/" + path)
        assert response.status_code == 200
        assert response.json() == {"fixture": True}
        getattr(client, method).assert_called_once()
