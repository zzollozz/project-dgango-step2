# from django.test import TestCase
#
# # Create your tests here.
#
# # n = 5
# # fact = 1
# # for i in range(2, n + 1):
# #     fact = fact * i
# # print(fact)
# #
# a = [5, 1, 3, 4, 2, 7]
# # print(a[::-1])
# max = a[0]
# min = a[0]
#
# for index in range(len(a)):
#     if max < a[index]:
#         max = a[index]
#     elif min > a[index]:
#         min = a[index]
#
#
# print(f'максимальное число в списке => {max} Минимальное число в списке => {min}')
#
# print(f'Индекс максимального число в списке => {a.index(max)} Индекс Минимального число в списке => {a.index(min)}')
#
# sum = 0
#
# if a.index(max) < a.index(min):
#     for i in range(a.index(max) + 1, a.index(min)):
#         sum += a[i]
# else:
#     for i in range(a.index(min) + 1, a.index(max)):
#         sum += a[i]
# print(sum)
#
#

# # ==> Решето Эратосфена <==
# n = 64
# a = [i for i in range(0, n + 1)]
#
# a[1] = 0
#
# i = 2
# while i < n / 2:
#     j = i + i
#     while j <= n:
#         a[j] = 0
#         j = j + i
#     i += 1
#
# a = [i for i in a if a[i] != 0]
# print(a)
# """
# создаем массив длинной n элементов включительно
# начиная со второго элемента последовательно его просматриваем
# если число составное то заменяем его нулем
# после этого из изменненного списка уберем образовавшиеся нули и получим
# количество простых чисел строго меньше заданного n
#
# """


# # ==> Сортировка Вставкой <==
#
# def insertion_sort(nums):
#     # Сортировку начинаем со второго элемента, т.к. считается, что первый элемент уже отсортирован
#     for i in range(1, len(nums)):
#         item_to_insert = nums[i]
#         # Сохраняем ссылку на индекс предыдущего элемента
#         j = i - 1
#         # Элементы отсортированного сегмента перемещаем вперёд, если они больше
#         # элемента для вставки
#         while j >= 0 and nums[j] > item_to_insert:
#             nums[j + 1] = nums[j]
#             j -= 1
#         # Вставляем элемент
#         nums[j + 1] = item_to_insert
#
# # Проверяем, что оно работает
# random_list_of_nums = [9, 1, 15, 28, 6]
# insertion_sort(random_list_of_nums)
# print(random_list_of_nums)
from collections import defaultdict


# ascii_list = [' ', '!', 'D', 'S', 'A', 'N', 'a', 'm', 'a', 'D']
# letters = [0] * 95
#
# for i in ascii_list:
#     nomer = ord(i) - 32
#     letters[nomer] += 1
#
#
# for i in range(95):
#     if letters[i] > 0:
#         print(chr(i + 32) * letters[i], end=" ")

# """
# ввод: неупорядоченный массив из печатных ASCII символов (код символа 32-127)
# создаем список из 0 длинной 95 символов
# циклом пройдем по массиву из печатных ASCII символов и на каждой итерации текущий элемент преобразуем в код символа вычитая
# из него 32 полученный результат используем как индекс в созданном списке добавляя в него по еденице.
# По полученному списку со значениями количества символов проходим циклом с условием если значение больше или равно 1
# то индексу этого значения добавляем 32, преобразуем в символ ASCII и согласно количества в значении добавляем его в список
# вывод: получаем отсортированный по алфовиту список.
# сложность линейная
# тип сортировки подсчетом """
# data_list = ['D', '!', 'D', 'S', 'A', 'N', 'a', 'm', 'a', 'D']
# letters = [0] * 95
# res = []
# for el in data_list:
#     el_dec = ord(el) - 32
#     letters[el_dec] += 1
#
# for i in range(len(letters)):
#
#     if letters[i] >= 1:
#         for n in range(letters[i]):
#             res.append(chr(i + 32))
#
# print(res)

# import re
#
# sss = 'наша Мама пошла поГулять агент007, стриж, ГТО'
# lll = ['Мама', 'авТо', 'гриБ', 'агент007', 'стриж', 'ГТО']
#
#
# pattern = r'\b([а-я]*[А-Я][а-я]*)\b'
#
# print(re.findall(pattern, sss))
#
# for i in lll:
#     if not re.match(pattern, i):
#         print(i)


# def sdf(i):
#     i -= 1
#     if i:
#         print(i)
#         return sdf(i)
#
# sdf(5)

# class Node:
#     def __init__(self, val):
#         self.l_child = None
#         self.r_child = None
#         self.data = val
#
# def binary_insert(root, node):
#     if root is None:
#         root = node
#     else:
#         if root.data > node.data:
#             if root.l_child is None:
#                 root.l_child = node
#             else:
#                 binary_insert(root.l_child, node)
#         else:
#             if root.r_child is None:
#                 root.r_child = node
#             else:
#                 binary_insert(root.r_child, node)
#
# def in_order_print(root):
#     if not root:
#         return
#     in_order_print(root.l_child)
#     print(root.data)
#     in_order_print(root.r_child)
#
# def pre_order_print(root):
#     if not root:
#         return
#     print(root.data)
#     pre_order_print(root.l_child)
#     pre_order_print(root.r_child)
#
#
#
# r = Node(3)
# binary_insert(r, Node(7))
# binary_insert(r, Node(1))
# binary_insert(r, Node(5))
#
# print("in order:")
# in_order_print(r)
#
# print("pre order")
# pre_order_print(r)
#
# """
# in order:
# 1
# 3
# 5
# 7
# pre order
# 3
# 1
# 7
# 5
# """