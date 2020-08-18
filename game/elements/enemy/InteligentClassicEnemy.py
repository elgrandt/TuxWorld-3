import enemy
import load_data.images as img

class InteligentClassicEnemy(enemy.LimitsEnemy,enemy.enemy4Player):
    def __init__(self,x,y,Range=2,Limits=None):
        self.init(x, y, img.ClassicEnemy)
        self.startEnemy4Player()
        self.SetLimits(Limits)
        self.SetDirection(enemy.Directions.RANDOM)
        self.SetForce(1)
        self.setType("Classic enemy")
        self.SetSpeed(4)

        attack = {"type":enemy.AttackRanges.CIRCLE,"radius":500}

        self.setAttackRange(attack)

    def handleSearching(self,angle,distance):
        self.setInitialAngle(angle)
