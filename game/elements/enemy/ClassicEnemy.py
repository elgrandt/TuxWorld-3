import enemy
import load_data.images as img

class ClassicEnemy(enemy.LimitsEnemy):
    def __init__(self,x,y,Direction="Random",Limits=None):
        self.init2(x, y, img.ClassicEnemy, Limits)
        self.SetDirection(Direction)
        self.SetForce(1)
        self.setType("Classic enemy")