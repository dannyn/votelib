from typing import List



class Candidate:
    def __init__(self, name: str):
       self.name = name 


class Ballot:
    def __init__(self, rankings: List[str], weights=None):
        self.rankings = rankings 
        self.weights = weights


class Election:
    def __init__(self, candidates: List[str], ballots: List[Ballot], num_winners: int):
        self.candidates = candidates
        self.ballots = ballots
        self.num_winners = num_winners
