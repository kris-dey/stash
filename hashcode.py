#!/usr/bin/env python
import os
import sys
import subprocess
import cProfile

class Book:
    def __init__(self, i, score):
        self.i = i
        self.score = score

class Library:
    def __init__(self, i, signup_days, books, per_day):
        self.i = i
        self.signup_days = signup_days
        self.books = books
        self.per_day = per_day
        self.score_cache = 0
        self.sort_books()

    def score(self, remaining):
        remaining -= self.signup_days
        remaining *= self.per_day
        # remaining *= self.per_day #the good one
        books_tmp = self.books[:remaining]
        score_tmp = 0
        for book in books_tmp:
            score_tmp += book.score
        self.score_cache = score_tmp / (self.signup_days*5) #the good one
        return self.score_cache

    def get_libs_remaining(self, remaining):
        remaining -= self.signup_days
        remaining *= self.per_day
        self.books = self.books[:remaining]
        # return self.books[:remaining]

    def sort_books(self):
        self.books = sorted(self.books, key=lambda b: b.score, reverse=True)

    def update_books(self, rm_able):
        tmp_books = list(set(self.books) - rm_able)
        if len(tmp_books) != len(self.books):
            self.books = tmp_books
            self.sort_books()
        # self.books = set(self.books) - rm_able



class Scanner:
    def __init__(self, f_in, f_out):
        self.in_ = f_in
        self.out = f_out

    def n_list(self):
        return list(map(int, self.in_.readline().strip().split(' ')))

    def scan(self):
        header = self.n_list()
        #n_books = header[0]
        n_libraries = header[1]
        self.days = header[2]

        self.books = []
        for i, score in enumerate(self.n_list()):
            self.books.append(Book(i, score))

        self.libraries = []
        for i in range(n_libraries):
            info = self.n_list()
            l_books = list(map(lambda i: self.books[i], self.n_list()))
            self.libraries.append(Library(i, info[1], l_books, info[2]))

    def pick(self):
        chosen = []
        d = self.days
        refresh = True
        counter_def = 10
        counter = 0
        while d >= 0 and self.libraries:
            max_score = -999999999999
            max_lib = None
            for lib in self.libraries:
                if refresh:
                    score = lib.score(d)
                else:
                    score = lib.score_cache
                #score = -lib.signup_days
                if score > max_score:
                    max_score = score
                    max_lib = lib
            if not max_lib:
                break

            max_lib.get_libs_remaining(d)
            if not max_lib.books:
                break

            chosen.append(max_lib)
            self.libraries.remove(max_lib)
            d -= max_lib.signup_days

            # do collision
            rm_able = set(max_lib.books)
            if refresh:
                for lib in self.libraries:
                    lib.update_books(rm_able)
            if counter == counter_def:
                refresh = True
                counter = 0
            else:
                refresh = False
        self.chosen = chosen

    def write(self):
        self.out.write(f'{len(self.chosen)}\n')
        for lib in self.chosen:
            self.out.write(f'{lib.i} {len(lib.books)}\n')
            self.out.write(f'{" ".join(map(lambda b: str(b.i), lib.books))}\n')

def main():
    def run(i, o):
        scanner = Scanner(i, o)
        scanner.scan()
        scanner.pick()
        scanner.write()

    if len(sys.argv) > 1:
        with open(sys.argv[1]) as i:
            with open(sys.argv[2], 'w') as o:
                run(i, o)
    else:
        procs = []
        for f in os.listdir('in/'):
            i = os.path.join('in', f)
            o = os.path.join('out', f'{f[0]}.txt')
            procs.append(subprocess.Popen([sys.argv[0], i, o]))
        for p in procs:
            p.wait()


if __name__ == '__main__':
    main()

