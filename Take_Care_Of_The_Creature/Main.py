
import time , os , random , math
from  datetime import datetime
from Character import character

# Reading and Appending the file information
statsFile = open("CharacterStats.txt","r+")
loginLog = open("LoginLog.txt","a+")

statsInfoE = []
infoDict = {}

# Writing action time to the log
currrentTime = datetime.now()
loginLog.write(currrentTime.strftime("%d/%m/%Y %H:%M !Program_Started\n")) 


######### FUNCTIONS #########

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def switchGame(no1,no2,operator):
    resultCases = {
        "*": no1 * no2,
        "-": no1 - no2,
        "+": no1 + no2,
        "/": math.ceil(int(no1 / no2)),
    }
    return resultCases.get(operator)

# Math Game for earning coins
def mathGame(character):
    clear_terminal()
    randomNo1 = random.randint(1,100)
    randomNo2 = random.randint(1,100)
    operatorsList = ["*","-","+","/"]
    operator = random.choice(operatorsList)
    result = switchGame(randomNo1,randomNo2,operator)
    print(character.checkImage())
    solve = int(input(f"\n{character.name} asks: {randomNo1} {operator} {randomNo2} = ? (Please enter integer value)"))
    if solve == result:
        print(f"{character.name}: Yess , it is Correct\nYou earn +5 Coin")
        character.coin += 5
    else:
        print(f"{character.name}: No , it is Wrong\nYou earn nothing")
        
# Store
def store(character):
    clear_terminal()
    while True:
        clear_terminal()
        print(f"1)Bread / +10 Hunger \t\tCoin:{character.coin}\n2)Pasta / +25 Hunger\n0)Exit")
        choice = int(input("Enter: "))
        clear_terminal()
        if character.coin > 0:
            if choice == 1:
                choice2 = input("Bread Cost = 40 Coin. Buy? (y/n)")
                if choice2.lower() == "y" and character.coin >= 40:
                    character.coin -=40
                    character.hunger = min(character.hunger + 10, 100)
                    loginLog.write(currrentTime.strftime(f"%d/%m/%Y %H:%M !{character.name}_ate_Bread\n")) 
            elif choice == 2:
                choice2 = input("Past Cost = 80 Coin. Buy? (y/n)")
                if choice2.lower() == "y" and character.coin >= 80:
                    character.coin -= 80
                    character.hunger = min(character.hunger + 25, 100)
                    loginLog.write(currrentTime.strftime(f"%d/%m/%Y %H:%M !{character.name}_ate_Pasta\n")) 
            elif choice == 0:
                break
            else:
                print("Enter a valid number")
        else:
            print("You dont have enough coin to buy anything!")
            break
    
# Taking informations from CharacterStats,txt and putting these information to the dict
def takeInfo():
    statsInfo = statsFile.read().split("\n")
    for i in range(len(statsInfo)):
        statsInfoE.append(statsInfo[i].split(":"))
        infoDict.update({statsInfoE[i][0] : statsInfoE[i][1]})
        if statsInfoE[i][0] == "Hunger" or statsInfoE[i][0] == "Coin":
            infoDict.update({statsInfoE[i][0] : float(statsInfoE[i][1])})
    return infoDict

# Update Stats
def updateStats(character):
    statsFile.seek(0)
    statsFile.write(f"Name:{character.name}\nHunger:{character.hunger}\nStatus:{character.status}\nCoin:{character.coin}")

# Updating the status of the creature
def updateStatus(character):
    try:
        loginLog.seek(0)
        pastInfo = loginLog.readlines()[-2].split(" ") # Getting last program ending date info
    except:
        loginLog.seek(0)
        pastInfo = loginLog.readlines()[-1].split(" ") # If code is here there is no last program ending date info
    
    #Calculating the time difference between last ending date
    lastDate = datetime.strptime(pastInfo[0],"%d/%m/%Y")
    lastTime = datetime.strptime(pastInfo[1],"%H:%M").time()
    lastDateTime = datetime.combine(lastDate.date(),lastTime)
    timeDifference = (currrentTime - lastDateTime).total_seconds() // 60

    # Changing hunger value
    character.hunger = round(character.hunger - timeDifference * 0.1,2)

    # Changing character.status
    if character.hunger >= 85:
        character.status = "Happy"
    elif character.hunger >= 50 :
        character.status = "Default"
    elif character.hunger >= 1:
        character.status = "Sad"
    elif character.hunger < 0:
        character.status = "Dead"
        character.hunger = 0
    
    # Updating Logs
    updateStats(character)
    
# Creating a character
if os.stat("CharacterStats.txt").st_size == 0:
    name = input("Write a name for your creature: ")
    statsFile.write(f"Name:{name}\nHunger:{50}\nStatus:Default\nCoin:{100}")

statsFile.seek(0)
Info = takeInfo()
creature = character(Info.get("Name"), Info.get("Hunger"), Info.get("Status"), Info.get("Coin"))
updateStatus(creature)
# Game Loop
while True:
    clear_terminal()
    print("Status :",creature.status," " * 4,"Hunger :",creature.hunger," " * 8,"Coin :",creature.coin)
    print(creature.checkImage())
    print("\n"," " * 20, creature.name)
    
    print(f"\n1)Play Math Game\n2)Play Rock-Paper-Scissors\n3)Store\n0)Exit")
    choice = int(input("Enter: "))
    
    if choice == 1:
        # Play Math Game
        mathGame(creature)
    elif choice == 2:
        # Play R-P-S
        pass
    elif choice == 3:
        # Open store
        store(creature)
        updateStatus(creature)
    elif choice == 0:
        loginLog.write(currrentTime.strftime("%d/%m/%Y %H:%M !Program_Ended\n")) 
        updateStats(creature)
        statsFile.close()
        loginLog.close()
        break
    else:
        print("Please enter a valid number !")
        
    time.sleep(1)
    

### TODO ###
# Kucuk oyunlari oynayarak para kazanma sistmi getirilmeli
# - Tas-Kagit-Makas / 