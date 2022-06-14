from episode01.samples import clues2x2, clues5x5s
from episode03b.puzzle import Puzzle


def test_init_clues2x2():
    puzzle2x2 = Puzzle(clues2x2)
    assert puzzle2x2.required_blacks_count == 3
    assert puzzle2x2.norm_clues == {'rows': [[1], [2]],
                                    'cols': [[2], [1]]}
    assert puzzle2x2.is_consistent()


def test_init_clues5x5s():
    puzzle5x5s = Puzzle(clues5x5s)
    assert puzzle5x5s.required_blacks_count == 14
    assert puzzle5x5s.norm_clues == {'rows': [[1], [3], [1, 1], [3], [5]],
                                     'cols': [[1], [4], [2, 2], [4], [1]]}
    assert puzzle5x5s.is_consistent()


def test_clues_with_differnts_sums_in_rows_and_cols_are_inconsistent():
    # inbalanced clues 2 in rows and 3 in cols
    clues1 = {
        'rows': [1, 1],
        'cols': [2, 1]
    }
    puzzle1 = Puzzle(clues1)
    print(f"blacks in rows={puzzle1.get_black_count(axis='rows')}")
    print(f"blacks in cols={puzzle1.get_black_count(axis='cols')}")
    assert not puzzle1.is_consistent()
