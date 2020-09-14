import random


def get_random_array(size=10, min_val=-5, max_val=5):
    """Generates random array with length = size
    size: length of array. Default is 10
    min_val: minimum value in array. Default is -5
    max_val: maximum value in array. Default is 5"""
    assert isinstance(size, int)
    return [random.randint(min_val, max_val) for _ in range(size)]


def findMaxSubArray(A):
    if len(A) == 1:
        return A

    # A = A[:len(A)-1] if A[0] > A[-1] else A[1:]

    # фиксируем начальную сумму и начальный индекс
    start_indx = end_indx = 0
    last_sum = A[start_indx]

    # проходим по каждому элементу массива
    for current_indx, current_val in enumerate(A):
        current_sum = sum(A[start_indx:current_indx]) + A[current_indx]

        # Если текущее значение > суммы предыдущ. эл=тов
        if A[current_indx] > current_sum:
            # обновляем значения
            start_indx = end_indx = current_indx
            last_sum = A[start_indx]

        if current_sum > last_sum:
            last_sum = current_sum
            end_indx = current_indx

    return A[start_indx: end_indx+1]


if __name__ == "__main__":

    test_array = get_random_array() # [4, -1, 2, 0, -5, 6] # [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    print(test_array)
    result = findMaxSubArray(test_array)

    print('max sum is', sum(result))
    print('max sub array', result)