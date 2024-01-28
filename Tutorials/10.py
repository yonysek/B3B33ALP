objemy = [2, 5, 9]
cil = 3


def je_cil(s):
    return s[0] == cil or s[1] == cil or s[2] == cil


fr = [((0, 0, 0), "")]
byli = {}
byli[(0, 0, 0)] = 1

konec = False
while len(fr) > 0 and not konec:
    s, cesta = fr.pop(0)
    print(s, cesta)
    if cesta != "":
        cesta += ","
    for i in range(3):
        if s[i] < objemy[i]:
            s2 = [x for x in s]
            s2[i] = objemy[i]
            c2 = cesta + "N" + str(i)
            if je_cil(s2):
                print(c2)
                konec = True
                break
            t2 = tuple(s2)
            if not t2 in byli:
                fr.append((t2, c2))
                byli[t2] = 1
    if konec:
        break
    for i in range(3):
        if s[i] > 0:
            s2 = [x for x in s]
            s2[i] = 0
            c2 = cesta + "V" + str(i)
            if je_cil(s2):
                print(c2)
                konec = True
                break
            t2 = tuple(s2)
            if not t2 in byli:
                fr.append((t2, c2))
                byli[t2] = 1
    if konec:
        break
    for i in range(3):
        for j in range(3):
            if i != j and s[i] > 0 and s[j] < objemy[j]:
                s2 = [x for x in s]
                if s[i] <= objemy[j] - s[j]:
                    s2[j] += s2[i]
                    s2[i] = 0
                else:
                    s2[i] -= objemy[j] - s[j]
                    s2[j] = objemy[j]
                c2 = cesta + str(i) + "P" + str(j)
                if je_cil(s2):
                    print(c2)
                    konec = True
                    break
                t2 = tuple(s2)
                if not t2 in byli:
                    fr.append((t2, c2))
                    byli[t2] = 1
if not konec:
    print("Neexistuje reseni")


###
class Person:
    def __init__(self, name, sex):
        self.name = name
        self.sex = sex
        self.children = []
        self.parents = []  # parents of this node
        self.partner = None  # partner (=husband/wife of this node)

    def addChild(self, node):
        self.children.append(node)

    def addParent(self, node):
        self.parents.append(node)

    def setPartner(self, node):
        self.partner = node

    def __repr__(self):
        s = "Female" if self.sex == "F" else "Male"
        return self.name + " " + s


p = Person("Petr", "M")
print(p)
x = Person("x", "M")
p.addChild(x)
