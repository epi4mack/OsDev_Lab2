import string
import multiprocessing
import hashlib
from time import perf_counter
from os import system

alphabet = string.ascii_lowercase

hash1 = "1115dd800feaacefdf481f1f9070374a2a81e27880f187396db67958b207cbad"
hash2 = "3a7bd3e2360a3d29eea436fcfb7e44c735d117c42d1c1835420b6b9942dd4f1b"
hash3 = "74e1bb62f8dabb8125a58852b63bdf6eaef667cb56ac7f7cdba6d7305c50a22f"

hashes = [hash1, hash2, hash3]

def bruteforce(event=None, hash='', start_letter:str = 'a'):
    global alphabet
    start_index = alphabet.index(start_letter)
    alphabet = alphabet[start_index:] + alphabet[:start_index]

    current_string = start_letter * 5

    while True:
        if hashlib.sha256(current_string.encode()).hexdigest() == hash:
            print(f"Найденный пароль: {current_string}")
            if event is not None: event.set()
            return

        temp = list(current_string)
        index = len(temp) - 1

        while index >= 0:
            if temp[index] != alphabet[-1]:
                temp[index] = alphabet[alphabet.index(temp[index]) + 1]
                break
            else:
                temp[index] = alphabet[0]
                index -= 1

        current_string = ''.join(temp)

def get_num_threads() -> int:
    while True:
        try:
            if int(num_threads) > 0:
                return int(num_threads)
            else:
                system("cls")
                num_threads = input("Введите количество потоков: ")
        except:
            system("cls")
            num_threads = input("Введите количество потоков: ")

if __name__ == '__main__':
    system("cls")

    num = get_num_threads()

    if num > 26: num = 26

    system("cls")

    if num == 1:
        print(f"Однопоточный режим\n")

        total_start = perf_counter()

        for hash in hashes:
            t1 = perf_counter()
            print(f"Поиск пароля для хэш-значения: {hash}")
            bruteforce(hash=hash)
            print(f"Заняло времени: {perf_counter() - t1}")
            print('-'*96)

        print(f"Затраченное на поиск трех паролей время: {perf_counter() - total_start}\n")
    else:
        print(f"Используется потоков: {num}\n")

        total_start = perf_counter()
        processes = []
        
        for hash in hashes:
            t1 = perf_counter()
            event = multiprocessing.Event()

            for i in range(num):
                processes.append(multiprocessing.Process(target=bruteforce, args=(event, hash, alphabet[-i],)))

            print(f"Поиск пароля для хэш-значения: {hash}")

            for process in processes:
                process.start()

            event.wait()

            if event.is_set():
                for process in processes:
                    if process.is_alive(): process.terminate()

            for process in processes:
                process.join()

            print(f"Заняло времени: {perf_counter() - t1}")
            print('-'*96)
            processes.clear()

        print(f"Затраченное на поиск трех паролей время: {perf_counter() - total_start}\n")
