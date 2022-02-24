
class Contributor:
    def __init__(self, name, idx):
        self.name = name
        self.idx = idx
        self.skills = {}

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



class Solution:
    def __init__(self):
        self.nb_projects = 0
        self.assignments = []

    def __repr__(self):
        str = f"Sol: {self.nb_projects} projects: {self.assignments}"
        return str


    def parse(self, solution_filename):
        solution_file_lines = open(solution_filename).readlines()
        self.nb_projects = int(solution_file_lines[0])
        
        for i in range(len(solution_file_lines)-1):
            line = solution_file_lines[i+1].strip()
            if i % 2 == 0:
                project_name = line
            else:
                self.assignments += (project_name,line.split())

    
    def score(self, problem):
        day = 0
        current_projects = None
        occupations = dict()
        pending_projects = self.assignments.items()
        
        # loop over days
        while True:

            # start new projects
            new_pending_projects = []
            for p in pending_projects:
                contributors = problem.projects[p].contributors
                if all_available(contributors):
                    current_projects += [project]
                    for contributor in contributors:
                        occupations[contributor] = current_project.id
                else:
                    new_pending_projects += [project]
            pending_projects = new_pending_projects
            
            # advance current projects
            for project in current_projects:
                project.time_remaining -= 1
            
            # finish current projects
            new_current_projects = []
            for project in current_projects:
                if project.time_remaining == -1:
                    # free contributors
                    for contributor in project.contributors:
                        occupations[contributor] = None
                    # increase skills of contributor
                    for skill in project.skills:
                        for contributor in project.contributors:
                            if self.contrib.skill[skill] >= project.skills[skill]:
                                self.contrib.skill[skill] += 1
                else:
                    new_current_projects = project
            current_projects = new_current_projects

            # it's a new day
            day += 1
