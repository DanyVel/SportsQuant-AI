"""
Demo script for validating SQLAlchemy metadata registration.
"""

from sportsquant.persistence.orm.base import Base

# Import ORM models so they register themselves with Base.metadata.
from sportsquant.persistence.orm import (  # noqa: F401
    GameORM,
    PlayerGameStatsORM,
    PlayerORM,
    TeamGameStatsORM,
    TeamORM,
)


def main() -> None:
    """
    Print all registered ORM tables.
    """
    print("=" * 80)
    print("REGISTERED TABLES")
    print("=" * 80)

    for table_name in sorted(Base.metadata.tables):
        print(table_name)


if __name__ == "__main__":
    main()