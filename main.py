from solution import *
from sys import stdin, stderr, argv
from operator import itemgetter


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
            project.skills += [(skill, lvl)]
            project.tasks.append((skill, lvl))

        prob.projects[name] = project

    return prob



def sort_tasks(projects):
    temp_pr = []

    for project in projects:
        mx_lvl = 0
        for ts in project.tasks:
            if ts[1] > mx_lvl:
                mx_lvl = ts[1]
        temp_pr.append((project,mx_lvl,project.B))

    sorted_pr = sorted(temp_pr, key = itemgetter(1,2))
    new_pr = []
    for el in sorted_pr:
        new_pr.append(el[0])
    projects = new_pr
    return projects


def sort_by_score(projects):
    projects.sort(key=lambda x : (-x.S, x.B-x.D))
    return projects


def naive(problem):
    remaining_projects = list(problem.projects.values())
    people = list(problem.contribs.values())

    projects = []

    sol = Solution()
    while len(remaining_projects) != len(projects):
        #print("ok")
        #projects = sort_by_score(remaining_projects)
        projects = sorted(remaining_projects, key= lambda p:  p.S/(p.D*p.R))[::-1]
        #print(len(projects))
        remaining_projects = []

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
            #print(people_list)
            if None not in people_list:
                # Add asignment
                sol.assignments.append((project.name,[x.name for x in people_list]))
                sol.nb_projects += 1
                # Skill up people
                for idx, task in enumerate(project.tasks):
                    skill, taks_lvl = task
                    contrib = people_list[idx]
                    lvl = contrib.skills[skill]

                    if lvl < 100 and ((taks_lvl == lvl) or (taks_lvl == lvl+1)):
                        # print("lvl up - ", contrib.name, skill, contrib.skills[skill])
                        problem.contributor_skills[skill][lvl].remove(contrib)
                        contrib.skills[skill] += 1
                        problem.contributor_skills[skill][lvl+1].append(contrib)
                        # print("lvl up + ", contrib.name, skill, contrib.skills[skill])
            else:
                remaining_projects.append(project)

    return sol


if __name__ == "__main__":
    problem = parse()

    solution = naive(problem)

    solution.print()
    solution.print(stderr)
    if "--sol" in argv:
        print(solution.score(problem))
