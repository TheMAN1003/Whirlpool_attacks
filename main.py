# var 10 Whirlpool
import whirlpool
import random
import time
import numpy as np
from scipy import stats


def whirl(message):
    h = whirlpool.new(message.encode())
    hashed_output = h.hexdigest()
    return hashed_output


def insert_change(message):
    pos = random.randint(0, len(message) - 1)
    letter_list = list(message)
    new_letter = chr(random.randint(32, 126))
    while letter_list[pos] == new_letter:
        new_letter = chr(random.randint(32, 126))
    letter_list[pos] = new_letter
    return ''.join(letter_list)


def form_message_rps():
    message = "NedozhdiiMaksymAndriyovich"
    suffix = random.randint(10**5, 10**6-1)
    message += str(suffix)
    return message


def form_message_bd():
    message = "NedozhdiiMaksymAndriyovych"
    prefix = str(random.randint(10 ** 5, 10 ** 6 - 1))
    prefix += message
    return prefix


def random_prototype_search1():
    starting_message = form_message_rps()
    hashed_message = whirl(starting_message)
    messages = [starting_message]
    thirty_hashes = [hashed_message]
    i = 1
    while True:
        my_message = starting_message + str(i)
        my_hashed_message = whirl(my_message)
        if i < 30:
            messages.append(my_message)
            thirty_hashes.append(my_hashed_message)
        if hashed_message[-4:] == my_hashed_message[-4:]:
            messages.append(my_message)
            thirty_hashes.append(my_hashed_message)
            return [messages, thirty_hashes, i]
        i += 1


def random_prototype_search2():
    starting_message = form_message_rps()
    my_message = starting_message
    hashed_message = whirl(starting_message)
    messages = [starting_message]
    thirty_hashes = [hashed_message]
    i = 1
    while True:
        my_message = insert_change(my_message)
        if my_message == starting_message:
            continue
        my_hashed_message = whirl(my_message)
        if i < 30:
            messages.append(my_message)
            thirty_hashes.append(my_hashed_message)
        if hashed_message[-4:] == my_hashed_message[-4:]:
            messages.append(my_message)
            thirty_hashes.append(my_hashed_message)
            return [messages, thirty_hashes, i]
        i += 1


def birthday1():
    starting_message = form_message_bd()
    hashed_message = whirl(starting_message)
    hashes = [hashed_message]
    messages_with_short_keys = {hashed_message[-8:]: starting_message}
    messages = [starting_message]
    thirty_hashes = [hashed_message]
    i = 1
    while True:
        message = starting_message + str(i)
        my_hashed_message = whirl(message)
        if i < 30:
            messages.append(message)
            thirty_hashes.append(my_hashed_message)
        new_key = my_hashed_message[-8:]
        if new_key in messages_with_short_keys:
            messages.append(messages_with_short_keys.get(new_key))
            thirty_hashes.append(hashes[list(messages_with_short_keys.keys()).index(new_key)])
            col_index = list(messages_with_short_keys.keys()).index(new_key)
            messages_with_short_keys[new_key] = message
            messages.append(message)
            thirty_hashes.append(my_hashed_message)
            hashes.append(my_hashed_message)
            return [messages, thirty_hashes, i, col_index]
        messages_with_short_keys[new_key] = message
        hashes.append(my_hashed_message)
        i += 1


def birthday2():
    message = form_message_bd()
    hashed_message = whirl(message)
    hashes = [hashed_message]
    messages_with_short_keys = {hashed_message[-8:]: message}
    messages = [message]
    thirty_hashes = [hashed_message]
    i = 1
    while True:
        message = insert_change(message)
        my_hashed_message = whirl(message)
        if i < 30:
            messages.append(message)
            thirty_hashes.append(my_hashed_message)
        new_key = my_hashed_message[-8:]
        if new_key in messages_with_short_keys:
            if message == messages_with_short_keys[new_key]:
                continue
            messages.append(messages_with_short_keys.get(new_key))
            thirty_hashes.append(hashes[list(messages_with_short_keys.keys()).index(new_key)])
            col_index = list(messages_with_short_keys.keys()).index(new_key)
            messages_with_short_keys[new_key] = message
            messages.append(message)
            thirty_hashes.append(my_hashed_message)
            return [messages, thirty_hashes, i, col_index]
        messages_with_short_keys[new_key] = message
        hashes.append(my_hashed_message)
        i += 1


print("Атака прообразів варіант 1:")
difficulty = []
time_start = time.time()
for j in range(100):
    result = random_prototype_search1()
    if j == 0:
        print("Перші 30 і останнє повідомлення: ")
        for message in result[0]:
            print(message)
        print("Відповідні значення гешів:")
        for hashes in result[1]:
            print(hashes)
    difficulty.append(result[2])

print(difficulty)
mean = np.mean(difficulty)
variance = np.var(difficulty, ddof=1)
confidence_interval = stats.t.interval(0.95, len(difficulty) - 1, loc=mean, scale=stats.sem(difficulty))
print(mean)
print(variance)
print(confidence_interval)
time_end = time.time()
print("time elapsed: ", time_end-time_start)


print("Атака прообразів варіант 2:")
difficulty = []
time_start = time.time()
for j in range(100):
    result = random_prototype_search2()
    if j == 0:
        print("Перші 30 і останнє повідомлення: ")
        for message in result[0]:
            print(message)
        print("Відповідні значення гешів:")
        for hashes in result[1]:
            print(hashes)
    difficulty.append(result[2])

print(difficulty)
mean = np.mean(difficulty)
variance = np.var(difficulty, ddof=1)
confidence_interval = stats.t.interval(0.95, len(difficulty) - 1, loc=mean, scale=stats.sem(difficulty))
print(mean)
print(variance)
print(confidence_interval)
time_end = time.time()
print("time elapsed: ", time_end-time_start)


print("Атака днів народження варіант 1:")
difficulty = []
time_start = time.time()
for j in range(100):
    result = birthday1()
    if j == 0:
        print("Перші 30 і останнє повідомлення: ")
        for message in result[0]:
            print(message)
        print("Відповідні значення гешів:")
        for hashes in result[1]:
            print(hashes)
        print("Індекси повідомлень, що співпали:")
        print(result[3], result[2])
    difficulty.append(result[2])

print(difficulty)
mean = np.mean(difficulty)
variance = np.var(difficulty, ddof=1)
confidence_interval = stats.t.interval(0.95, len(difficulty) - 1, loc=mean, scale=stats.sem(difficulty))
print(mean)
print(variance)
print(confidence_interval)
time_end = time.time()
print("time elapsed: ", time_end-time_start)


print("Атака днів народжень варіант 2:")
difficulty = []
time_start = time.time()
for j in range(100):
    result = birthday2()
    if j == 0:
        print("Перші 30 і останнє повідомлення: ")
        for message in result[0]:
            print(message)
        print("Відповідні значення гешів:")
        for hashes in result[1]:
            print(hashes)
        print("Індекси повідомлень, що співпали:")
        print(result[3], result[2])
    difficulty.append(result[2])

print(difficulty)
mean = np.mean(difficulty)
variance = np.var(difficulty, ddof=1)
confidence_interval = stats.t.interval(0.95, len(difficulty) - 1, loc=mean, scale=stats.sem(difficulty))
print(mean)
print(variance)
print(confidence_interval)
time_end = time.time()
print("time elapsed: ", time_end-time_start)

