TEAM_FACTOR = 0.3
PTS_FACTOR = 1.0
REB_FACTOR = 1.2
AST_FACTOR = 1.5

class Player:
    def __init__(self, name, team, team_wins, pts, reb, ast):
        self.name = name
        self.team = team
        self.wins = int(team_wins)
        self.pts = float(pts)
        self.reb = float(reb)
        self.ast = float(ast)
        self.score = 0
        self.factor()

    def factor(self):
        self.score = TEAM_FACTOR * self.wins
        self.score += PTS_FACTOR * self.pts
        self.score += REB_FACTOR * self.reb
        self.score += AST_FACTOR * self.ast
