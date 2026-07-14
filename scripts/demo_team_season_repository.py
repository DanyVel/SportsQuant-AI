"""
Manual test for NBATeamSeasonRepository.
"""

from sportsquant.repositories.nba import NBATeamSeasonRepository


def main() -> None:
    repository = NBATeamSeasonRepository()

    team_season = repository.get_by_team_and_season(
        team_id=1610612738,      # Boston Celtics
        season_id="22023",
    )

    print(team_season)


if __name__ == "__main__":
    main()