"""
Target Generation for the first predictive problem (win/loss).

Produces the Prediction Target for an observation by applying the
frozen win/loss rule defined in docs/design/target-generation.md and
docs/specifications/target-generation.md.

This module intentionally uses a minimal, provisional representation
for the Prediction Target (a plain `int`), as authorized by the Tech
Lead for this initial implementation. This does not resolve Open
Question 1 (concrete PredictionTarget representation), which remains
open.
"""

from __future__ import annotations


class UndeterminableTargetError(ValueError):
    """Raised when a Prediction Target cannot be determined because
    the information required to apply the frozen rule is missing.

    This is a minimal, local signaling mechanism used only to avoid
    silently returning an invalid placeholder (such as `None`, `0`, or
    `-1`) when required input is absent. Raising this exception is a
    technical necessity to keep this unit safe; it does not resolve
    Open Question 5 (behavior for undeterminable targets), which
    remains open. Any policy about exclusion, propagation, or
    downstream handling of this case belongs to a later, still
    undecided integration.
    """


def generate_win_loss_target(
    team_points: int | None,
    opponent_points: int | None,
) -> int:
    """Generate the Prediction Target for the first predictive problem.

    Applies the frozen rule: 1 if the represented team's points are
    greater than the opponent's points, 0 if they are lower.

    A tie (`team_points == opponent_points`) is outside the scope
    defined by the frozen specification: the source documents do not
    contemplate it, and no third outcome is introduced here. This
    function does not decide what a tie means; it only refuses to
    silently return an unspecified value for a case the frozen rule
    does not cover.

    Args:
        team_points: Points scored by the team represented by the
            observation, at the end of the game. `None` indicates the
            information is not available.
        opponent_points: Points scored by the opponent, at the end of
            the game. `None` indicates the information is not
            available.

    Returns:
        1 if `team_points > opponent_points`, 0 if
        `team_points < opponent_points`.

    Raises:
        UndeterminableTargetError: If either value is missing.
        NotImplementedError: If `team_points == opponent_points`. This
            case is out of scope for the frozen win/loss rule, which
            defines only two outcomes; no behavior for it has been
            specified.
    """
    if team_points is None or opponent_points is None:
        raise UndeterminableTargetError(
            "Cannot generate a Prediction Target: team_points and "
            "opponent_points must both be provided."
        )

    if team_points > opponent_points:
        return 1

    if team_points < opponent_points:
        return 0

    raise NotImplementedError(
        "team_points and opponent_points are equal. A tie is out of "
        "scope for the frozen win/loss rule and no behavior for it "
        "has been specified."
    )