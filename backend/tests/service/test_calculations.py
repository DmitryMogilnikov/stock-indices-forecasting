from backend.src.service import calculations


def test_is_reduction_sufficient():
    # Case where the reduction is sufficient
    assert calculations.is_reduction_sufficient(
        4.59,
        3.41,
        1.0
    )

    # Case where the reduction is insufficient
    assert not calculations.is_reduction_sufficient(
        4.59,
        3.82,
        1.0
    )

    # Case when percent_change > initial_percent
    assert not calculations.is_reduction_sufficient(
        3.82,
        4.59,
        1.0
    )


def test_get_days_to_reduce_procent():
    # Case for an empty array of changes
    assert calculations.get_days_to_reduce_procent(
        [],
        4.60,
        0.6
    ) == 0

    # Case when the decrease is sufficient after the third day
    assert calculations.get_days_to_reduce_procent(
        [4.59, 4.21, 3.89, 2.47],
        4.60,
        0.6
    ) == 3

    # Case where the reduction is achieved on the last day
    assert calculations.get_days_to_reduce_procent(
        [4.59, 4.21, 3.89, 2.47],
        4.60,
        1.0
    ) == 4

    # Case where the reduction is not enough after all the days
    assert calculations.get_days_to_reduce_procent(
        [4.59, 4.21, 3.89, 2.47],
        4.60,
        5.0
    ) == 0


def test_calculate_days_to_target_reductions():
    # Case for an empty array of changes
    assert calculations.calculate_days_to_target_reduction(
        [],
        0.6
    ) == []

    # Case with correct calculation of days
    assert calculations.calculate_days_to_target_reduction(
        [4.59, 4.21, 3.89, 2.47],
        0.6
    ) == [2, 2, 1, 0]

    # Case where the desired target reduction will never be achieved
    assert calculations.calculate_days_to_target_reduction(
        [4.59, 4.21, 3.89, 2.47],
        5.0
    ) == [0, 0, 0, 0]

    # A case where the desired change will be received immediately
    assert calculations.calculate_days_to_target_reduction(
        [4.59, 4.21, 3.89, 2.47],
        0.1
    ) == [1, 1, 1, 0]

    # A case where the desired change will be received on the last day
    assert calculations.calculate_days_to_target_reduction(
        [4.59, 4.21, 3.89, 2.47],
        2.1
    ) == [3, 0, 0, 0]
