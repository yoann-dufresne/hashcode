
class Contributor:
    def __init__(self, name, id):
        self.name = name
        self.id = id
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
