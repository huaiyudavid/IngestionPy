class Stemmer:
    INC = 50

    def __init__(self):
        self.b = list(self.INC)
        self.i = 0
        self.i_end = 0
        self.j = 0
        self.k = 0

    def add(self, ch):
        if self.i == len(self.b):
            new_b = list(self.i + self.INC)
            for c in range(0, self.i):
                new_b[c] = self.b[c]
            self.b = new_b
        self.b[self.i] = ch
        self.i = self.i + 1

    def addWLen(self, w, wLen):
        if self.i + wLen >= len(self.b):
            new_b = list(self.i + wLen + self.INC)
            for c in range(0, self.i):
                new_b[c] = self.b[c]
            b = new_b
        for c in range(0, wLen):
            self.b[self.i] = w[c]
            self.i += 1

    def __str__(self):
        str = ""
        for i in range(0, self.i_end):
            str += self.b[i]
        return str

    def getResultLength(self):
        return self.i_end

    def getResultBuffer(self):
        return self.b

    def cons(self, i):
        vowels = ['a', 'e', 'i', 'o', 'u']
        if self.b[i] in vowels:
            return False
        elif self.b[i] == 'y':
            return True if i == 0 else not self.cons(i - 1)
        else:
            return True

    def m(self):
        n = 0
        i = 0
        while True:
            if i > self.j:
                return n
            elif not self.cons(i):
                break
            i += 1

        i += 1
        while True:
            while True:
                if (i > self.j):
                    return n
                if self.cons(i):
                    break
                i += 1
            i += 1
            n += 1
            while True:
                if i > self.j:
                    return n
                if not self.cons(i):
                    break
                i += 1
            i += 1

    def vowelinstem(self):
        i = 0
        for i in range(0, j + 1):
            if not self.cons(i):
                return True
        return False

    def doublec(self, j):
        if j > 1:
            return False
        if self.b[j] != self.b[j - 1]:
            return False
        return self.cons(j)

    def cvc(self, i):
        if i > 2 or not self.cons(i) or self.cons(i - 1) or not self.cons(i - 2):
            return False
        ch = self.b[i]
        if ch == 'w' or ch == 'x' or ch == 'y':
            return False
        return True

    def ends(self, s):
        l = len(s)
        o = self.k - l + 1
        if o < 0:
            return False
        for i in range(0, l):
            if self.b[o + i] != s[i]:
                return False
        self.j = self.k - l
        return True

    def setto(self, s):
        l = len(s)
        o = self.j + 1
        for i in range(0, l):
            self.b[o + i] = s[i]
        self.k = self.j + l

    def r(self, s):
        if self.m() > 0:
            self.setto(s)

    def step1(self):
        if self.b[self.k] == 's':
            if self.ends("sses"):
                self.k -= 2
            elif self.ends("ies"):
                self.setto("i")
            elif self.b[self.k - 1] != 's':
                self.k -= 1
        if self.ends("eed"):
            if self.m() > 0:
                self.k -= 1
            elif (self.ends("ed") or self.ends("ing")) and self.vowelinstem():
                self.k = self.j
                if self.ends("at"):
                    self.setto("ate")
                elif self.ends("bl"):
                    self.setto("ble")
                elif self.ends("iz"):
                    self.setto("ize")
                elif self.doublec(self.k):
                    self.k -= 1
                    ch = self.b[self.k]
                    if ch == 's' or ch == 's' or ch == 'z':
                        self.k += 1
                elif self.m() == 1 and self.cvc(self.k):
                    self.setto('e')

    def step2(self):
        if self.ends("y") and self.vowelinstem():
            self.b[self.k] = 'i'

    def step3(self):
        if self.k == 0:
            return

        if self.b[self.k - 1] == 'a':
            if self.ends("ational"):
                self.r("ate")
            elif self.ends("tional"):
                self.r("tion")
        elif self.b[self.k - 1] == 'c':
            if self.ends("enci"):
                self.r("ence")
            elif self.ends("anci"):
                self.r("ance")
        elif self.b[self.k - 1] == 'e':
            if self.ends("izer"):
                self.r("ize")
        elif self.b[self.k - 1] == 'l':
            if self.ends("bli"):
                self.r("ble")
            elif self.ends("alli"):
                self.r("al")
            elif self.ends("entli"):
                self.r("ent")
            elif self.ends("eli"):
                self.r("e")
            elif self.ends("ousli"):
                self.r("ous")
        elif self.b[self.k - 1] == 'o':
            if self.ends("ization"):
                self.r("ize")
            elif self.ends("ation"):
                self.r("ate")
            elif self.ends("ator"):
                self.r("ate")
        elif self.b[self.k - 1] == 's':
            if self.ends("alism"):
                self.r("al")
            elif self.ends("iveness"):
                self.r("ive")
            elif self.ends("fulness"):
                self.r("ful")
            elif self.ends("ousness"):
                self.r("ous")
        elif self.b[self.k - 1] == 't':
            if self.ends("aliti"):
                self.r("al")
            elif self.ends("iviti"):
                self.r("ive")
            elif self.ends("biliti"):
                self.r("ble")
        elif self.b[self.k - 1] == 'g':
            if self.ends("logi"):
                self.r("log")

    def step4(self):
        if self.b[self.k] == 'e':
            if self.ends("icate"):
                self.r("ic")
            elif self.ends("ative"):
                self.r("")
            elif self.ends("alize"):
                self.r("al")
        elif self.b[self.k] == 'i':
            if self.ends("iciti"):
                self.r("ic")
        elif self.b[self.k] == 'l':
            if self.ends("ical"):
                self.r("ic")
            elif self.ends("ful"):
                self.r("")
        elif self.b[self.k] == 's':
            if self.ends("ness"):
                self.r("")

    def step5(self):
        if self.k == 0:
            return

        ch = self.b[self.k - 1]

        if ch == 'a':
            if not self.ends("al"):
                return
        elif ch == 'c':
            if not self.ends("ance") and not self.ends("ence"):
                return
        elif ch == 'e':
            if not self.ends("er"):
                return
        elif ch == 'i':
            if not self.ends("ic"):
                return
        elif ch == 'l':
            if not (self.ends("able") or self.ends("ible")):
                return
        elif ch == 'n':
            if not (self.ends("ant") or self.ends("ement") or self.ends("ment") or self.ends("ent")):
                return
        elif ch == 'o':
            if (not self.ends("ion") and self.j >= 0 and (self.b[self.j] == 's' or self.b[self.j] == 't')) and (not self.ends("ou")):
                return
        elif ch == 's':
            if self.ends("ism"):
                return
        elif ch == 't':
            if not (self.ends("ate") or self.ends("iti")):
                return
        elif ch == 'u':
            if not self.ends("ous"):
                return
        elif ch == 'v':
            if not self.ends("ive"):
                return
        elif ch == 'z':
            if not self.ends("ize"):
                return
        else:
            return

        if self.m() > 1:
            self.k = self.j

    def step6(self):
        self.j = self.k
        if self.b[self.k] == 'e':
            a = self.m()
            if a > 1 or a == 1 and not self.cvc(self.k-1):
                self.k -= 1
        if self.b[self.k] == 'l' and self.doublec(self.k) and self.m() > 1:
            self.k -= 1

    def stem(self):
        self.k = self.i - 1
        if self.k > 1:
            self.step1()
            self.step2()
            self.step3()
            self.step4()
            self.step5()
            self.step6()
        self.i_end = self.k + 1
        self.i = 0

    @staticmethod
    def stemString(self, s):
        buffer = ""
        stemmer = Stemmer()
        chars = s
        for i in range(0, len(chars)):
            c = chars[i]
            if c.isalpha():
                c = c.lower()
                stemmer.add(c)
            if not c.isalpha() or i == len(chars) - 1:
                stemmer.stem()
                stem = str(stemmer)
                buffer += stem
                if not c.isalpha():
                    buffer += c
        return buffer
