import pytest

from clients.nba_client import NBAClient, NBAResponse


@pytest.mark.parametrize("method,args,path", [
    ("get_live_scoreboard", (), "scoreboard/todaysScoreboard_00"),
    ("get_live_boxscore", ("0022500001",), "boxscore/boxscore_0022500001"),
    ("get_live_play_by_play", ("0022500001",), "playbyplay/playbyplay_0022500001"),
])
def test_cdn_host_and_json_contract(httpx_mock, method, args, path):
    httpx_mock.add_response(url=f"https://cdn.nba.com/static/json/liveData/{path}.json", json={"game": {"actions": []}})
    with NBAClient("https://stats.nba.com/stats", "", "", "", "", "test") as client:
        assert getattr(client, method)(*args).data == {"game": {"actions": []}}
    assert httpx_mock.get_requests()[0].headers["host"] == "cdn.nba.com"

def test_invalid_stats_shape_rejected():
    response = NBAResponse(data={"resultSets": [{"headers": ["ID", "NAME"], "rowSet": [[1]]}]}, status_code=200)
    with pytest.raises(ValueError):
        response.result_set()
