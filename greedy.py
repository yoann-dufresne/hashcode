from main import *
from solution import *

if __name__ == "__main__":
    problem = parse()

def finish_current_projects(day, current_projects, time_remaining, used_people, problem, project_people, project_people_set, final_score, verbose=False):
    new_current_projects = []
    points = 0
    for project_name in current_projects:
        if time_remaining[project_name] == 0:
            # free contributors
            people_set = project_people_set[project_name]
            used_people -= people_set
            # restore visibility of that contributor in contributor_skills
            for c in problem.contribs.values():
                if c.name not in people_set: continue
                for skill, lvl in c.skills.items():
                    problem.contributor_skills[skill][lvl].append(c)
            # skill them up
            people = project_people[project_name]
            project = problem.projects[project_name]
            skill_up_people(people, project, problem)
            # calculate score
            if day < project.B:
                points += project.S
                if verbose: print("[score preview]",project_name,"done on time",day,"before",project.B,"points",points,"total so far",final_score)
            else:
                points += max(0,project.S-1-(day-project.B))
                if verbose: print("[score preview]", project_name,"done after time",day,"before",project.B,"points",points,"total so far",final_score)
        else:
            new_current_projects += [project_name]
    current_projects = new_current_projects
    return points


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
    project_scores = {}
    final_score = 0
    max_day = 0
    project_people = {}
    project_people_set = {}
    remaining_projects = []

    for project in problem.projects.values():
        max_day = max(max_day, project.B+project.S+1)
        remaining_projects += [project]

    #remaining_projects = sorted(remaining_projects, key= lambda p:  p.S/(p.D**2*p.R))[::-1]
    #remaining_projects = sorted(remaining_projects, key= lambda p:  p.S/(p.D*p.R))[::-1]
    #remaining_projects = sorted(remaining_projects, key= lambda p:  p.B)
    remaining_projects = sorted(remaining_projects, key= lambda p:  p.S)
    #remaining_projects = sorted(remaining_projects, key= lambda p:  p.mean_lvl)
    #remaining_projects = sorted(remaining_projects, key= lambda p:  p.max_lvl)[::-1]
    used_people = set()
    interesting_days = set([0])
    nb_people_total = len(problem.contribs)

    # loop over days
    while True:
        if day % 100 == 0:print("assigning day",day)
        if len(remaining_projects) == 0 and len(current_projects) == 0 or day > max_day: break

        # finish current projects
        if day in interesting_days:
            points = finish_current_projects(day, current_projects, time_remaining, used_people, problem,\
                                             project_people, project_people_set, final_score, verbose)
            final_score += points

        # maybe start new projects
        new_remaining_projects = []
        if day in interesting_days:
            for project in remaining_projects:
                project_name = project.name
                project = problem.projects[project.name]
               
                # heuristic to not even try to assign anyone if we're short staffed anyway
                if len(project.tasks) > nb_people_total - len(used_people):
                    needs_someone = True
                else:
                    mentees_added = 0
                    test_used_people = used_people.copy()
                    mentoring = False 
                    if mentoring:
                        people_list, has_someone, needs_someone = add_people(test_used_people, project, problem, stop_early=False)
                        if has_someone and needs_someone:
                            mentees_added, needs_someone = add_mentees(people_list, test_used_people, project, problem)
                    else:
                        people_list, has_someone, needs_someone = add_people(test_used_people, project, problem)

                if needs_someone is False:
                    used_people = test_used_people
                    # disable visibility of that contributor in skills
                    for c in people_list:
                        if c is None: continue
                        for skill, lvl in c.skills.items():
                            problem.contributor_skills[skill][lvl].remove(c)
                    #sorted_used_people = tuple(sorted(list(used_people)))
                    if verbose: print(f"[greedy] {project_name} assigned! day {day} with {len(people_list)} people" + (f" ({mentees_added} mentees)" if mentees_added>0 else "") + f" [{len(problem.contribs)-len(used_people)} people available, {len(remaining_projects)} projects in pile]")
                    current_projects += [project_name]
                    interesting_days.add(day+project.D)
                    time_remaining[project_name] = project.D
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
                    if project.B + project.S > day+project.D : # discard expired projects
                        new_remaining_projects += [project]
                    #print(f"[debug scorer] day {day}: incompatible project {project_name}")
            remaining_projects = new_remaining_projects
            
        # advance time in current projects
        for project_name in current_projects:
            time_remaining[project_name] -= 1

        # it's a new day
        day += 1
        
    print("solution done, score",final_score)
    return sol

