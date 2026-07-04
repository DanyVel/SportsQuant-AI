from sportsquant.config.settings import (
    PROJECT_NAME,
    DEFAULT_SPORT,
    DEBUG,
)

from sportsquant.utils.paths import PROJECT_ROOT


def main() -> None:
    print("=" * 50)
    print(PROJECT_NAME)
    print("=" * 50)

    print(f"Project Root : {PROJECT_ROOT}")
    print(f"Default Sport: {DEFAULT_SPORT}")
    print(f"Debug Mode   : {DEBUG}")


if __name__ == "__main__":
    main()