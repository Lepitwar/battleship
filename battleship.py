#Dylan Waters
#ID:1343144

import random
from string import ascii_uppercase
class BattleshipGame:
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self):
        #generates the 10x10 grid for both comnputer and user
        self.__comp_board =[]
        for yaxis in range(10):
            self.__comp_board.append([" "]*10) 
        self.__user_board =[]
        for yaxis in range(10):
            self.__user_board.append([" "]*10) 
        #The creation of the global lists, used througout the function
        self.__Ship_Sizes=[5,4,3,3,2]
        self.__Ship_letter=['A',"B","S","D","P"]
        self.__Ship_Names=['Aircraft Carrier','Battleship','Submarine','Destroyer','Patrol Boat']
        self.__Comp_ships=[]
        self.__User_ships=[]
        self.__User_sunken_ships=[]
        self.__Comp_sunken_ships=[]
        self.__CompShipCoords=[]
        self.__UserShipCoords=[]
        self.__CompShotCoords=[]
        self.__UserShotCoords=[]
        self.__EnemyCoords=[]
        self.__temp=[]
        self.__UserMisses=0
        self.__CompMisses=0
        self.__UserHits=0
        self.__CompHits=0
        self.__round=0
        self.__smartHunt=[]
        computer=True
        self.RandomShipGenerator(computer)
    #generates the 5 ships for computer 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def smartHunt(self):
        lowest=self.smarterHunt()
        #lowest=2
        start=0
        for yaxis in range(10):
            x=start
            while x<10:
                self.__smartHunt.append([x,yaxis])
                x+=lowest
            start+=1
            if start==lowest:
                start=0
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def smarterHunt(self):
        target=2
        shiplengths=[]
        for ship in self.__User_sunken_ships:
            shiplengths.append(len(ship[2])-1)
        if 2 in shiplengths:
            target=3
            shiplengths.remove(2)
            if 3 in shiplengths:
                shiplengths.remove(3)
                if 3 in shiplengths:
                    target=4
                    shiplengths.remove(3) 
                    if 4 in shiplengths:
                        target=5
                        shiplengths.remove(4)
        #print("Target is length",target,shiplengths)
        #invalidCoords=[]
        #index=1
        #while index != target:
            #start=0
            #for y in range(10):
                #x=start
                #while x<10:
                    #if [x+index,y] in self.__CompShotCoords and [x-index,y] in self.__CompShotCoords:
                        #if [x,y+index] in self.__CompShotCoords and [x,y-index] in self.__CompShotCoords:
                            #print(x,y,'INVALID')
                            #if [x,y] not in invalidCoords:
                                #invalidCoords.append([x,y])
                    ##self.__smartHunt.append([x,yaxis])
                    #x+=target
                #start+=1
                #if start==target:
                    #start=0   
            #index+=1
        #print(invalidCoords)
        #print("no loop")
        return target
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def RandomShipGenerator(self,computer):
        for index in range(len(self.__Ship_Sizes)):
            valid=False
            while not valid:
                x=random.randint(0,9)
                y=random.randint(0,9)
                #0:ship is vertical 1:ship is horizontal 
                direction=random.randint(0,1)
                orientation='v'
                if direction==1:
                    orientation='h'
                valid=self.validatePlacement(computer,self.__Ship_letter[index],self.__Ship_Sizes[index],x,y,orientation)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def drawingShips(self,hide):
        if hide==False:
            #at the end of the game, if you lose, the computer will display it's board
            for ship in self.__Comp_ships:
                letter=ship.pop()
                for coord in ship:
                    self.__comp_board[coord[1]][coord[0]]=letter
                ship.append(letter)
        
        for ship in self.__User_ships:
            #displays users board
            letter=ship.pop()
            for coord in ship:
                self.__user_board[coord[1]][coord[0]]=letter
            ship.append(letter)        
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~     
    def hittingShips(self):
        self.getMisses(None)
        self.getHits(None)
        for shot in self.__CompShotCoords:
            #Updates the board with every shot taken by the computer
            hit=False
            for ship in self.__User_ships:
                if shot in ship:
                    self.__user_board[shot[1]][shot[0]]='#'
                    self.getHits(True)
                    hit=True
            if not hit:
                self.__user_board[shot[1]][shot[0]]='*'
                self.getMisses(True)
        for shot in self.__UserShotCoords:
            #Updates the board with every shot taken by the User
            hit=False
            for ship in self.__Comp_ships:
                if shot in ship:
                    self.__comp_board[shot[1]][shot[0]]='#'
                    self.getHits(False)
                    hit=True
            if not hit:
                self.getMisses(False)
                self.__comp_board[shot[1]][shot[0]]='*'          
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def drawBoards(self,hide):
        #hide=False
        self.drawingShips(hide)
        self.hittingShips()
        SunkenComp=self.getEnemyFleet(False)
        SunkenUser=self.getEnemyFleet(True)
        while len(SunkenComp)!=7:
            SunkenComp.append(' ')
        while len(SunkenUser)!=7:
            SunkenUser.append(' ')            
            
        printlist=[]
        statement1="Nbr. of hits  : "+'\t'+' '+str(self.__CompHits)+'\t'*2+"   "+str(self.__UserHits)
        statement2="Nbr. of Misses: "+'\t'+' '+str(self.__CompMisses)+'\t'*2+"   "+str(self.__UserMisses)
        statement3="Ships sunk    : "+'\t'+' '+str(len(self.__User_sunken_ships))+'\t'*2+"   "+str(len(self.__Comp_sunken_ships))
        #Printing the actual board
        rownumber=0
        print("\n  Computer's board:",'\t'," User's board:",'\t',"At round:",self.__round)
        print('  1 2 3 4 5 6 7 8 9 10','\t',' 1 2 3 4 5 6 7 8 9 10','\t'*3,'Computer Status:  User Status:')
        for grid in range(len(self.__comp_board)):
            print(ascii_uppercase[rownumber],end='|')          
            for row in self.__comp_board[grid]:
                print(row,end='|')
            print('\t'+ascii_uppercase[rownumber],end='|')          
            for row in self.__user_board[grid]:
                print(row,end='|')
            if rownumber==0:
                print('',statement1)
            elif rownumber==1:
                print('',statement2) 
            elif rownumber==2:
                print('',statement3)
            else:
                sunken2=SunkenComp[rownumber-3]
                sunken1=SunkenUser[rownumber-3]
                print('\t'*3+' '+sunken2.ljust(16)+"  "+sunken1.ljust(16))

            rownumber+=1
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  
    #The Start of placements fucntions, they check if the coord is already taken.
    #CompShipCoords and UserShipCoords is a list of all the taken coords.
    #Iterates over the length of the ship, if they are all valid, it returns the ship
    def computerVerticalPlacement(self,x,y,size,TempShip):
        if [x,y] not in self.__CompShipCoords:
            TempShip.append([x,y])
            for i  in range(size-1):
                y+=1
                if [x,y] not in self.__CompShipCoords:
                    TempShip.append([x,y])
                else:
                    return False, []
        else:
            return False, []
        return True, TempShip
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def UserVerticalPlacement(self,x,y,size,TempShip):
        if [x,y] not in self.__UserShipCoords:
            TempShip.append([x,y])
            for i  in range(size-1):
                y+=1
                if [x,y] not in self.__UserShipCoords:
                    TempShip.append([x,y])
                else:
                    return False, []
        else:
            return False, []
        return True, TempShip    
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def computerHorizontalPlacement(self,x,y,size,TempShip):
        if [x,y] not in self.__CompShipCoords:
            TempShip.append([x,y])
            for i  in range(size-1):
                x+=1
                if [x,y] not in self.__CompShipCoords:
                    TempShip.append([x,y])
                else:
                    return False, []
        else:
            return False, []
        return True, TempShip
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def UserHorizontalPlacement(self,x,y,size,TempShip):
        if [x,y] not in self.__UserShipCoords:
            TempShip.append([x,y])
            for i  in range(size-1):
                x+=1
                if [x,y] not in self.__UserShipCoords:
                    TempShip.append([x,y])
                else:
                    return False, []
        else:
            return False, []
        return True, TempShip    
    
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def validatePlacement(self,computer,ship,size,x,y,orientation):
        #Checks the orientation and if its the computer then sends the ship to the proper placement function
        TempShip=[]
        valid=False
        if orientation.lower()=='v':
            #if it exceeds the board, returns false
            if (size+y)<11:
                #depending on computer, sends to the placement functions
                if computer:
                    valid,TempShip=self.computerVerticalPlacement(x,y,size,TempShip) 
                else:
                    valid,TempShip=self.UserVerticalPlacement(x,y,size,TempShip)
                    if valid==False:
                        return False
        elif orientation.lower()=='h':
            if size+x<11:
                if computer:
                    valid,TempShip=self.computerHorizontalPlacement(x,y,size,TempShip)
                else:
                    valid,TempShip=self.UserHorizontalPlacement(x,y,size,TempShip)
                    if valid==False:
                        return False  
        #if the ship is valid, it appends the coords to ship list and the taken coords list
        if valid and computer:
            TempShip.append(ship)
            self.__Comp_ships.append(TempShip)
            for index in TempShip:
                self.__CompShipCoords.append(index)
            return True
        elif valid and not computer:
            TempShip.append(ship)
            self.__User_ships.append(TempShip)
            for index in TempShip:
                self.__UserShipCoords.append(index)
            return True
        else:
            return False
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~     
    def userplacement(self):
        computer=False
        hide=True
        # UNCODE THIS PORTION FOR RANDOM PLACEMENT OF USER SHIPS
        randominput=input("Would you like your ships to be randomly placed? (Y/ENTER): ")
        if randominput.lower()=='y':
            self.RandomShipGenerator(computer)
            self.drawBoards(hide)
            return    
        #Generates the 5 user ships
        for index in range(len(self.__Ship_Sizes)):
            valid=False
            size=self.__Ship_Sizes[index]
            ship=self.__Ship_letter[index]
            while not valid:
                #validating coords enter by user
                print("Placing a",self.__Ship_Names[index],"of size",self.__Ship_Sizes[index])
                try:
                    userinput=input("Enter coordinates x y (x in [A..J] and y in [1..10]): ")
                    x,y=userinput.split()
                    x=ascii_uppercase.index(x.upper())
                    y=int(y)-1
                    if x >-1 and x <10 and y>-1 and y<10:
                        orientation=input("This ship is vertical or horizontal (v,h)? ")
                    else:
                        #Purposely raises an error to reset the validating process
                        error=int(error)
                except:
                    pass
                else:
                    #Sends the info to the placement functions
                    if self.validatePlacement(computer,ship,size,y,x,orientation):
                        self.drawBoards(hide)
                        valid=True
                    else:
                        #Makes the user enter new coords
                        self.drawBoards(hide)
                        if orientation.lower()=='h' or orientation.lower()=='v':
                            print('Cannot place a',self.__Ship_Names[index],'there. Stern is out of the board or collides with other ship. \nPlease take a look at the board and try again.')
                            pointless=input('Hit ENTER to continue. ')
                            
                        else:
                            print("Invalid orientation.")
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def _CompMakesMove(self):
        #Keeps an list of recently hit spots
        #If a boat sinks, it will remove it from the list of unknown coords
        if self.__temp!=[]:
            if self.__temp[-1]==True:
                self.__temp.pop()
                for ship in self.__User_ships:
                    shipsunk=True
                    for index in ship[:-1]:
                        if index in self.__temp:
                            pass
                        else:
                            shipsunk=False
                    if shipsunk:
                        for index in ship[:-1]:
                            self.__temp.remove(index)
                        return True
        return False
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def CompMakesMove(self):
        missedCoords=[]     
        if self._CompMakesMove():
            #if a boat sinks it resets the hunting list
            self.__EnemyCoords=[]
        #if there is unknown hit coords it will update where to look 
        if self.__temp!=[] and self.__EnemyCoords==[]:
            for mysterycoords in self.__temp:
                #makes each coord an 'intial' hit
                x=mysterycoords[0]
                y=mysterycoords[1]
                missedCoords.append([[x+1,y,"side"],[x,y+1,"vert"],[abs(x-1),y,"side"],[x,abs(y-1),"vert"]])
                for coord in missedCoords[0]:
                    if coord not in self.__CompShotCoords:
                        self.__EnemyCoords.append(coord)              
        # updates the valid hunting spots
        self.smartHunt()
        valid=False
        computer=True
        ori=False
        threat=[]
        answer=[]
        #The start of the hunting phase
        while not valid:
            if len(self.__EnemyCoords)!=0:
                #if there is priority spots
                proper=True
                while proper:
                    answer=self.__EnemyCoords.pop()
                    if answer[1]<int(10) and answer[1]>-1 and answer[0]<10 and answer[0]>-1:  
                        proper=False
                    else:
                        #if the list empty or the last coord is invalid 
                        answer=[]
                        rand_pop=random.randint(0,int(len(self.__smartHunt))-1)
                        xy=self.__smartHunt.pop()
                        x=xy[0]
                        y=xy[1]                           
                        break
                    if len(self.__EnemyCoords)==0:
                        #if the priority list is empty
                        rand_pop=random.randint(0,int(len(self.__smartHunt))-1)
                        xy=self.__smartHunt.pop()
                        x=xy[0]
                        y=xy[1]                           
                        break 
            else:
                #selects a random value in the valid hunting spots
                rand_pop=random.randint(0,int(len(self.__smartHunt))-1)
                xy=self.__smartHunt.pop(rand_pop)
                x=xy[0]
                y=xy[1] 
                answer=[]
                
            if answer!=[]:
                #priority shot, splits the variables 
                x=answer[0]
                y=answer[1]
                ori=answer[2]
            #move function
            valid,threat=self.makeA_Move(computer,x,y)
            if valid:
                #if the shot is a hit it up dates the priority list
                if len(threat)!=0:
                    for coord in threat[0]:
                        if coord not in self.__CompShotCoords:
                            self.__EnemyCoords.append(coord)
                
                if not ori==False:
                    #if the move was made from the priority list
                    #Removes the wrong directions
                    if [x,y] in self.__UserShipCoords:
                        for  index in self.__EnemyCoords:
                            if index[2] != ori:
                                self.__EnemyCoords.remove(index)        
                return 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def UserMakesMove(self):
        #user enters coords to make a mov function, prevents invalid ones
        valid=False
        computer=False
        while not valid:
            try:
                #x=random.randint(0,9)
                #=random.randint(0,9)   
                userinput=input("Enter coordinates x y (x in [A..J] and y in [1..10]): ")
                x,y=userinput.split()
                x=ascii_uppercase.index(x.upper())
                y=int(y)-1
                
            except:
                print("Invalid coordinates please try again")
            else:
                if x >-1 and x <10 and y>-1 and y<10:
                    if self.makeA_Move(computer,y,x):
                        return        
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def getEnemyFleet(self,computer):
        #lists of ships to sink and that have been sunken
        if computer:
            sunken=[]
            nonsunken=[]
            for ship in self.__Ship_Names:
                nonsunken.append(ship)
            for ship in self.__Comp_sunken_ships:
                nonsunken.remove(ship[1])
                sunken.append(ship[1])
        else:
            sunken=[]
            nonsunken=[]
            for ship in self.__Ship_Names:
                nonsunken.append(ship)
            for ship in self.__User_sunken_ships:
                nonsunken.remove(ship[1])
                sunken.append(ship[1])            
        return sunken
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def makeA_Move(self,computer,x,y): 
        #If the move coords are valid(Not already taken) then appends them to the master list
        #Provides feedback for user
        threat=[]
        if computer:
            if [x,y] not in self.__CompShotCoords:
                self.__CompShotCoords.append([x,y])
                if [x,y] in self.__UserShipCoords:
                    self.__temp.append([x,y])
                    #threat=[]
                    threat.append([[x+1,y,"side"],[x,y+1,"vert"],[abs(x-1),y,"side"],[x,abs(y-1),"vert"]])             
                self.drawBoards(True)
                return  True, threat
        else:
            if [x,y] not in self.__UserShotCoords:
                self.__UserShotCoords.append([x,y])
                self.drawBoards(True)
                if [x,y] in self.__CompShipCoords:
                    print("Hit at",ascii_uppercase[y],x+1)
                else:
                    print("Miss at",ascii_uppercase[y],x+1)
                return True
            else:
                print("Sorry",ascii_uppercase[y],x+1,"was already played. Try again.")
                return False 
        return False,[]
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def checkWinning(self,computer):
        #if all ships ae sunk returns true
        winning=True
        for ship in self.__Ship_letter:
            if not self.checkIfSunk(computer,ship):
                winning=False
        if winning:
            return True
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~      
    def checkIfSunk(self,computer,ship):
        #checks if a specific 'ship' just sank or has already been sunk
        sunk=True
        if computer:
            for symbol in self.__User_sunken_ships:
                if symbol[0]==ship:
                    return True
            index=self.__Ship_letter.index(ship)
            ship=self.__User_ships[index]
            for coords in ship[:-1]:
                if coords not in self.__CompShotCoords:
                    sunk=False
        else:
            for symbol in self.__Comp_sunken_ships:
                if symbol[0]==ship:
                    return True
            index=self.__Ship_letter.index(ship)
            ship=self.__Comp_ships[index]
            for coords in ship[:-1]:
                if coords not in self.__UserShotCoords:
                    sunk=False            
        if sunk:
            
            #if a ship just got sunk gives user feedback
            if computer:
                self.__temp.append(True)
                print("Your",self.__Ship_Names[index],'has been sunk!')
                self.__User_sunken_ships.append([self.__Ship_letter[index],self.__Ship_Names[index],ship])
            else:
                print("You sunk a",self.__Ship_Names[index]+'!')
                self.__Comp_sunken_ships.append([self.__Ship_letter[index],self.__Ship_Names[index],ship])
            return True
        return
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def incrementRounds(self):
        self.__round+=1
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def getMisses(self,computer):
        if computer==None:
            self.__UserMisses=0
            self.__CompMisses=0           
        elif computer:
            self.__CompMisses+=1
        else:
            self.__UserMisses+=1
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   
    def getHits(self,computer):
        if computer==None:
            self.__UserHits=0
            self.__CompHits=0            
        elif computer:
            self.__CompHits+=1
        else:
            self.__UserHits+=1
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def main():
    hide=True
    computer=True
    #Starts game
    game=BattleshipGame()
    game.drawBoards(hide)
    game.userplacement()
    input("Done placing user ships. Hit ENTER to continue. ")
    win=False
    while not win:
        #Actual game
        if computer:
            game.incrementRounds()
            game.CompMakesMove()
            game.getEnemyFleet(computer)
        else:
            game.UserMakesMove()
        win=game.checkWinning(computer)
        if win:
            #Win states
            if computer:
                hide=False
                game.drawBoards(hide)
                print('Computer won! Better luck next time')
            else:
                print('Congratulations! User WON!')
        else:
            #switches from user to computer, vise versa
            if computer:
                computer=False
            else:
                computer=True

main()