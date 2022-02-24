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

        prob.add_contrib(cont)

    for p_idx in range(P):
        sp = stdin.readline().strip().split()
        name = sp[0]
        D, S, B, R = [int(x) for x in sp[1:]]

        project = Project(name, p_idx, D, S, B, R)

        for _ in range(R):
            skill, lvl = stdin.readline().strip().split()
            lvl = int(lvl)
            project.skills[skill] = lvl
            project.tasks.append((skill, lvl))

        prob.projects[name] = project

    return prob



def naive(problem):
    projects = list(problem.projects.values())
    people = list(problem.contribs.values())

    sol = Solution()
    for project in projects:
        used_people = set()
        people_list = []
        for skill, lvl in project.tasks:
            contrib = None
            for possible_contrib in problem.contributor_skills[skill][lvl:]:
                if len(possible_contrib) > 0:
                    for c in possible_contrib:
                        if c not in used_people:
                            contrib = c
                            used_people.add(c)
                    break
            people_list.append(contrib)
        if None not in people_list:
            sol.assignments.append([x.name for x in people_list])
            sol.nb_projects += 1

    return sol


if __name__ == "__main__":
    problem = parse()

    # solution = Solution()
    # solution.parse("data/sol_a.txt")
    solution = naive(problem)

    print(solution)
    solution.print()
    print(solution.score(problem))
