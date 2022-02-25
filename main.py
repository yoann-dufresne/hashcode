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
            project.mean_lvl = sum([x[1] for x in project.skills])/len(project.skills)

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

def most_available(list_people):
    #return sorted(list_people, key=lambda x: nb_tasks[x.name])
    return list_people

def add_people(people_list, used_people, project, problem):
    # try adding people who have the required skills
    for skill, lvl in project.tasks:
        contrib = None
        for possible_contrib in problem.contributor_skills[skill][lvl:]:
            if len(possible_contrib) > 0:
                #for c in most_available(possible_contrib):
                for c in possible_contrib:
                    if c.name not in used_people:
                        contrib = c
                        used_people.add(c.name)
                break
        people_list.append(contrib)

 
# mentorship program
# Input: a list of people (people_list) assigned to project
#        which may contain None entries, i.e. a skill was unfilled.
# Output: a augmented list with people who will be mentored.

def add_mentees(people_list, used_people, project, problem):
    # determine what skills are already available in the input list
    can_mentor = set()
    for i, contrib in enumerate(people_list):
        skill,lvl = project.tasks[i]
        if contrib is not None:
            for j,x in enumerate(project.tasks):
                other_skill, other_lvl  = x
                if skill == other_skill: continue
                if other_skill in contrib.skills and contrib.skills[other_skill] >= other_lvl:
                    can_mentor.add(j)
    # adding mentees when there's a mentor present
    for i,x in enumerate(project.tasks):
        skill, lvl = x
        contrib = people_list[i]
        if contrib is None:
            # try to add mentees
            if i in can_mentor:
                possible_contrib = problem.contributor_skills[skill][lvl-1]
                if len(possible_contrib) > 0:
                    for c in most_available(possible_contrib):
                        if c.name not in used_people:
                            contrib = c
                            used_people.add(c.name)
                    break
                if contrib is not None:
                    print(f"[debug mentee] added a mentee with skill {skill} level {lvl-1}")
                    people_list[i] = contrib
    # finally, retry by adding anyone with a pulse ;) when a needed mentored skill has level 1
    for i,x in enumerate(project.tasks):
        skill, lvl = x
        if lvl == 1:
            contrib = people_list[i]
            if contrib is None:
                if i in can_mentor:
                    for c in most_available(problem.contribs.values()):
                        if c.name not in used_people:
                            contrib = c
                            used_people.add(c.name)
                            break
                    if contrib is not None:
                        print(f"[debug mentee] added a mentee with skill {skill} level {lvl-1}")
                        people_list[i] = contrib

def skill_up_people(people_list, project, problem):
    # Skill up people
    for idx, task in enumerate(project.tasks):
        skill, task_lvl = task
        contrib = people_list[idx]
        if skill not in contrib.skills:
            contrib.skills[skill] = 0
            problem.contributor_skills[skill][0] += [contrib]
        lvl = contrib.skills[skill]

        if lvl < 100 and (task_lvl >= lvl):
            # print("lvl up - ", contrib.name, skill, contrib.skills[skill])
            problem.contributor_skills[skill][lvl].remove(contrib)
            contrib.skills[skill] += 1
            problem.contributor_skills[skill][lvl+1].append(contrib)
            # print("lvl up + ", contrib.name, skill, contrib.skills[skill])

def naive(problem):
    remaining_projects = list(problem.projects.values())
    people = list(problem.contribs.values())

    from collections import Counter
    nb_tasks = Counter()
    projects = []

    sol = Solution()
    while len(remaining_projects) != len(projects):
        #projects = sort_by_score(remaining_projects)
        projects = sorted(remaining_projects, key= lambda p:  p.S/(p.D**2*p.R))[::-1]

        remaining_projects = []
        for project in projects:
            used_people = set()
            people_list = []
            
            add_people(people_list, used_people, project, problem)

            #add_mentees(people_list, used_people, project, problem)

            #print(people_list)
            if None not in people_list:
                # Add asignment
                sol.assignments.append((project.name,[x.name for x in people_list]))
                sol.nb_projects += 1

                # decrease future availability of that person (good?)
                for x in people_list:
                    nb_tasks[x.name] += 1

                skill_up_people(people_list, project, problem)
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
