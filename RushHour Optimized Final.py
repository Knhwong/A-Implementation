import copy
import heapq

#Kin Hei Wong

#HEURISTIC METHODS ARE LOCATED WITHIN GAMESTATE METHODS!!!
#HEURISTIC METHODS ARE LOCATED WITHIN GAMESTATE METHODS!!!
#HEURISTIC METHODS ARE LOCATED WITHIN GAMESTATE METHODS!!!
#HEURISTIC METHODS ARE LOCATED WITHIN GAMESTATE METHODS!!!
#HEURISTIC METHODS ARE LOCATED WITHIN GAMESTATE METHODS!!!
#HEURISTIC METHODS ARE LOCATED WITHIN GAMESTATE METHODS!!!

#MINI MAP 
# 1) CLASS METHODS
# 2) MAIN CORE CODE (DRIVER, SEARCH, GENERATENEWSTATES)
# 3) MOVEMENT OPERATORS
# 4) PRINTING/MISC METHODS
# 5) FINDING VEHICLES METHODS

#I feel that utilising multiple arrays gets messy, so instead we use objects to record the location of a vehicle, and store it in a list within a larger GameState class.
class Vehicle :
    def __init__(self,x,y,length,char,orientation):
        self.x = x 
        self.y = y
        self.length = length 
        self.char = char
        self.orientation = orientation 
        # X and Y is always the "head", that which length pulls from.
        # Orientation 

    #Operator Overload so we can compare class object to characters in parsing
    def __eq__(self, key):
        if key == self.char:
            return True
        else:
            return False


#WE USE THIS GLOBAL VARIABLE TO EASILY SWITCH BETWEEN BLOCK AND IMPROVED HEURISTIC. 
#I KNOW GLOBAL VARIABLES ARE A BAD PRACTICE AND I PROMISE I WILL NOT USE THEM IN ACTUAL WORK
#THIS IS A HW ASSIGNMENT OF LIMITED COMPLEXITY THUS A USE OF A SINGLE GLOBAL VARIABLE FOR A SINGLE METHOD IS OK
heuristic = True

#Represents one possible game state. We use a class as we need to encapsulate vehicles with corresponding GameMatrix, and using two lists is messy.
#Also parent pointer is used for backtracking to build path later on.
class GameState:
    def __init__(self, GameMatrix,g, Vehicles,Parent):
        self.GameMatrix = GameMatrix
        self.g = g + 1
        self.Vehicles = Vehicles
        self.Parent = Parent
        self.X = self.findX()
        self.f = self.g + self.h()

    def h(self):
        if heuristic:
            return self.hblock()
        else:
            return self.himproved()
    #BLOCK HEURISTIC
    def hblock(self):
        h = 0
        if self.GameMatrix[2][5] != 'X':
            h = 1
            for i in range(len(self.GameMatrix)):
                if (self.GameMatrix[2][i] != '-' and self.GameMatrix[2][i] != 'X'):
                    h = h + 1
        return h
    
    #IMPROVED HEURISTIC
    #We improve the heuristic by encouraging the movement of blocking vertical 3-length vehicles downwards, along with encouragement of move x forwards.
    #For HW input, all states explored were optimal. 11964 States in 18 seconds for worst test case.
    def himproved(self):
        h = 0
        
        #Move block forward
        for v in self.Vehicles:
            if v.orientation%2:
                if (v.x >= self.X.x + self.X.length):
                    h = h + (3-v.y)
                if (v.y < 3 and self.GameMatrix[v.y+v.length][v.x] != '-'):
                    h = h + 1

        #Move x forward. We multiply by 2 to attach greater weight to moving x.
        h =  h + 2*(5-self.X.x)
        return h
    

    
    def findX(self):
        for i in self.Vehicles:
            if i.char == "X":
                return i
 
    #OVERLOADED COMPARISON OPERATORS FOR SORTING OF GAMESTATE BY F
    def __lt__(self, key):
        return self.f < key.f
    def __le__(self,key):
        return self.f <= key.f
    def __gt__(self, key):
        return self.f > key.f
    def __ge__(self,key):
        return self.f >= key.f

#{MAIN DRIVER CODE, RUN THIS FUNCTION!}
#RUN THIS CODE!
#RUN THIS CODE! 
#RUN THIS CODE!
#RUN THIS CODE!
def RushHour(h,input):
    global heuristic
    if (h == 1):
        heuristic = False
    FirstState = GameState(StringtoMatrix(input),0, FindVehicles(input), None)
    Path = Search(FirstState)
    Printing(Path)
#RUN THIS CODE!
#RUN THIS CODE!
#RUN THIS CODE!
#RUN THIS CODE!



#Conversions
def StringtoMatrix(input):
    Matrix = []
    for i in input:
        temp = []
        for q in i:
            temp.append(q)
        Matrix.append(temp)
    TupleMatrix = tuple(map(tuple,Matrix))
    return TupleMatrix


#Iterative is much easier to debug than recursive. This is still the A* algorithm, which is basically just modified dijikstras.
def Search(FirstState):
    Frontier = [FirstState]
    heapq.heapify(Frontier)
    Explored = {FirstState.GameMatrix}
    States = []
    while (Frontier != []):
        CurrState = heapq.heappop(Frontier)
        States.append(CurrState)
        if CurrState.GameMatrix[2][5] == 'X':
            return States
        else:
            AddtoHeap(Frontier,GenerateNewStates(CurrState,Explored))
    return []

def AddtoHeap(Frontier,NewFrontier):
    for i in NewFrontier:
        heapq.heappush(Frontier, i)
    

def GenerateNewStates(GameState,Explored):
    States = []
    for i in range(len(GameState.Vehicles)):
        #We use array index to know the location of Vehicle for copying Vehicles later on.
        #Generate via new states via vehicle movement.
        if (GameState.Vehicles[i].orientation%2):
            States = States + VerticalPush(GameState, GameState.Vehicles[i], i, Explored)
        else:
            States = States + HorizontalPush(GameState, GameState.Vehicles[i], i, Explored)
    return States

def CheckExplored(CurrState, Explored):
    if (CurrState.GameMatrix in Explored):
        return []
    else:
        Explored.add(CurrState.GameMatrix)
        return [CurrState]
        
#{---MOVEMENT OPERATORS---}

#These are pushes based on orientation, not on the direction of push. 
def VerticalPush(GameState, Vehicle, i,Explored):
    States = []
    if(Vehicle.y > 0 and GameState.GameMatrix[Vehicle.y-1][Vehicle.x] == '-'):
        States = States + CheckExplored(PushUp(GameState, Vehicle, i),Explored)
    if (Vehicle.y + Vehicle.length < len(GameState.GameMatrix) and GameState.GameMatrix[Vehicle.y+Vehicle.length][Vehicle.x] == '-'):
        States = States + CheckExplored(PushDown(GameState,Vehicle,i),Explored)
    return States

#Actual Pushes here.
def PushUp(CurrState, Vehicle, i):
    NewMatrix = list(map(list,(CurrState.GameMatrix)))
    NewVehicles =  copy.deepcopy(CurrState.Vehicles)

    NewMatrix[Vehicle.y-1][Vehicle.x] = Vehicle.char
    NewMatrix[Vehicle.y+ Vehicle.length-1][Vehicle.x] = '-'
    NewVehicles[i].y = Vehicle.y - 1

    NewTuple = tuple(map(tuple,NewMatrix))
    
    return GameState(NewTuple, CurrState.g, NewVehicles, CurrState)

def PushDown(CurrState, Vehicle, i):
    NewMatrix = list(map(list,(CurrState.GameMatrix)))
    NewVehicles =  copy.deepcopy(CurrState.Vehicles)

    NewMatrix[Vehicle.y][Vehicle.x] = '-'
    NewMatrix[Vehicle.y+ Vehicle.length][Vehicle.x] = Vehicle.char
    NewVehicles[i].y = Vehicle.y + 1
    
    NewTuple = tuple(map(tuple,NewMatrix))
    
    return GameState(NewTuple, CurrState.g, NewVehicles, CurrState)
        

def HorizontalPush(GameState, Vehicle, i, Explored):
    States = []
    if(Vehicle.x > 0) and (GameState.GameMatrix[Vehicle.y][Vehicle.x-1] == '-'):
        States =  States +CheckExplored(PushLeft(GameState, Vehicle, i), Explored)
    if (Vehicle.x + Vehicle.length < len(GameState.GameMatrix) and GameState.GameMatrix[Vehicle.y][Vehicle.x+Vehicle.length] == '-'):       
        States = States + CheckExplored(PushRight(GameState, Vehicle, i),Explored)
    return States

def PushRight(CurrState, Vehicle, i):
    
    NewMatrix = list(map(list,(CurrState.GameMatrix)))
    NewVehicles =  copy.deepcopy(CurrState.Vehicles)

    NewMatrix[Vehicle.y][Vehicle.x+Vehicle.length] = Vehicle.char
    NewMatrix[Vehicle.y][Vehicle.x] = '-'
    NewVehicles[i].x = Vehicle.x + 1
    
    NewTuple = tuple(map(tuple,NewMatrix))
    
    return GameState(NewTuple, CurrState.g, NewVehicles, CurrState)

def PushLeft(CurrState, Vehicle, i):

    
    NewMatrix = list(map(list,(CurrState.GameMatrix)))
    NewVehicles =  copy.deepcopy(CurrState.Vehicles)

    NewMatrix[Vehicle.y][Vehicle.x + Vehicle.length-1] = '-'
    NewMatrix[Vehicle.y][Vehicle.x-1] = Vehicle.char
    NewVehicles[i].x = Vehicle.x - 1
    NewTuple = tuple(map(tuple,NewMatrix))
    
    return GameState(NewTuple, CurrState.g, NewVehicles, CurrState)


def Printing(Path):
    if len(Path) == 0:
        print("No Solution could be found")
    else:
        BackTracking(Path)


#Each GameState contains a pointer to the parent. So we just start from the success node and backtrack to the first node to get the real path.
def BackTracking(Path):
    CurrState = Path[-1]
    TruePath = []
    
    while (CurrState.Parent != None):
        TruePath.append(CurrState)
        CurrState = CurrState.Parent
    TruePath.reverse()
    for i in TruePath:
        for y in i.GameMatrix:
                print(y)
        print('\n')
    
    #We do not count the initial state as a move but we do for explored. 
    print("Total Moves: ",len(TruePath))
    print("Total states explored: ",len(Path))



def cons(item,lst):
    return item + lst

#I know, this looks like a giant wall of text. This function finds individual vehicles on the intial board
# and adds them to a list for later. Because of how I need to change my array accesses, abstracting things
# would just make the code more complicated than it needs to, save for some overloading tomfoolery that I am not bothered to do right now. 

#How this works is by iterating on matrix till we find a character. Then we search if the character exists on down or right to build vehicle.
def FindVehicles(GameMatrix):
    Vehicles = []
    for y in range(len(GameMatrix)):
        for x in range(len(GameMatrix[y])):
            if GameMatrix[y][x] != '-' and (GameMatrix[y][x] in Vehicles) == False:
                char = GameMatrix[y][x]
                length = 1
                #Check for right oriented
                if (x < len(GameMatrix)-1 and GameMatrix[y][x+length] == char):
                    while (x+length < len(GameMatrix) and GameMatrix[y][x+length] == char):
                        length = length + 1
                    Vehicles.append(Vehicle(x,y,length,char,2))
                #Check for down oriented
                elif (y < len(GameMatrix)-1 and GameMatrix[y+length][x] == char):
                    while (y+length < len(GameMatrix) and GameMatrix[y+length][x] == char):
                        length = length + 1
                    Vehicles.append(Vehicle(x,y,length,char,1))

                # Why do we skip up and left? Because down and right will take in all down and left, so
                # that we ensure that x,y coords are always at the "head" of the vehicle. 
                # This reduces the number of conditions to check later on in state generation.
    return Vehicles

