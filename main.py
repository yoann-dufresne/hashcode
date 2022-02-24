from solution import *
from sys import stdin


def parse():
    C, P = [int(x) for x in stdin.readline().strip().split()]
    prob = Problem(C, P)

    for c_idx in range(C):
        name, num_skills = stdin.readline().strip().split()
        num_skills = int(num_skills)
        cont = Contributor(name, c_idx)

        for _ in range(num_skills):
            skill, lvl = stdin.readline().strip().split()
            lvl = int(lvl)
            cont.skills[skill] = lvl

        prob.contribs.append(cont)

    return prob



if __name__ == "__main__":
    problem = parse()

    print(problem)
