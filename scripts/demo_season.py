from datetime import date

from sportsquant.models import Season


season = Season(
    season_id="22023",
    season_name="2023-24",
    start_date=date(2023, 10, 24),
    end_date=date(2024, 4, 14),
)

print(season)