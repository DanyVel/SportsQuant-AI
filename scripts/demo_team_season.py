from sportsquant.models import Record
from sportsquant.models import TeamSeason


team_season = TeamSeason(
    season_id="22023",
    team_id=1610612738,
    record=Record(
        wins=64,
        losses=18,
    ),
)

print(team_season)