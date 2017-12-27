from cs1graphics import Canvas, Circle, Point
import time
import copy

    

class BallWrapper(Circle):
    def __init__(self,x,y,vx,vy,radius=15):
        Circle.__init__(self)
        self._ball = Ball(x, y, vx, vy)
        self._radius = radius
        self.moveTo(self._ball.getPositionX(),self._ball.getPositionY())
        self.setRadius(radius)
        self.setFillColor("green")

    def advance(self,world):
        self._ball.advance(world)
        newx,newy = self._ball.getPositionX(),self._ball.getPositionY()
        radius = self._radius
        self.moveTo(newx,newy)
        # check to see if we should remove it from world
        if (newx+radius < 0.0 or 
            newx-radius > world.getWidth() or 
            newy+radius < 0.0 or 
            newy-radius > world.getHeight()):
            world.remove(self)

class Star(Circle):
    def __init__(self,x,y,mass,radius=8):
        Circle.__init__(self, radius, Point(x,y))
        self.setFillColor("red")
        self._mass = mass

    def getMass(self):
        return self._mass

    def getPositionX(self):
        return self.getReferencePoint().getX()
    
    def getPositionY(self):
        return self.getReferencePoint().getY()
    
    def advance(self,world):
        pass

class World:

    def __init__(self,width=500,height=400,color="white",title="Simulated World"):
        self._canvas = Canvas(width,height,color,title)
        self._canvas.setAutoRefresh(False)
        self._star = None
        self._controller = None
        self._timestamp = 0

    def getWidth(self):
        return self._canvas.getWidth()

    def getHeight(self):
        return self._canvas.getHeight()

    def setController(self,controller):
        self._controller = controller
        
    def getGravity(self):
        if self._controller:
            return self._controller.getGravity()
        else:
            return 0.0

    def getStar(self):
        return self._star

    def _setStar(self,star):
        if (self._star):
            self._canvas.remove(star)
        self._star = star
        star.setDepth(0)
        self._canvas.add(star)
        self._canvas.refresh()

    def add(self,updatable):
        try:
            updatable.advance        # note this is not a call, just a check to see if advance exists
        except:
            raise StandardError, "You may only add objects which support an appropriate 'advance' method"
        self._timestamp += 1
        updatable.setDepth(self._timestamp)
        self._canvas.add(updatable)
        self._canvas.refresh()

    def remove(self, obj):
        self._canvas.remove(obj)
               
    def numObj(self):
        return len(self._canvas.getContents())
    
    def _mainloop(self):

        more = True
        while more:
#            global debug
#            if debug:
#                print "within world's mainloop"
            objects = self._canvas.getContents()   # latest list of objects
            for obj in objects:
                obj.advance(self)
            self._canvas.refresh()
            if self._controller:
                more = self._controller.processDelay(self)
        
class SimpleController:
    DEFAULT_WIDTH = 500
    DEFAULT_HEIGHT = 400
    DEFAULT_DELAY = 0.01
    DEFAULT_GRAV = 0.05
    DEFAULT_STARMASS = 1000
    DEFAULT_EXTRA = "n"
    DEFAULT_SEQUENCE = 1
    DEFAULT_SEQUENCEGAP = 5

    # should be class method
    def inputDefault(self,question,defVal,convert,validity):
        invalidMsg = False;
        print question,"(default %s):"%defVal,
        line = raw_input()
        try:
            result = eval(convert)
            if not eval(validity):
                result = defVal
                invalidMsg = True
        except:
            result = defVal
            if line !="":
                invalidMsg = True

        if invalidMsg:
            print "Invalid entry: %s.  Using default %s instead" % (line,defVal)

        return result

    def __init__(self):

        print """Welcome to our simulator.
Throughout this program we will offer default responses
with each question.  If you wish to accept the default,
you may simply enter return.  Now let's begin.
"""

        print "First, we must set the dimension of our world."

        width = self.inputDefault(
            "What width would you like?",SimpleController.DEFAULT_WIDTH,
            "int(line)","result > 0")

        height = self.inputDefault(
            "What height would you like?",SimpleController.DEFAULT_HEIGHT,
            "int(line)","result > 0")

        print """
Next we must decide what type of world.
The standard world has uniform, vertical gravity.
An extra credit world has gravity based upon a star.
"""
        extra = self.inputDefault(
            "Would you like the extra credit version?",SimpleController.DEFAULT_EXTRA,
            "line.strip()[0]","result in ['Y','y','N','n']")
        extra = extra in ['Y','y']

        if extra:
            self._gravity = 0.0
            mass = self.inputDefault(
                "What mass does the star have?",SimpleController.DEFAULT_STARMASS,
                "float(line)","True")
        else:
            self._gravity = self.inputDefault(
                "What gravity value would you like?",SimpleController.DEFAULT_GRAV,
                "float(line)","True")

        self._delay = self.inputDefault(
            "What delay value would you like?",SimpleController.DEFAULT_DELAY,
            "float(line)","result>=0.0")


        world = self._world = World(width,height)
        if extra:
           world._setStar(Star(width/2.0,height/2.0,mass))

        print "The world has been successfully created"

        done = False
        while not done:
            more = self.inputDefault(
                "\nWould you like to add a sequence of balls?",'y',
                "line.strip()[0]","result in ['Y','y','N','n']")
            done = more in ['n','N']
            if not done:
                defx = width/4.0
                if extra: defx*=2.0
                x = self.inputDefault(
                    "Enter X coordinate of initial position",defx,
                    "float(line)","True")
                
                defy = height*0.8
                y = self.inputDefault(
                    "Enter Y coordinate of initial position",defy,
                    "float(line)","True")

                defvx = width*.005
                if extra: defvx *= .8
                vx = self.inputDefault(
                    "Enter X coordinate of initial velocity",defvx,
                    "float(line)","True")

                if extra: defvy = 0.0
                else:     defvy = -height*.0125
                vy = self.inputDefault(
                    "Enter Y coordinate of initial velocity",defvy,
                    "float(line)","True")

                self._moreballs = self.inputDefault(
                    "How many such balls would you like released in this sequence?",
                    SimpleController.DEFAULT_SEQUENCE,"int(line)","result > 0")

                self._seqcount = 0

                def factory():
                    return BallWrapper(x,y,vx,vy)
                self._factory = factory
                world.setController(self)
                world._mainloop()
        print "Goodbye"
                
    
    def processDelay(self,w):
        time.sleep(self._delay)
        if (self._moreballs>0 and self._seqcount==0):
            w.add(self._factory())
            self._moreballs -= 1
        self._seqcount = (self._seqcount+1)%self.DEFAULT_SEQUENCEGAP
        base = 0
        if (w.getStar()): base+=1
        return (w.numObj()>base)

    def getGravity(self):
        return self._gravity

    
if __name__ == "__main__":
    from Ball import Ball
    control = SimpleController()
