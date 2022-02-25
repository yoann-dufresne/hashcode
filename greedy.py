from main import *
from solution import *

if __name__ == "__main__":
    problem = parse()

# less naive greedy strategy: 
# sort problems
# then try to pack as problems at the same time given the availability of people
# then re-sort remaining problems, etc..

def schedule_packing(problem):
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
    
    #remaining_projects = sorted(remaining_projects, key= lambda p:  p.S/(p.D**2*p.R))[::-1]
    remaining_projects = sorted(remaining_projects, key= lambda p:  p.B)
    used_people = set()

    # loop over days
    while day < 6000: #FIXME: know when to stop
        if day % 1 == 0:print("assigning day",day)
        if len(remaining_projects) == 0 and len(current_projects) == 0 or day > max_day: break

        # maybe start new projects
        new_remaining_projects = []
        for project in remaining_projects:
            project_name = project.name
            people_list = []
            project = problem.projects[project.name]
            
            test_used_people = set(used_people)
            add_people(people_list, test_used_people, project, problem)

            add_mentees(people_list, used_people, project, problem)

            if None not in people_list:
                used_people = test_used_people
                print("[debug greedy]",project_name,"assigned! day",day,"with people",people_list)
                current_projects += [project_name]
                time_remaining[project_name] = total_time[project_name]
                project_people_set[project_name] = set([x.name for x in people_list])
                project_people[project_name] = people_list[:] 
                assert(len(people_list) == len(project.tasks))

                # Add asignment
                sol.assignments.append((project.name,[x.name for x in people_list]))
                sol.nb_projects += 1

                # gather stats on the person for future choices
                for x in people_list:
                    x.nb_tasks += 1
                    x.last_task = sol.nb_projects

            else:
                # if not, it goes back to the list of pending projects
                #print(f"[debug scorer] day {day}: incompatible project {project_name}")
                new_remaining_projects += [project]
        remaining_projects = new_remaining_projects
        
        # advance time in current projects
        for project_name in current_projects:
            time_remaining[project_name] -= 1
        
        # finish current projects
        new_current_projects = []
        for project_name in current_projects:
            if time_remaining[project_name] == 0:
                # free contributors
                people_set = project_people_set[project_name]
                used_people -= people_set
                # skill them up
                people = project_people[project_name]
                project = problem.projects[project_name]
                skill_up_people(people, project, problem)
                project_skills = all_proj_skills[project_name]
                for i,person_name in enumerate(people):
                    # increase skills of contributor
                    skill, lvl = project_skills[i]
                    if person_name not in people_skills:
                        people_skills[person_name] = {}
                    if skill not in people_skills[person_name]:
                        people_skills[person_name][skill] = 0
                    if people_skills[person_name][skill] >= lvl:
                        people_skills[person_name][skill] += 1
                # calculate score
                if day < best_before[project_name]:
                    points = project_scores[project_name]
                    project_done_by_best += 1
                    print("[debug greedy score]",project_name,"done on time",day,"before",best_before[project_name],"points",points,"total so far",final_score)
                else:
                    project_done_after_best += 1
                    points = max(0,project_scores[project_name]-1-(day-best_before[project_name]))
                    print("[debug greedy score]", project_name,"done after time",day,"before",best_before[project_name],"points",points,"total so far",final_score)
                final_score += points
            else:
                new_current_projects += [project_name]
        current_projects = new_current_projects

        # it's a new day
        day += 1
        
    return sol

