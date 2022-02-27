from solution import *
from sys import stdin, stderr, argv
from operator import itemgetter
import greedy


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
    #return sorted(list_people, key=lambda x: x.nb_tasks)[::-1]
    return sorted(list_people, key=lambda x: x.last_task)[::-1]

def sort_above_lvl(people,skill,lvl, used_people):
    res = [(c.skills[skill],c) for c in people \
                               if skill in c.skills and c.skills[skill] >= lvl \
                                                    and c.name not in used_people]
    return [x[1] for x in sorted(res)]

def add_people(used_people, available_people, project, problem,stop_early=True):
    people_list = []
    # try adding people who have the required skills
    has_someone = False
    needs_someone = False
    for skill, lvl in project.tasks:
        contrib = None
        #for c in sort_above_lvl(available_people,skill,lvl, used_people): #good idea but 2slow
        for possible_contrib in problem.contributor_skills[skill][lvl:]:
            if len(possible_contrib) > 0:
                for c in most_available(possible_contrib):
                #for c in possible_contrib:
                    if c.name not in used_people:
                        contrib = c
                        used_people.add(c.name)
                        has_someone = True
                        break
                if contrib is not None: break
        people_list.append(contrib)
        if stop_early and contrib is None: break
        if contrib is None: needs_someone = True

    return people_list, has_someone, needs_someone

 
# mentorship program
# Input: a list of people (people_list) assigned to project
#        which may contain None entries, i.e. a skill was unfilled.
# Output: a augmented list with people who will be mentored.

def add_mentees(people_list, used_people, available_people, project, problem):
    # determine what skills are already available in the input list
    can_mentor = set()
    needs_someone = False
    mentees_added = 0
    has_skill = {}
    for contrib in people_list:
        if contrib is not None:
            for skill in contrib.skills:
                if skill not in has_skill:
                    has_skill[skill]=0
                else: 
                    has_skill[skill]=max(has_skill[skill],contrib.skills[skill])
    for j,x in enumerate(project.tasks):
        skill, lvl  = x
        if skill in has_skill and has_skill[skill] >= lvl:
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
                            mentees_added += 1
                            used_people.add(c.name)
                            break
                    if contrib is not None: break
                if contrib is not None:
                    #print(f"[debug mentee] added a mentee with skill {skill} level {lvl-1}")
                    people_list[i] = contrib
    # finally, retry by adding anyone with a pulse ;) when a needed mentored skill has level 1
    for i,x in enumerate(project.tasks):
        skill, lvl = x
        contrib = people_list[i]
        if lvl == 1:
            if contrib is None:
                if i in can_mentor:
                    for c in most_available(problem.contribs.values()):
                        if c.name not in used_people:
                            contrib = c
                            mentees_added += 1
                            used_people.add(c.name)
                            break
                    if contrib is not None:
                        #print(f"[debug mentee] added a mentee with skill {skill} level {lvl-1}")
                        people_list[i] = contrib
        if contrib is None: needs_someone = True
    return mentees_added, needs_someone

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

# naive greedy strategy: 
# sort problems
# then sort people for those problems

def naive(problem):
    remaining_projects = list(problem.projects.values())
    people = list(problem.contribs.values())

    from collections import Counter
    projects = []

    sol = Solution()
    while len(remaining_projects) != len(projects):
        #projects = sort_by_score(remaining_projects)
        #projects = sorted(remaining_projects, key= lambda p:  p.B)[::-1]
        projects = sorted(remaining_projects, key= lambda p:  p.S/(p.D**2*p.R))[::-1]

        remaining_projects = []
        for project in projects:
            used_people = set()
            
            mentoring = False 
            if mentoring:
               people_list, has_someone, needs_someone = add_people(used_people, project, problem,stop_early=False)
               if has_someone and needs_someone:
                   add_mentees(people_list, used_people, project, problem)
            else:
               people_list, osef, osef = add_people(used_people, project, problem)

            #print(people_list)
            if None not in people_list:
                # Add asignment
                sol.assignments.append((project.name,[x.name for x in people_list]))
                sol.nb_projects += 1

                # gather stats on the person for future choices
                for p in people_list:
                    p.nb_tasks += 1
                    p.last_task = sol.nb_projects

                skill_up_people(people_list, project, problem)
            else:
                remaining_projects.append(project)

    return sol


if __name__ == "__main__":
    problem = parse()
    
    problem.verbose = "--verbose" in argv

    if "--naive" in argv:
        solution = naive(problem)
    else: 
        solution = greedy.schedule_packing(problem)

    solution.print()
    solution.print(stderr)
    if "--score" in argv:
        print(solution.score(problem))
