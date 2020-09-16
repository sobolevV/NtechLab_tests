import random


def get_random_array(size=10, min_val=-5, max_val=5):
    """Generates random array with length = size
    size: length of array. Default is 10
    min_val: minimum value in array. Default is -5
    max_val: maximum value in array. Default is 5"""
    return [random.randint(min_val, max_val) for _ in range(size)]


def findMaxSubArray(A):
    if len(A) == 1:
        return A

    # начальные индексы подмассива
    start_indx = end_indx = 0
    # фиксируем последнюю сумму и сумму для текущего обхода подмассива
    last_sum = current_sum = 0

    # проходим по каждому элементу массива
    for current_indx, current_val in enumerate(A):
        # если текущая сумма уменьшается <= 0
        if current_sum <= 0:
            current_sum = current_val  # сохраняем значение для текущего "обхода" подмассива
            start_indx = current_indx  # обновляем начальную позицию т.к. пред. эл-ты умеьшают сумму
        else:
            # иначе сумма > 0, добавляем элемент
            current_sum += current_val

        # если сумма текущего подмассива увеличилась
        if current_sum > last_sum:
            last_sum = current_sum  # сохраняем эту сумма
            end_indx = current_indx  # обновляем последний индекс

    return A[start_indx: end_indx+1], last_sum


if __name__ == "__main__":

    test_array = [-2, 1, -3, 4, -1, 2, 1, -5, 4]  # get_random_array()
    print(test_array)

    sub_array, array_sum = findMaxSubArray(test_array)

    print('max sum is', array_sum)
    print('max sub array', sub_array)