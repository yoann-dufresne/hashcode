from sys import stdout


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
        self.contributors = []
        self.tasks = []
        self.skills = {}

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
            print(skill, "".join(f"{self.contributor_skills[skill][l]}" for l in range(101)))



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
            print(" ".join(x for x in assignment), file=stream)


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
        occupations = dict()
        pending_projects = self.assignments[:]
        time_remaining = {}
        total_time = {}
        project_scores = {}
        best_before = {}
        people_skills = {}
        final_score = 0

        for project in problem.projects.values():
            total_time[project.name] = project.D
            project_scores[project.name] = project.S
            best_before[project.name] = project.B

        for person in problem.contribs.values():
            people_skills[person.name] = dict(person.skills.items())

        def all_available(people, occupations):
            return all([p not in occupations or occupations[p] is None for p in people])

        # loop over days
        while True:
            if len(pending_projects) == 0 and len(current_projects) == 0: break
            print(pending_projects,"pending")

            # start new projects
            new_pending_projects = []
            for project_name, people in pending_projects:
                if all_available(people, occupations):
                    current_projects += [project_name]
                    for person_name in people:
                        occupations[person_name] = project_name
                    time_remaining[project_name] = total_time[project_name]
                else:
                    new_pending_projects += [(project_name, people)]
            pending_projects = new_pending_projects
            
            # advance current projects
            for project_name in current_projects:
                time_remaining[project_name] -= 1
            
            # finish current projects
            new_current_projects = []
            for project_name in current_projects:
                if time_remaining[project_name] == 0:
                    # free contributors
                    project_skills = [p.skills for p in problem.projects.values() if p.name == project_name][0]
                    for person_name in occupations:
                        if occupations[person_name] == project_name:
                            occupations[person_name] = None
                        # increase skills of contributor
                        for skill in project_skills:
                            if skill not in people_skills[person_name]:
                                people_skills[person_name][skill] = 0
                            if people_skills[person_name][skill] >= project_skills[skill]:
                                people_skills[person_name][skill] += 1
                    # calculate score
                    if day < best_before[project_name]:
                        final_score += project_scores[project_name]
                    else:
                        final_score += max(0,project_scores[project_name]-1-(day-best_before[project_name]))
                else:
                    new_current_projects += [project_name]
            current_projects = new_current_projects

            # it's a new day
            day += 1
        return final_score
