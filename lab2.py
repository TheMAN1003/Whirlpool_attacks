# var 10 Whirlpool
import whirlpool
import secrets
import time
import numpy as np
import pickle

# random.seed(42)


def whirl(message: bytes, n):
    h = whirlpool.new(message)
    hashed_output = h.hexdigest()
    length = int(n/4)
    return hashed_output[-length:]


def byte(message):
    return bytes.fromhex(message)


def new_hex(bit_length):
    hexstr = hex(secrets.randbits(bit_length))[2:]
    return "0" * (int(bit_length / 4) - len(hexstr)) + hexstr


gen = False
r = ""


def excess_func(n, x):
    global gen
    global r
    if gen == False:
        r = new_hex(128 - n)
        gen = True
    s = r + x
    return str(s)


def hex_to_bin(hex, n):
    bitstr = str(bin(int(hex, 16)))[2:]
    return "0" * (int(len(hex) * n / 4) - len(bitstr)) + bitstr


def byte_to_hex(bytes):
    return ''.join([hex(i)[2:].zfill(2) for i in bytes])


def build_table(K, L, n):
    res = np.array(["", ""] * K, dtype=object)
    for i in range(K):
        x0 = new_hex(n)
        x = x0
        for j in range(L):
            x = whirl(byte(excess_func(n, x)), n)
        res[i] = (x0, x)
    return res


def random_prototype_search(K, L, table, h, n):
    y = h
    for j in range(L):
        for i in range(K):
            if table[i][1] == y:
                x = table[i][0]
                for m in range(L - j - 1):
                    x = whirl(byte(excess_func(n, x)), n)
                return excess_func(n, x)
        y = whirl(byte(excess_func(n, y)), n)
    return "Error"

def build_table_2(K, L, n, r):
    res = np.array(["", ""] * K, dtype=object)
    for i in range(K):
        x0 = new_hex(n)
        x = x0
        for j in range(L):
            x = whirl(byte(r + x), n)
        res[i] = (x0, x)
    return res


def random_prototype_search_2(K, L, table, h, n, r):
    y = h
    for j in range(L):
        for i in range(K):
            if table[i][1] == y:
                x = table[i][0]
                for m in range(L - j - 1):
                    x = whirl(byte(r + x), n)
                return r + x
        y = whirl(byte(r + y), n)
    return "Error"


N = 10_000
cut = 32
cut_easy = 16

K = [2**20, 2**22, 2**24]
L = [2**10, 2**11, 2**12]

K_easy = [2**10, 2**12, 2**14]
L_easy = [2**5, 2**6, 2**7]

file_path = [["1.pkl", "2.pkl", "3.pkl"], ["4.pkl", "5.pkl", "6.pkl"], ["7.pkl", "8.pkl", "9.pkl"]]
file_path_1 = "chances.txt"

success = ""
p = 0
q = 0

time_start = time.time()
for k in K:
    for l in L:
        count_success = 0
        table = build_table(k, l, cut)
        with open(file_path[p][q], 'wb') as file:
            pickle.dump(table, file)
        for i in range(N):
            input_vector = byte(new_hex(256))
            h = whirl(input_vector, cut)
            x = random_prototype_search(k, l, table, h, cut)
            if x != "Error":
                res = whirl(byte(x), cut)
                if h == res:
                    count_success += 1
                    # print(f'K = {k}')
                    # print(f'L = {l}')
                    # print(f'message = {input_vector}')
                    # print(f'input hash = {h}')
                    # print(f'found collision = {res}')
        success_rate = count_success / N * 100
        success += f'Success rate for K={k}, L={l}: {success_rate}%\n'
        print(f'Success rate for K={k}, L={l}: {success_rate}%')
        q += 1
    p += 1
    q = 0


time_end = time.time()
print(f"Time elapsed = {time_end-time_start} seconds")
success += f"Time elapsed = {time_end-time_start} seconds \n"

print(success)
with open(file_path_1, 'w') as file:
    file.write(success)


N = 10_000
cut = 32
cut_easy = 16

K = [2**10, 2**11, 2**12]
L = [2**10, 2**11, 2**12]

K_easy = [2**5, 2**6, 2**7]
L_easy = [2**5, 2**6, 2**7]

success = ""
list = []

time_start = time.time()


for k in K:
    for l in L:
        tables = []
        count_success = 0
        for j in range(k):
            r = new_hex(128-cut)
            list.append(r)
            tables.append(build_table_2(k, l, cut, r))
        for i in range(N):
            input_vector = byte(new_hex(256))
            h = whirl(input_vector, cut)
            x = random_prototype_search(k, l, tables[i], h, cut, list[i])
            if x != "Error":
                res = whirl(byte(x), cut)
                if h == res:
                    count_success += 1
                    # print(f'K = {k}')
                    # print(f'L = {l}')
                    # print(f'message = {input_vector}')
                    # print(f'input hash = {h}')
                    # print(f'found collision = {res}')
        success_rate = count_success / N * 100
        success += f'Success rate for K={k}, L={l}: {success_rate}%\n'
        print(f'Success rate for K={k}, L={l}: {success_rate}%')

time_end = time.time()
for i in success:
    print(f'Success rate is {i}%')

print(f"Time elapsed = {time_end-time_start} seconds")
success += f"Time elapsed = {time_end-time_start} seconds \n"

print(success)
with open(file_path_1, 'w') as file:
    file.write(success)
