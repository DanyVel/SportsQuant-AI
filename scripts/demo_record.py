from sportsquant.models import Record

record = Record(
    wins=64,
    losses=18,
)

print(record)
print(record.games_played)
print(record.win_percentage)