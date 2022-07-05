import socket
from threading import Thread
import random

# server's IP address
SERVER_HOST = "192.168.90.6"
SERVER_PORT = 8888
all_cs = set()
pl = []
l_enemy = ["Goblin", "Kobold", "Orc"]
s = socket.socket()
hints = ["The orc attacks the buffest character first", "When fighting with a kobold, you can only pray", "Goblin is smart. Weak looking enemy will die first", "Be wary with the altar, young adventurer. For it can cause demise unknowingly.", "Unify your answers when faced with a statue, only then rewards will be reaped.", "Warping. The act of self degrading. In dire times, you can warp yourself in the hopes that the enemy does not target you."]
# Make port as reusable port
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((SERVER_HOST, SERVER_PORT))
s.listen(2)
print("\n\t~~~~~~~~~~ PYTHON MULTIPLAYER GAME ~~~~~~~~~~ ")
print("---------------------------------------------------")
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")
menu = "\n!! Make your move NOW !! \n1. Attack\n2. Defend\n3. Analyze\n4. Warp\n5. Heal\n6. Wait\n\n"
death_count = 0
class enemy:
    def __init__(self, typ, stren, agil, intel):
        self.typ = typ
        if self.typ == "Goblin":
            self.m_hp = stren + 5
        elif self.typ == "Kobold":
            self.m_hp = stren + 10
        elif self.typ == "Orc":
            self.m_hp = stren + 15
        self.c_hp = self.m_hp
        self.stren = stren
        self.agil = agil
        self.intel = intel
    
    def p_stat(self):
        return f"Type: {self.typ}\nHealth: {self.c_hp}/{self.m_hp}\nStrength: {self.stren}\nAgility: {self.agil}\nIntelligence: {self.intel}"
    
    def take_dmg(self, dmg):
        self.c_hp = self.c_hp - dmg

    def cond(self):
        if self.c_hp >= self.m_hp * 3/4:
            return "Healthy"
        elif self.c_hp >= self.m_hp * 2/4:
            return "Hurt"
        elif self.c_hp >= self.m_hp * 1/ 4:
            return "Very Hurt"
        else:
            return "Near Death"

    def deal_dmg(self):
        if self.typ == "Orc":
            dmg = self.stren
        elif self.typ == "Kobold":
            dmg = self.agil
        elif self.typ == "Goblin":
            dmg = self.intel
        return dmg
    
    def heal(self, h):
        self.c_hp += h
        if self.c_hp > self.m_hp:
            self.c_hp = self.m_hp
            
def sto1(cs, msg):
    cs.send(msg.encode())

def stoa(msg):
    for cs in all_cs:
        cs.send(msg.encode())

class adv:
    def __init__(self, cl, stren, agil, intel):
        self.cl = cl
        #if cl == "Warrior":   #Not used because it will be unfair to people who got mage, which have the worst hp = one shot killed by everything
        #    self.c_hp = stren + 10
        #    self.m_hp = stren + 10
        #elif cl == "Archer":
        #    self.c_hp = stren + 5
        #    self.m_hp = stren + 5
        #elif cl == "Mage":
        #    self.c_hp = stren
        #    self.m_hp = stren
        self.c_hp = 20
        self.m_hp = 20
        self.stren = stren
        self.agil = agil
        self.intel = intel
        self.dead = 0
        self.dmg_taken = 1
        self.insight = 0

    def p_health(self):
        return f"Health {self.c_hp}/{self.m_hp}"

    def take_dmg(self, dmg):
        self.c_hp = self.c_hp - (dmg * self.dmg_taken)
        self.dmg_taken = 1

    def p_stat(self):
        return f"Class: {self.cl}\nHealth: {self.c_hp}/{self.m_hp}\nStrength: {self.stren}\nAgility: {self.agil}\nIntelligence: {self.intel}"

    def cond(self):
        if self.c_hp >= self.m_hp * 3/4:
            return f"Healthy"
        elif self.c_hp >= self.m_hp * 2/4:
            return f"Hurt"
        elif self.c_hp >= self.m_hp * 1/ 4:
            return f"Very Hurt"
        elif self.c_hp > 0:
            return f"Near Death"
        else:
            return f"Dead"

    def death(self):
        self.c_hp = 0
        self.stren = 0
        self.agil = 0
        self.intel = 0
        self.dead = 1

    def analyze(self):
        self.insight = 1

    def deal_dmg(self): #Dealing damage
        if self.cl == "Warrior":
            dmg = self.stren
        elif self.cl == "Archer":
            dmg = self.agil
        elif self.cl == "Mage":
            dmg = self.intel
        return dmg

    def warping(self, targ): #Minus stat
        if targ == "1":
            print("Warping strength")
            self.stren -= 2
        elif targ == "2":
            print("Warping Agility")
            self.agil -= 2
        elif targ == "3":
            print("Warping Intelligence")
            self.intel -= 2

    def sac(self):
        if self.cl == "Warrior":
            self.stren += 10
        elif self.cl == "Archer":
            self.agil += 10
        elif self.cl == "Mage":
            self.intel += 10

    def defend(self):
        self.dmg_taken = 0.5

    def heal(self, h):
        self.c_hp += h
        if self.c_hp > self.m_hp:
            self.c_hp = self.m_hp

def warp(player):
    if player == 0:
        sto1(pl1, pl[player].p_stat())
        sto1(pl1, "\n1. Strength\n2. Agility\n3. Intelligence\n\n5. Back")
        return pl1.recv(1024).decode()
    elif player == 1:
        sto1(pl2, pl[player].p_stat())
        sto1(pl2, "\n1. Strength\n2. Agility\n3. Intelligence\n\n5. Back")
        return pl2.recv(1024).decode()

def w_room():
    global pl1
    global pl2
    player = 1
    while player != 3:
        clas = random.choice(["Warrior", "Archer", "Mage"])
        if clas == "Warrior":
            stren = 10
            agil = 5
            intel = 3
        elif clas == "Archer":
            stren = 5
            agil = 10
            intel = 3
        elif clas == "Mage":
            stren = 3
            agil = 5
            intel = 10
            
        client_socket, client_address = s.accept()
        print(f"[+] {client_address} connected.\n---------------------------------------------------")
        all_cs.add(client_socket)
        if player == 1:
            pl1 = client_socket
            print("player 1")
            sto1(pl1, "Player 1 has entered")
            pl.append(adv(clas, stren, agil, intel))
        elif player == 2:
            pl2 = client_socket
            print("player 2")
            msg = "Player 2 has joined"
            pl1.send(msg.encode())
            pl.append(adv(clas, stren, agil, intel))
        player+=1

def select(play):
    norm = f"1. Player 1: {pl[0].cond()}\n2. Player 2: {pl[1].cond()}\n3. {enemy1.typ}: {enemy1.cond()}\n\n5. Back"
    hide = f"1. Player 1: {pl[0].cond()}\n2. Player 2: {pl[1].cond()}\n3. Hidden: {enemy1.cond()}\n\n5. Back"
    if play == 0:
        if pl[play].insight == 0:
            sto1(pl1, hide + "\nWho?")
        else:
            sto1(pl1, norm + "\nWho?")
        return pl1.recv(1024).decode()
    elif play == 1:
        if pl[play].insight == 0:
            sto1(pl2, hide + "\nWho?")
        else:
            sto1(pl2, norm + "\nWho?")
        return pl2.recv(1024).decode()

def death_check():
    global death_count
    i = 0

    death_count = 0
    for check in pl:
        if pl[i].dead == 1:
            death_count += 1
        i += 1

    i = 0
    for check in pl:
        if (pl[i].c_hp <= 0 or pl[i].stren <= 0) and pl[i].dead == 0:
            pl[i].death()
            death_count += 1
            if i == 0:
                sto1(pl1, "died\n")
                sto1(pl1, "Hint: ")
                sto1(pl1, random.choice(hints))
                sto1(pl2, f"Player 1 has died while fighting {enemy1.typ}\n")
            elif i == 1:
                sto1(pl2, "died\n")
                sto1(pl2, "Hint: ")
                sto1(pl2, random.choice(hints))
                sto1(pl1, f"Player 2 has died while fighting {enemy1.typ}'n")
        i += 1
    if death_count >= 2:
        endprog()

def hidden(hid ,player):
    norm = f"\nPlayer 1: {pl[0].cond()}\nPlayer 2: {pl[1].cond()}\n{enemy1.typ}: {enemy1.cond()}\n\n"
    hide = f"\nPlayer 1: {pl[0].cond()}\nPlayer 2: {pl[1].cond()}\nHidden: {enemy1.cond()}\n\n"
    if hid == 0:
        sto1(player, hide)
    elif hid == 1:
        sto1(player, norm)

def turn(play): #play = 0 == PLayer 1 turn, play = 1 == Player 2 turn
    while True:
        dc = 0
        act = "0"
        while act != "1" and act != "2" and act != "3" and act != "4" and act != "5" and act != "6":
            act = "0"
            if play == 0 and not pl[0].dead:
                try:
                    if not pl[1].dead and dc != 1:
                        sto1(pl2, "Waiting for Player 1 to finish turn")
                    hidden(pl[play].insight, pl1)
                    sto1(pl1, pl[play].p_stat() + "\n\n")
                    sto1(pl1, menu)
                    sto1(pl1, "\n\nCommand: ")
                    act = pl1.recv(1024).decode()
                except:
                    print("Player 1 has dc")
                    sto1(pl2, "Player 1 has disconnected")
                    pl[0].death()
                    dc = 1
                    break

            elif play == 1 and not pl[1].dead:
                try:
                    if not pl[0].dead and dc != 1:
                        sto1(pl1, "Waiting for Player 2 to finish turn")
                    hidden(pl[play].insight, pl2)
                    sto1(pl2, pl[play].p_stat() + "\n\n")
                    sto1(pl2, menu)
                    sto1(pl2, "\n\nCommand: ")
                    act = pl2.recv(1024).decode()
                except:
                    print("Player 2 has dc")
                    sto1(pl1, "Player 2 has disconnected")
                    pl[1].death()
                    dc = 1
                    break
            else:
                break

        if dc == 1:
            break

        if act == "1":
            print("Attacking")
            targ = select(play)
            if targ == "3":
                print(f"Attacking {enemy1.typ}\n")
                enemy1.take_dmg(pl[play].deal_dmg())
            elif targ == "1":
                print("Attacking player 1\n")
                pl[0].take_dmg(pl[play].deal_dmg())
            elif targ == "2":
                print("Attacking player 2\n")
                pl[1].take_dmg(pl[play].deal_dmg())
            elif targ == "5": #Back
                print("Back from Attacking\n")
                continue
            break

        elif act == "2":
            print("Defending\n")
            pl[play].defend()
            break

        elif act == "3":
            targ = select(play)
            if targ == "3":
                print("Analyzing enemy")
                stat = enemy1.p_stat()
            elif targ == "1":
                print("Analyzing Player 1")
                stat = pl[0].p_stat()
            elif targ == "2":
                print("Analyzing Player 2")
                stat = pl[1].p_stat()
            elif targ == "5": #Back
                print("Back from analyzing")
                continue
            pl[play].analyze()
            if play == 0:
                sto1(pl1, stat)
            elif play == 1:
                sto1(pl2, stat)
            break
        
        elif act == "4":
            targ = warp(play)
            if targ == "5":
                print("Back from Warping")
                continue
            else:
                pl[play].warping(targ)
                break

        elif act == "5":
            targ = select(play)
            if targ == "1":
                pl[0].heal(3)
            elif targ == "2":
                pl[1].heal(3)
            elif targ == "3":
                enemy1.heal(3)
            elif targ == "5":
                continue
            break

        elif act == "6":
            print("Wait")
            break

    death_check()

def battle():
    play = 0
    if not pl[0].dead:
        sto1(pl1, "\nYou have encountered an enemy, prepare for BATTLE.\n")
    if not pl[1].dead:
        sto1(pl2, "\nYou have encountered an enemy, prepare for BATTLE.\n")
    global enemy1
    global death_count
    enemy1 = enemy(random.choice(l_enemy), random.randint(5,10), random.randint(5,10), random.randint(5,10))
    print("\n!!Created enemy!!\n" + enemy1.p_stat())
    while enemy1.c_hp > 0: #Fight until enemy dies
        if pl[0].agil >= pl[1].agil: #Player 1 then player 2
            if not pl[0].dead:
                turn(0)
            if not pl[1].dead:
                turn(1)
        elif pl[1].agil > pl[0].agil: #Player 2 then player 1
            if not pl[1].dead:
                turn(1)
            if not pl[0].dead:
                turn(0)
        if enemy1.c_hp > 0: #Enemy's Turn
            if enemy1.typ == "Goblin":
                if pl[0].intel >= pl[1].intel and not pl[1].dead:
                    pl[0].take_dmg(enemy1.deal_dmg())
                else:
                    pl[0].take_dmg(enemy1.deal_dmg())
            elif enemy1.typ == "Orc":
                if pl[0].stren >= pl[1].stren and not pl[0].dead:
                    pl[0].take_dmg(enemy1.deal_dmg())
                    pl[1].take_dmg(int(enemy1.deal_dmg() * 0.2))
                else:
                    pl[1].take_dmg(enemy1.deal_dmg())
                    pl[0].take_dmg(int(enemy1.deal_dmg() * 0.2))
            elif enemy1.typ == "Kobold":
                hit = random.randint(0,1)
                pl[hit].take_dmg(enemy1.deal_dmg())
        print("\n")
        print("Player 1 stats\n" + pl[0].p_stat())
        print("\n")
        print("Player 2 stats\n" + pl[1].p_stat())
        print("\n")
        print("Enemy stats\n" + enemy1.p_stat())
        print("\n")
        i = 0
        for check in pl:
            pl[i].dmg_taken = 1 #Reset the defense
            i += 1
        death_check()
    i = 0
    for check in pl:
        pl[i].insight = 0

def sac_room():
    print("Sacrifical Room")
    if not pl[0].dead:
        sto1(pl1, "You encountered a room with an altar in the middle. There are carvings on the floor that says \"Sacrifice some of your partner's life for greater power\"\nWhat will you do?\n\n1. Sacrifice\n2. Leave\n")
    if not pl[1].dead:
        sto1(pl2, "You encountered a room with an altar in the middle. There are carvings on the floor that says \"Sacrifice some of your partner's life for greater power\"\nWhat will you do?\n\n1. Sacrifice\n2. Leave\n")
    if not pl[0].dead:
        if not pl[1].dead:
            sto1(pl2, "Waiting for player 1")
        sto1(pl1, "\n\nCommand: ")
        com1 = pl1.recv(1024).decode()
        if com1 == "1":
            pl[0].sac()
            pl[1].take_dmg(10)
            death_check()
    if not pl[1].dead:
        if not pl[0].dead:
            sto1(pl1, "Waiting for player 2")
        sto1(pl2, "\n\nCommand: ")
        com2 = pl2.recv(1024).decode()
        if com2 == "1":
            pl[1].sac()
            pl[0].take_dmg(10)
            death_check()

def rec_room():
    print("Recovery Room")
    if not pl[0].dead:
        sto1(pl1, "You encountered a room with a statue inside. Carvings on the statues that says \"Answer with unison, fruition shall follow. Answer with contrast, only dust will follow\"\nWhat will you do?\n\n1. Single heal\n2. All heal\n")
    if not pl[1].dead:
        sto1(pl2, "You encountered a room with a statue inside. Carvings on the statues that says \"Answer with unison, fruition shall follow. Answer with contrast, only dust will follow\"\nWhat will you do?\n\n1. Single heal\n2. All heal\n")
    if not pl[0].dead:
        if not pl[1].dead:
            sto1(pl2, "Waiting for player 1")
        sto1(pl1, "\n\nCommand: ")
        com1 = pl1.recv(1024).decode()
        if com1 == "1":
            sto1(pl1, "Who Shall be healed?\n\n1. Player 1\n2. Player 2")
            h1 = pl1.recv(1024).decode()
            print(f"h1: {h1}")
        else:
            com1 = "2"
    if not pl[1].dead:
        if not pl[1].dead:
            sto1(pl2, "Waiting for player 1")
        sto1(pl2, "\n\nCommand: ")
        com2 = pl2.recv(1024).decode()
        if com2 == "1":
            sto1(pl2, "Who Shall be healed?\n\n1. Player 1\n2. Player 2")
            h2 = pl2.recv(1024).decode()
            print(f"h2: {h2}")
        else:
            com2 = "2"
    if pl[0].dead:
        com1 = com2
        h1 = h2
    if pl[1].dead:
        com2 = com1
        h2 = h1
    if com1 == "2" and com2 == "2":
        pl[0].heal(5)
        pl[1].heal(5)
        print("All Heal by 5")
    elif com1 == com2 and h1 == h2:
        if h1 == "1":
            print("Heal player 1 by 10")
            pl[0].heal(10)
        elif h1 == "2":
            print("Heal player 2 by 10")
            pl[1].heal(10)
    else:
        if not pl[0].dead:
            sto1(pl1, "No help will be given to people with no unison")
        if not pl[1].dead:
            sto1(pl2, "No help will be given to people with no unison")

def endprog():
    global death_count
    if death_count == 2:
        print("!!ATTENTION!! Both players has died!")
        for cs in all_cs:
            cs.close()
        s.close()
        quit()

w_room()
n_enc = 0

while n_enc <= 5:
    n_enc += 1
    if n_enc == 3:
        sac_room()
    elif n_enc == 5:
        rec_room()
    else:
        battle()

i = 0
for cd in all_cs:
    if not pl[i].dead:
        if i == 0:
            sto1(pl1, "win")
        else:
            sto1(pl2, "win")
    i += 1

for cs in all_cs:
    cs.close()
s.close()
