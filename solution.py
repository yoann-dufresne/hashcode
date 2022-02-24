from sys import stdout, stderr


class Contributor:
    def __init__(self, name, idx):
        self.name = name
        self.idx = idx
        self.skills = {}

    def __repr__(self):
        return self.name

class Project:
    def __init__(self, name, idx, D, S, B, R):
        self.name = name
        self.idx = idx
        self.D = D
        self.S = S
        self.B = B
        self.R = R
        self.tasks = []
        self.skills = []

class Problem:
    def __init__(self, C, P):
        self.C = C
        self.P = P
        self.contribs = {}
        self.projects = {}
        self.contributor_skills = {}

    def add_contrib(self, contributor):
        self.contribs[contributor.name] = contributor
        for skill in contributor.skills:
            # New skill
            if skill not in self.contributor_skills:
                self.contributor_skills[skill] = [[] for _ in range(101)]
            # level add
            lvl = contributor.skills[skill]
            self.contributor_skills[skill][lvl].append(contributor)



class Solution:
    def __init__(self):
        self.nb_projects = 0
        self.assignments = []

    def __repr__(self):
        str = f"Sol: {self.nb_projects} projects: {self.assignments}"
        return str

    def print(self, stream=stdout):
        print(len(self.assignments), file=stream)
        for assignment in self.assignments:
            print(assignment[0], file=stream)
            print(" ".join(x for x in assignment[1]), file=stream)
    
    def write(self, out_filename):
        g = open(out_filename,"w")
        g.write(str(len(self.assignments))+"\n")
        for assignment in self.assignments:
            g.write(assignment[0]+"\n")
            g.write(" ".join(x for x in assignment[1])+"\n")
        g.close()
 

    def parse(self, solution_filename):
        solution_file_lines = open(solution_filename).readlines()
        self.nb_projects = int(solution_file_lines[0])
        
        for i in range(len(solution_file_lines)-1):
            line = solution_file_lines[i+1].strip()
            if i % 2 == 0:
                project_name = line
            else:
                self.assignments += [(project_name,line.split())]

    
    def score(self, problem):
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
        next_project = {}

        for project in problem.projects.values():
            total_time[project.name] = project.D
            project_scores[project.name] = project.S
            best_before[project.name] = project.B
            max_day = max(max_day, project.B*2+1)
            all_proj_skills[project.name] = project.skills

        pending_projects = []
        for project_name, people in self.assignments:
            project_people[project_name] = people
            project_people_set[project_name]= set(people)
            pending_projects += [project_name]
            for p in people:
                if p not in next_project:
                    next_project[p] = []
                next_project[p] += [project_name]

        for person in problem.contribs.values():
            people_skills[person.name] = dict(person.skills.items())

        # loop over days
        while True:
            if day % 10000 == 0:print("scoring day",day)
            if len(pending_projects) == 0 and len(current_projects) == 0 or day > max_day: break

            # start new projects
            new_pending_projects = []
            for project_name in pending_projects:
                #print(f"[debug scorer] day {day} testing project {project_name}")
                compatible = True
                project_skills = all_proj_skills[project_name]
                if not project_people_set[project_name].issubset(available):
                    compatible = False
                if compatible:
                    people = project_people[project_name]
                    for i,p in enumerate(people):
                        skill, needed_lvl = project_skills[i] 
                        if people_skills[p][skill] < needed_lvl:
                            compatible = False
                            break
                        if project_name != next_project[p][0]:
                            compatible = False
                            break
                if compatible:
                    current_projects += [project_name]
                    time_remaining[project_name] = total_time[project_name]
                    available -= project_people_set[project_name]
                else:
                    #print(f"[debug scorer] day {day}: incompatible project {project_name}")
                    new_pending_projects += [project_name]
            pending_projects = new_pending_projects
            
            # advance current projects
            for project_name in current_projects:
                time_remaining[project_name] -= 1
            
            # finish current projects
            new_current_projects = []
            for project_name in current_projects:
                if time_remaining[project_name] == 0:
                    # free contributors
                    people = project_people_set[project_name]
                    available |= people
                    project_skills = all_proj_skills[project_name]
                    for i,person_name in enumerate(people):
                        # increase skills of contributor
                        skill, lvl = project_skills[i]
                        if skill not in people_skills[person_name]:
                            people_skills[person_name][skill] = 0
                        if people_skills[person_name][skill] >= lvl:
                            people_skills[person_name][skill] += 1
                        next_project[person_name] = next_project[person_name][1:]
                    # calculate score
                    if day < best_before[project_name]:
                        points = project_scores[project_name]
                        project_done_by_best += 1
                        print("[debug score]",project_name,"done on time",day,"before",best_before[project_name],"points",points)
                    else:
                        project_done_after_best += 1
                        points = max(0,project_scores[project_name]-1-(day-best_before[project_name]))
                        print("[debug score]", project_name,"done after time",day,"before",best_before[project_name],"points",points)
                    final_score += points
                else:
                    new_current_projects += [project_name]
            current_projects = new_current_projects

            # it's a new day
            day += 1
        verbose=True
        if verbose:
            print(f"solution calculated, {project_done_by_best} projects done before best, {project_done_after_best} after")
        return final_score
