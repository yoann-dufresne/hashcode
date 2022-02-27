from main import *
from solution import *

if __name__ == "__main__":
    problem = parse()

from functools import lru_cache 
@lru_cache(maxsize=None)
def try_add_people(used_people, project, problem):
    set_used_people = set(used_people)
    good = True
    # try adding people who have the required skills
    for skill, lvl in project.tasks:
        contrib = None
        for possible_contrib in problem.contributor_skills[skill][lvl:]:
            if len(possible_contrib) > 0:
                for c in most_available(possible_contrib):
                #for c in possible_contrib:
                    if c.name not in set_used_people:
                        contrib = c
                break
        if contrib is None:
            good = False
            break
    return good


# less naive greedy strategy: 
# sort problems
# then try to pack as problems at the same time given the availability of people
# then re-sort remaining problems, etc..

#@profile
def schedule_packing(problem):
    verbose = problem.verbose
    people = list(problem.contribs.values())

    from collections import Counter
    projects = []

    sol = Solution()
    day = 0

    current_projects = []
    time_remaining = {}
    total_time = {}
    project_scores = {}
    best_before = {}
    people_skills = {}
    final_score = 0
    max_day = 0
    project_done_by_best = 0
    project_done_after_best =  0
    all_proj_skills = {}
    available = set([c for c in problem.contribs])
    project_people = {}
    project_people_set = {}
    remaining_projects = []

    for project in problem.projects.values():
        total_time[project.name] = project.D
        project_scores[project.name] = project.S
        best_before[project.name] = project.B
        max_day = max(max_day, project.B*2+1)
        all_proj_skills[project.name] = project.skills
        remaining_projects += [project]

    for person in problem.contribs.values():
        people_skills[person.name] = dict(person.skills.items())
    
    remaining_projects = sorted(remaining_projects, key= lambda p:  p.S/(p.D**2*p.R))[::-1]
    #remaining_projects = sorted(remaining_projects, key= lambda p:  p.B)
    used_people = set()
    sorted_used_people= tuple()
    interesting_days = set([0])

    # loop over days
    while True:
        if day % 100 == 0:print("assigning day",day)
        if len(remaining_projects) == 0 and len(current_projects) == 0 or day > max_day: break

        # finish current projects
        if day in interesting_days:
            new_current_projects = []
            for project_name in current_projects:
                if time_remaining[project_name] == 0:
                    # free contributors
                    people_set = project_people_set[project_name]
                    used_people -= people_set
                    #sorted_used_people = tuple(sorted(list(used_people)))
                    # skill them up
                    people = project_people[project_name]
                    project = problem.projects[project_name]
                    skill_up_people(people, project, problem)
                    project_skills = all_proj_skills[project_name]
                    # calculate score
                    if day < best_before[project_name]:
                        points = project_scores[project_name]
                        project_done_by_best += 1
                        if verbose: print("[debug greedy score]",project_name,"done on time",day,"before",best_before[project_name],"points",points,"total so far",final_score)
                    else:
                        project_done_after_best += 1
                        points = max(0,project_scores[project_name]-1-(day-best_before[project_name]))
                        if verbose: print("[debug greedy score]", project_name,"done after time",day,"before",best_before[project_name],"points",points,"total so far",final_score)
                    final_score += points
                else:
                    new_current_projects += [project_name]
            current_projects = new_current_projects

        # maybe start new projects
        new_remaining_projects = []
        if day in interesting_days:
            for project in remaining_projects:
                project_name = project.name
                project = problem.projects[project.name]
                
                # attempt at optimizing this slow function
                #res = try_add_people(sorted_used_people, project, problem)
                #if res:
                if True:
                    test_used_people = used_people.copy()
                    mentoring = False 
                    if mentoring:
                        people_list = add_people(test_used_people, project, problem,stop_early=False)
                        add_mentees(people_list, test_used_people, project, problem)
                    else:
                        people_list = add_people(test_used_people, project, problem)
                #else:
                #    people_list = [None]


                if None not in people_list:
                    used_people = test_used_people
                    #sorted_used_people = tuple(sorted(list(used_people)))
                    if verbose: print(f"[debug greedy] {project_name} assigned! day {day} with {len(people_list)} people")
                    current_projects += [project_name]
                    interesting_days.add(day+total_time[project_name])
                    time_remaining[project_name] = total_time[project_name]
                    project_people_set[project_name] = set([x.name for x in people_list])
                    project_people[project_name] = people_list[:] 
                    assert(len(people_list) == len(project.tasks))

                    # Add asignment
                    sol.assignments.append((project.name,[x.name for x in people_list]))
                    sol.nb_projects += 1

                    # gather stats on the person for future choices
                    for p in people_list:
                        p.nb_tasks += 1
                        p.last_task = sol.nb_projects

                else:
                    # if not, it goes back to the list of pending projects
                    #print(f"[debug scorer] day {day}: incompatible project {project_name}")
                    new_remaining_projects += [project]
            remaining_projects = new_remaining_projects
            
        # advance time in current projects
        for project_name in current_projects:
            time_remaining[project_name] -= 1

        # it's a new day
        day += 1
        
    return sol

