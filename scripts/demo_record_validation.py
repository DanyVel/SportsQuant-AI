from sportsquant.models import Record

try:
    Record(
        wins=-5,
        losses=82,
    )
except ValueError as ex:
    print(ex)