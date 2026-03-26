"""Smoke tests for NBA data API endpoints."""

import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from apps.nba.models import Game, Player, Team


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def sample_team(db):
    return Team.objects.create(
        nba_id="1610612747",
        abbreviation="LAL",
        full_name="Los Angeles Lakers",
        nickname="Lakers",
        city="Los Angeles",
        conference="West",
        division="Pacific",
        is_active=True,
    )


@pytest.fixture
def sample_player(db, sample_team):
    return Player.objects.create(
        nba_id="2544",
        first_name="LeBron",
        last_name="James",
        full_name="LeBron James",
        team=sample_team,
        team_abbreviation="LAL",
        position="F",
        is_active=True,
    )


@pytest.fixture
def sample_game(db, sample_team):
    away = Team.objects.create(
        nba_id="1610612738",
        abbreviation="BOS",
        full_name="Boston Celtics",
        is_active=True,
    )
    return Game.objects.create(
        nba_id="0022401063",
        home_team=sample_team,
        away_team=away,
        home_team_abbreviation="LAL",
        away_team_abbreviation="BOS",
        home_score=110,
        away_score=105,
        game_date="2025-03-25",
        season="2024-25",
        status=Game.STATUS_FINAL,
    )


class TestTeamEndpoints:
    def test_list_teams(self, api_client, sample_team):
        response = api_client.get("/api/v1/teams/")
        assert response.status_code == 200
        data = response.json()
        assert data["count"] >= 1

    def test_retrieve_team(self, api_client, sample_team):
        response = api_client.get(f"/api/v1/teams/{sample_team.pk}/")
        assert response.status_code == 200
        assert response.json()["nba_id"] == "1610612747"

    def test_team_by_nba_id(self, api_client, sample_team):
        response = api_client.get("/api/v1/teams/nba/1610612747/")
        assert response.status_code == 200

    def test_filter_by_conference(self, api_client, sample_team):
        response = api_client.get("/api/v1/teams/?conference=West")
        assert response.status_code == 200
        assert response.json()["count"] >= 1


class TestPlayerEndpoints:
    def test_list_players(self, api_client, sample_player):
        response = api_client.get("/api/v1/players/")
        assert response.status_code == 200

    def test_retrieve_player(self, api_client, sample_player):
        response = api_client.get(f"/api/v1/players/{sample_player.pk}/")
        assert response.status_code == 200
        assert response.json()["full_name"] == "LeBron James"

    def test_player_by_nba_id(self, api_client, sample_player):
        response = api_client.get("/api/v1/players/nba/2544/")
        assert response.status_code == 200

    def test_filter_by_team(self, api_client, sample_player):
        response = api_client.get("/api/v1/players/?team=LAL")
        assert response.status_code == 200


class TestGameEndpoints:
    def test_list_games(self, api_client, sample_game):
        response = api_client.get("/api/v1/games/")
        assert response.status_code == 200

    def test_retrieve_game(self, api_client, sample_game):
        response = api_client.get(f"/api/v1/games/{sample_game.pk}/")
        assert response.status_code == 200
        assert response.json()["nba_id"] == "0022401063"

    def test_game_by_nba_id(self, api_client, sample_game):
        response = api_client.get("/api/v1/games/nba/0022401063/")
        assert response.status_code == 200

    def test_filter_by_season(self, api_client, sample_game):
        response = api_client.get("/api/v1/games/?season=2024-25")
        assert response.status_code == 200
        assert response.json()["count"] >= 1

    def test_filter_by_status(self, api_client, sample_game):
        response = api_client.get("/api/v1/games/?status=final")
        assert response.status_code == 200

    def test_game_not_found(self, api_client):
        response = api_client.get("/api/v1/games/nba/9999999999/")
        assert response.status_code == 404


class TestHealthCheck:
    def test_health_ok(self, api_client):
        response = api_client.get("/healthz")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"
