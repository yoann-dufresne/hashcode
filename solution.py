
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
        self.contribs = []
        self.projects = []

class Solution:
    def __init__(self):
        pass

    def __repr__(self):
        return ""
