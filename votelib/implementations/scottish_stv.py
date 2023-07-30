from enum import Enum
from typing import List
from votelib.election import Ballot, Candidate


class State(Enum):
    elected = 1
    eliminated = 2
    hopeful = 3


class StvCandidate:
    def __init__(self, candidate: Candidate):
        self.name = candidate.name
        self.state = State.hopeful
        self.ballots = []

    @property
    def first_place_votes(self):
        return sum([b.value for b in self.ballots])


class StvBallot:
    def __init__(self, ballot: Ballot):
        self.rankings = ballot.rankings
        self.value = 1

    def get_next(self, candidates: List[StvCandidate]):
        """
            Removed the first ranking, then finds the next ranking 
            on the ballot for a candidate who is still hopeful. 
            Removes all candidates prior to that. 

            Returns the ranking, or None if the ballot is exhausted
        """
        done = False
        new_c = None
        while not done:
            if len(self.rankings) >= 2:
                self.rankings.pop(0)
                maybe_c = self.rankings[0]
                if candidates[maybe_c].state == State.hopeful:
                    new_c = maybe_c
                    done = True
            else:
                done = True
        return new_c


class ScottishSTVDroop():

    name = "Scottish STV w/ Droop Quota"

    def __init__(self, candidates: List[Candidate], ballots: List[Ballot], num_winners: int):
        self.candidates = {c.name: StvCandidate(c) for c in candidates}
        self.ballots = [StvBallot(b) for b in ballots]
        self.num_winners = num_winners
        self.cur_winners = 0

        self.quota = (len(self.ballots) / num_winners) + 1

    def setup(self):
        # assign ballots to their first place pick
        for b in self.ballots:
            if len(b.rankings) != 0:
                self.candidates[b.rankings[0]].ballots.append(b)

    def run(self):
        self.setup()

        while self.cur_winners <= self.num_winners:
            """
                Its possible to end up in a state where there are not enough 
                exhausted ballots left to make more winners. 
                
                Possible other similar conditions as well.
                
                Need a finish_up function which sets the correct
                amount of candidates with the highest scores as winners.
            """
            round()
            
    def round(self):
        """
            Complete one round of STV
        """
        winner = None
        for c in self.candidates:
            if c.first_place_votes >= self.quota:
                winner = c
                break
        if winner:
            winner(c)
        else:
            self.eliminate()

    def winner(self, candidate: str):
        """
            Transfer the surplus ballots for a winning candidate.
        """
        c = self.candidates[candidate]
        surplus = len(self.ballots) - self.quota
        transfer_value = surplus / len(self.ballots)
        for b in c.ballots[:]:
            nxt = b.get_next(self.candidates)
            if nxt:
                b.value = b.value * transfer_value
                self.candidates[nxt].ballots.append(b)
            c.ballots.remove(b)
        c.state = State.elected
        self.cur_winners = self.cur_winners + 1

    def eliminate(self):
        """
            Find the candidate with the least number 1 votes,
            transfer all of their ballots, and eliminate them.
        """
        c = min(self.candidates,
                key=lambda c: self.candidates[c].first_place_votes)

        for b in self.candidates[c].ballots[:]:
            nxt = b.get_next(self.candidates)
            if nxt:
                self.candidates[nxt].ballots.append(b)
            self.candidates[c].ballots.remove(b)
        self.candidates[c].state = State.eliminated

    def state(self):
        """
            Returns the current state of all candidates
        """
        return [
            {
                "name": c.name,
                "first_place_votes": c.first_place_votes,
                "state": c.state,
            }
            for c in self.candidates
        ]
