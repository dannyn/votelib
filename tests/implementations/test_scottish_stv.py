import unittest

from votelib.election import Ballot, Candidate
from votelib.implementations.scottish_stv import ScottishSTVDroop, StvBallot, StvCandidate, State


class TestStvCandidate(unittest.TestCase):
    def test_first_place(self):
        ballots = [
            StvBallot(Ballot(["c2", "c1", "c3"])),
            StvBallot(Ballot(["c2", "c2", "c3"])),
            StvBallot(Ballot(["c1", "c2", "c3"])),
        ]

        ballots[2].value = 0.5
        c = StvCandidate(Candidate("c1"))
        c.ballots = ballots

        self.assertEqual(c.first_place_votes, 2.5)


class TestStvBallot(unittest.TestCase):
    def test_get_next(self):
        b = StvBallot(Ballot(["c1", "c2", "c3", "c4"]))

        candidates = {
            "c1": StvCandidate(Candidate("c1")),
            "c2": StvCandidate(Candidate("c2")),
            "c3": StvCandidate(Candidate("c3")),
            "c4": StvCandidate(Candidate("c4"))
        }
        candidates["c2"].state = State.eliminated

        nxt = b.get_next(candidates)
        self.assertEqual(nxt, 'c3')
        self.assertEqual(b.rankings, ['c3', 'c4'])

        nxt = b.get_next(candidates)
        self.assertEqual(nxt, 'c4')
        self.assertEqual(b.rankings, ['c4'])

        b = StvBallot(Ballot(["c1"]))
        candidates = {
            "c1": StvCandidate(Candidate("c1")),
            "c2": StvCandidate(Candidate("c2")),
        }
        nxt = b.get_next(candidates)
        self.assertIsNone(nxt)


class TestScottishSTVDroop(unittest.TestCase):
    def test_quota(self):
        """
            Make sure the quota is calculated correctly
        """
        None

    def test_setup(self):
        candidates = [
            Candidate("c1"),
            Candidate("c2"),
            Candidate("c3"),
        ]
        ballots = [
            Ballot(["c2", "c1", "c3"]),
            Ballot(["c2", "c2", "c3"]),
            Ballot(["c3", "c3", "c1"]),
            Ballot(["c2", "c3", "c1"]),
            Ballot(["c1", "c2", "c3"]),
        ]

        e = ScottishSTVDroop(candidates, ballots, 2)
        e.setup()

        self.assertEqual(len(e.candidates['c1'].ballots), 1)
        self.assertEqual(len(e.candidates['c2'].ballots), 3)
        self.assertEqual(len(e.candidates['c3'].ballots), 1)

    def test_eliminate(self):
        candidates = [
            Candidate("c1"),
            Candidate("c2"),
        ]
        ballots = [
            Ballot(["c1", "c2"]),
            Ballot(["c1", "c2"]),
            Ballot(["c2", "c1"]),
            Ballot(["c1", "c2"]),
            Ballot(["c2"]),
        ]

        e = ScottishSTVDroop(candidates, ballots, 1)

        e.setup()
        e.eliminate()
        self.assertEqual(e.candidates['c2'].state, State.eliminated)
        self.assertEqual(len(e.candidates['c1'].ballots), 4)
        self.assertEqual(e.candidates['c1'].first_place_votes, 4)

        
    def test_transfer(self):
        candidates = [
            Candidate("c1"),
            Candidate("c2"),
            Candidate("c3"),
        ]
        ballots = [
            Ballot(["c1", "c2"]),
            Ballot(["c1", "c2"]),
            Ballot(["c1", "c3"]),
            Ballot(["c2", "c1"]),
        ]

        e = ScottishSTVDroop(candidates, ballots, 2)
        e.setup()
        
        e.winner("c1") 

        self.assertEqual(e.candidates["c1"].state, State.elected)
        self.assertEqual(len(e.candidates["c1"].ballots), 0)
        self.assertEqual(len(e.candidates["c2"].ballots), 3)
        self.assertEqual(len(e.candidates["c3"].ballots), 1)

