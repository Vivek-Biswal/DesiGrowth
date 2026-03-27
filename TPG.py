import random
print("TERMINAL RPG BATTLE")
print()
print("INSTRUCTIONS:\nPress a/A for attack\nPress h/H to use healing potion\nPress r/R to escape from the game\nOnly 3 healing potions are available that provides +15 health\nYou can cast your healing potion only after your first move!")
print()
player_health=100

goblin_health=100

healing_potion=3

playing=True
name=input("Enter player's name: ")
print()
while playing:
    player_attack=random.randint(10,20)
    player_run=random.randint(1,2)

    goblin_attack=random.randint(5,15)
    
    user=input("Enter your move: ")
    user_input=user.lower()


    if user_input=="a":
        
        goblin_health-=player_attack
        print(name,"damaged the Goblin to",goblin_health)

    elif user_input=="h":
        if healing_potion>0:
            healing_potion-=1
            player_health+=15
        
            print(name,"used the healing potion!")
            print("Available healing potions are:",healing_potion)
        else:
            print("Out of potions!")
       
    
    elif user_input=="r":
        if player_run==1:
            print(name,"ran away from the field!")
            print("Goblin won!")
            playing=False
            break
        else:
            print("Your escape attempt failed!")
            

    else:
        print("Enter a valid move!")
        print()
        continue
        
        
    if goblin_health>0 and player_health>0:
        player_health-=goblin_attack

        print("Goblin damaged",name,"to",player_health)
        print(name,"health is:",player_health)
        print("Goblin health is:",goblin_health)
        print()
        
        
    if goblin_health<=0:
        print(name,"won!")
        print("Goblin died!")
        playing=False
        
        
    if player_health<=0:
        print("You lose!")
        playing=False
    
print("Congratulations! Thanks for playing!")
