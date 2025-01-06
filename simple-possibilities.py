"""
Computes the possibilities/probabilites of winning/losing by brute forcing all dice rolls and choices.
"""

from copy import deepcopy
from dataclasses import dataclass
import itertools
from pprint import pprint
from typing import Generator


class GameState:
    _front_row: list[bool]  # is flipped in front
    _back_row: list[bool]  # is flipped in back (MUST also be flipped in front)

    def __init__(self) -> None:
        self._front_row = [False] * 12
        self._back_row = [False] * 12

    def get_next_states(self, roll: int) -> list["GameState"]:
        result: list[GameState] = []

        def recur_helper(roll_remaining: int, state: GameState):
            if roll_remaining == 0:
                result.append(state)
                return

            vals = range(1, 13)
            for val, front_flipped, back_flipped in zip(
                vals, self._front_row, self._back_row, strict=True
            ):
                if front_flipped and back_flipped:
                    continue

                if (new_rem := roll_remaining - val) >= 0:
                    new_state = deepcopy(state)
                    if front_flipped:
                        new_state._back_row[val - 1] = True
                    else:
                        new_state._front_row[val - 1] = True
                    recur_helper(new_rem, new_state)

        recur_helper(roll, self)

        return result

    def is_won(self) -> bool:
        """Whether the game has been won. Occurs when all tiles have been flipped"""

        return all(self._front_row) and all(self._back_row)


def dice_rolls(num_sides: int = 6) -> Generator[int, None, None]:
    rolls_range = range(1, num_sides + 1)
    for a, b in itertools.product(rolls_range, rolls_range):
        yield a + b


@dataclass
class AllGamesResult:
    """
    Resultant type for searching through the possibilites of all games.

    Simply holds the number of winning games and number of losing games.
    """

    num_won: int = 0
    num_lost: int = 0

    def __add__(self, other: "AllGamesResult") -> "AllGamesResult":
        return AllGamesResult(
            self.num_won + other.num_won, self.num_lost + other.num_lost
        )


NUM_GAMES = 0
def find_all_games(state: GameState = GameState()) -> AllGamesResult:
    """
    Runs through all possible games to find the number of winning and losing games.

    Recursively searches in a depth-first manner for games.
    May use exponential memory.

    Parameters:
        state (GameState): Current state of the game (holds front and back tiles flipped states).
                           Defaults to the starting game state.

    Returns:
        tuple[int, int]: num winning games, num losing games
    """

    if state.is_won():
        return AllGamesResult(1, 0)

    result = AllGamesResult(0, 0)

    for roll in dice_rolls():
        next_states = state.get_next_states(roll)

        # No possible next states -> lost the game
        if not next_states:
            result += AllGamesResult(0, 1)

        for next_state in next_states:
            result += find_all_games(next_state)

    return result


def main():
    print("Computing the result of all possible games...")

    all_games_result = find_all_games()

    print(all_games_result)


if __name__ == "__main__":
    main()
