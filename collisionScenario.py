#File: collisions.py:

def collisionScenario(fish1,fish2,fish3,roundFish):

    if roundFish.getAlive() == True:

        fishList = []

        if roundFish == fish1:
            if fish2.getAlive() == True:
                fishList.append(fish2)
            if fish3.getAlive() == True:
                fishList.append(fish3)
        elif roundFish == fish2:
            if fish1.getAlive() == True:
                fishList.append(fish1)
            if fish3.getAlive() == True:
                fishList.append(fish3)
        elif roundFish == fish3:
            if fish1.getAlive() == True:
                fishList.append(fish1)
            if fish2.getAlive() == True:
                fishList.append(fish2)

        for collideFish in fishList:

            if roundFish.getX() == collideFish.getX() and roundFish.getY() == collideFish.getY():

                if roundFish.getFlee() == True:
                    collideMove(roundFish)
                else:
                    roundFish.move(-1)

    
