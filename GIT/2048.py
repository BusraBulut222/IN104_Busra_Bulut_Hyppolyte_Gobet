from random import *
from tkinter import *
from math import *
from copy import deepcopy
from numpy import *

####

#Jeu de 2048

# Lancez le programme pour plus d'explications



   
#      ___           ________                    ________
#    _/   \_        /        \        /         /        \
#   /       \       \        /       /          \        /
#           /       /        \      /           /        \
#          /        \        /     /            \________/
#         /         /        \    /     \       /        \
#        /          \        /   /______/___    \        /
#       /           /        \          \       /        \
#      /_______     \________/          /       \________/




# Lors du premier lancement, recopier ceci dans le shell après avoir lancé le programme, un message derreur va apparaitre, c'est normal, recopiez juste :

#     save("meilleurscore.npy",[[0],[0],[0],[0]])
#     save("derniercoup.npy",[])
#     save("dernierscore.npy",[])
#     save("victoires.npy",[[0],[0],[0],[0]])

# Puis relancez le programme






























A = list(load("derniercoup.npy"))
B=[list(i) for i in A]
C = list(load("dernierscore.npy"))

V = list(load("victoires.npy"))

def jeurandom(n):
    U = [[0 for i in range(n)] for j in range(n)]
    a = randint(2,3)
    A = [2,4]
    for i in range(a):
        x = randint(0,n-1)
        y = randint(0,n-1)
        U[x][y]=A[randint(0,1)]
    return(U)

score=[0]

meilleurscore = [[0],[0],[0],[0]]

P = list(load("meilleurscore.npy"))
for i in range(4):
    if P[i]>meilleurscore[i]:
        meilleurscore[i]=P[i]

def zéro(L):
    for x in L:
        if x == 0:
            return(True)
    return(False)

def suivantg(L,score2=score):
    while zéro(L):
        k=0
        while L[k]!=0:
            k+=1
        L.pop(k)
    J = []
    l = len(L)
    if l>=2:
        i = 0
        while i<l-1:
            if L[i]==L[i+1]:
                J.append(2*L[i])
                score2[0]+=2*L[i]
                i+=2
            else:
                J.append(L[i])
                i+=1
        if i == l-1:
            J.append(L[l-1])
    else:
        for x in L:
            J.append(x)
    return(J)

def inverse(L):
    l = len(L)
    for k in range(l//2):
        L[k],L[l-1-k] = L[l-1-k],L[k]

def suivantd(L,score2=score):
    inverse(L)
    u = suivantg(L,score2)
    inverse(u)
    return(u)

def nonvide(L):
    for x in L:
        if x!=0:
            return(True)
    return(False)

def pousseadroite(L):
    if nonvide(L):
        while L[len(L)-1] == 0:
            L[1:len(L)] = L[0:len(L)-1]
            L[0] = 0

def retourne(M):
    n = len(M)
    for i in range(n):
        for j in range(i):
            M[i][j],M[j][i]=M[j][i],M[i][j]

def recherchezero(M):
    L=[]
    for i in range(len(M)):
        for j in range(len(M)):
            if M[i][j] == 0:
                L.append((i,j))
    return(L)

def perdu(M):
    for L in M:
        if zéro(L):
            return(False)
        for x in range(len(L)-1):
            if L[x]==L[x+1]:
                return(False)
    retourne(M)
    for L in M:
        if zéro(L):
            retourne(M)
            return(False)
        for x in range(len(L)-1):
            if L[x]==L[x+1]:
                retourne(M)
                return(False)
    retourne(M)
    return(True)

def victoire(M):
    for x in range(len(M)):
        for y in range(len(M)):
            if M[x][y] == 2048:
                return(True)
    return(False)

def joue(action,D):
    A = deepcopy(D)
    if action == "gauche":
        m = 0
        for L in D:
            U = suivantg(L)
            D[m] = U
            m+=1
        for L in D:
            while len(L)<len(D):
                L.append(0)
    if action == "droite":
        m = 0
        for L in D:
            U = suivantd(L)
            D[m] = U
            m+=1
        for L in D:
            while len(L)<len(D):
                L.append(0)
            L = pousseadroite(L)
    if action == "bas":
        retourne(D)
        m = 0
        for L in D:
            U = suivantd(L)
            D[m] = U
            m+=1
        for L in D:
            while len(L)<len(D):
                L.append(0)
            L = pousseadroite(L)
        retourne(D)
    if action == "haut":
        retourne(D)
        m = 0
        for L in D:
            U = suivantg(L)
            D[m] = U
            m+=1
        for L in D:
            while len(L)<len(D):
                L.append(0)
        retourne(D)
    Z = recherchezero(D)
    if len(Z)>0:
        if D!=A:
            a = randint(0,len(Z)-1)
            (i,j) = Z[a]
            P = [2,4]
            b = randint(0,1)
            D[i][j] = P[b]

###

def meilleurmove(D):
    scorepi = [[0],[0],[0],[0]]
    a=4
    scoresuiv(D,scorepi,a)
    i=0
    while scorepi[i] != max(scorepi):
        i+=1
    actions = ["gauche","droite","haut","bas"]
    action = actions[i]
    return(action)


def scoresuiv(D,scorepi,a):
    valeurs = [[0],[0],[0],[0]]
    M = deepcopy(D)
    i=0
    calcule("gauche",M,scorepi[0])
    valeurs[0]=valeur(M,D)
    if M==D:
        scorepi[0]=[-100000000000000000000000000000000]
        a=0
    else:
        a-=1
        scoresuiv2(M,scorepi,a,i)
    M = deepcopy(D)
    i=1
    calcule("droite",M,scorepi[1])
    valeurs[1]=valeur(M,D)
    if M==D:
        scorepi[1]=[-1000000000000000000000000000000000]
        a=0
    else:
        a-=1
        scoresuiv2(M,scorepi,a,i)
    M = deepcopy(D)
    i=2
    calcule("haut",M,scorepi[2])
    valeurs[2]=valeur(M,D)
    if M==D:
        scorepi[2]=[-10000000000000000000000000000000000]
        a=0
    else:
        a-=1
        scoresuiv2(M,scorepi,a,i)
    M = deepcopy(D)
    i=3
    calcule("bas",M,scorepi[3])
    valeurs[3]=valeur(M,D)
    if M==D:
        scorepi[3]=[-10000000000000000000000000000000000]
        a=0
    else:
        a-=1
        scoresuiv2(M,scorepi,a,i)
    for i in range(4):
        scorepi[i][0]*=len(D)
        scorepi[i][0]-=2*valeurs[i]

def damier(n):
    M=[[]for i in range(n)]
    for i in range(n):
        for j in range(n):
            M[i].append(2*(i+j))
    return(M)

def scoresuiv2(M,scorepi,a,i):
    while a>0:
        actions = ["gauche","droite","haut","bas"]
        L = [[0],[0],[0],[0]]
        for z in range(3):
            U=deepcopy(M)
            calcule(actions[z],U,L[z])
        idmax=0
        for z in range(3):
            if L[z]>L[idmax]:
                idmax = z
        calcule(actions[idmax],M,scorepi[i])
        a-=1
        if not perdu(M):
            scoresuiv2(M,scorepi,a,i)
        else:
            a=0
        
def calcule(action,D,score2=score):
    if action == "gauche":
        m = 0
        for L in D:
            U = suivantg(L,score2)
            D[m] = U
            m+=1
        for L in D:
            while len(L)<len(D):
                L.append(0)
    if action == "droite":
        m = 0
        for L in D:
            U = suivantd(L,score2)
            D[m] = U
            m+=1
        for L in D:
            while len(L)<len(D):
                L.append(0)
            L = pousseadroite(L)
    if action == "bas":
        retourne(D)
        m = 0
        for L in D:
            U = suivantd(L,score2)
            D[m] = U
            m+=1
        for L in D:
            while len(L)<len(D):
                L.append(0)
            L = pousseadroite(L)
        retourne(D)
    if action == "haut":
        retourne(D)
        m = 0
        for L in D:
            U = suivantg(L,score2)
            D[m] = U
            m+=1
        for L in D:
            while len(L)<len(D):
                L.append(0)
        retourne(D)

def valeur(M,D):
    nbre = [2,4,8,16,32,64,128,256,512,1024,2048]
    places = [[],[],[],[],[],[],[],[],[],[],[]]
    valeur = 0
    for i in range(len(D)):
        for j in range(len(D)):
            for k in range(1,12):
                if M[i][j] == 2**k:
                    valeur+=nbre[k-1]*(damier(len(D))[i][j])
                    places[k-1].append((i,j))
    for u in range(11):
        int = 0
        L = places[u]
        l = len(L)
        if l>1:
            for i in range(l-1):
                for j in range(i+1,l):
                    for x in range(2):
                        int+=((L[i][x]-L[j][x])**2)*nbre[u]
        valeur+=int
    return(valeur)



###



Couleur=["#F5EFE8","#F5F0CA","#F5CEA5","#F5A167","#F58462","#CF543A","#F0F050","#099916","#209972","#257E99","#1E16FA","#8A54C4","#E45B9D","#D91214"]

class Interface(Frame):
    
    """Notre fenêtre principale.
    Tous les widgets sont stockés comme attributs de cette fenêtre."""
    
    def __init__(self, fenetre, **kwargs):
        Frame.__init__(self, fenetre, width=768, height=576, **kwargs)
        self.grid()
        
        self.ct=0
        self.c=0 
        self.v=0
        self.a=0
        
        # Création de nos widgets
        self.message = Label(self, text="Vous jouez à 2048 version 1.6.12")
        self.message.grid()
        
        self.bouton_cliquer1 = Button(self, text="Jouer à gauche", fg="blue",
                command=self.joue1)
        self.bouton_cliquer1.grid(column=1,row=4)
        
        self.bouton_cliquer2 = Button(self, text="Jouer à droite", fg="blue",
                command=self.joue2)
        self.bouton_cliquer2.grid(column=3,row=4)
        
        self.bouton_cliquer3 = Button(self, text="Jouer en bas", fg="blue",
                command=self.joue3)
        self.bouton_cliquer3.grid(column=2,row=5)
        
        self.bouton_cliquer4 = Button(self, text="Jouer en haut", fg="blue",
                command=self.joue4)
        self.bouton_cliquer4.grid(column=2,row=3)
        
        self.bouton_cliquer5 = Button(self, text="Jouer comme l'ordi", fg="orange",
                command=self.joue5)
        self.bouton_cliquer5.grid(column=2,row=4)
        
        self.bouton_cliquer6 = Button(self, text="Sauvegarder", fg="purple", command=self.sauvegarder)
        self.bouton_cliquer6.grid(column=0,row=7)
        
        self.bouton_cliquer7 = Button(self, text="Quitter", fg="red", command=self.quitter)
        self.bouton_cliquer7.grid(column=0,row=8)

        self.new_cv()
        if A==[]:
            self.new_solution()
        else:
            self.D = B
            save("derniercoup.npy",[])
        if C != []:
            score[0] = C[0]
            save("dernierscore.npy",[])
            self.actualise(self,D)
    
    def new_solution(self):
        self.new_solution=Tk()
        self.new_solution.grid()
        self.new_solution.bouton_cliquer1 = Button(self.new_solution, text="Jouer en 3*3", fg="blue",
                command=self.lance1)
        self.new_solution.bouton_cliquer1.grid(column=0,row=7)
        
        self.new_solution.bouton_cliquer2 = Button(self.new_solution, text="Jouer en 4*4", fg="blue",
                command=self.lance2)
        self.new_solution.bouton_cliquer2.grid(column=0,row=8)
        
        self.new_solution.bouton_cliquer3 = Button(self.new_solution, text="Jouer en 5*5", fg="blue",
                command=self.lance3)
        self.new_solution.bouton_cliquer3.grid(column=0,row=9)
        
        self.new_solution.bouton_cliquer4 = Button(self.new_solution, text="Jouer en 6*6", fg="blue",
                command=self.lance4)
        self.new_solution.bouton_cliquer4.grid(column=0,row=10)
    
    def actualise(self,D):
        if score[0]>meilleurscore[len(self.D)-3][0]:
            meilleurscore[len(self.D)-3][0] = score[0]
            P[len(self.D)-3][0]=score[0]
            save("meilleurscore.npy",P)
        cell_size=40
        board_size=len(self.D)
        canvas_size=cell_size*board_size
        self.canvas=Canvas(fenetre,width=canvas_size+3,height=canvas_size+3)
        self.canvas.grid(column=1,row=1)
        
        for x in range (len(self.D)):
            for y in range(len(self.D)):
                if self.D[y][x]!=0:
                    self.canvas.create_rectangle(x*cell_size+1,y*cell_size+1,x*cell_size+cell_size+1,(y+1)*cell_size+1,outline='white',fill = Couleur[int(log(self.D[y][x])/log(2))-1])
                    self.canvas.create_text((x+1/2)*cell_size,(y+1/2)*cell_size,text=self.D[y][x],fill='black')
        for x in range(len(self.D)+1):
            self.canvas.create_line(x*cell_size,0,x*cell_size,cell_size*board_size,width=2)
            self.canvas.create_line(0,x*cell_size,cell_size*board_size,x*cell_size,width=2)
        self.canvas.create_line(3,3,3,canvas_size,width=2)
        self.canvas.create_line(3,3,canvas_size,3,width=2)
        
        self.message = Label(self, text="Score: {} points".format(score[0]))
        self.message.grid(column=4, row =1)
        
        self.message = Label(self, text="Meilleur score: {} points".format(meilleurscore[len(self.D)-3][0]))
        self.message.grid(column=4, row =0)
        
        self.message = Label(self, text="Victoires: {}".format(V[len(self.D)-3][0]))
        self.message.grid(column=4, row =3)
        
        if perdu(self.D):
            self.lose()
        if self.v==0:
            if victoire(D):
                self.victory()
        if self.c==1:
            self.new_solutions.destroy()
        self.c+=1

    def joue1(self):
        joue("gauche",self.D)
        self.actualise(self.D)
    
    def joue2(self):
        joue("droite",self.D)
        self.actualise(self.D)
    
    def joue3(self):
        joue("bas",self.D)
        self.actualise(self.D)
    
    def joue4(self):
        joue("haut",self.D)
        self.actualise(self.D)
    
    def joue5(self):
        joue(meilleurmove(self.D),self.D)
        self.actualise(self.D)
    
    def lance1(self):
        self.D = jeurandom(3)
        self.actualise(self.D)
        self.new_solution.destroy()
    
    def lance2(self):
        self.D = jeurandom(4)
        self.actualise(self.D)
        self.new_solution.destroy()
        
    def lance3(self):
        self.D = jeurandom(5)
        self.actualise(self.D)
        self.new_solution.destroy()
        
    def lance4(self):
        self.D = jeurandom(6)
        self.actualise(self.D)
        self.new_solution.destroy()
    
    def sauvegarder(self):
        save("derniercoup.npy",self.D)
        save("dernierscore.npy",score)
        self.actualise(self.D)
        self.c=0
        self.v=0
        fenetre.destroy()
    
    def quitter(self):
        self.actualise(self.D)
        fenetre.destroy()
    
    def new_cv(self):
        self.new_solutions=Tk()
        self.new_solutions.message = Label(self.new_solutions, text="Bonjour,\nDepuis peu ce programme propose un bouton pour jouer le meilleur coup possible, attention la machine ne suit pas de stratégie précise et peut se suicider! \n\nSi vous constatez un problème, une erreur,ou pour une quelconque suggestion, n'hésitez pas a nous contacter sur nos adresses mail:\nhippo.gobet@gmail.com\neliott.pollice@gmail.com\n\nAmusez vous bien!\nCordialement,\nLe support technique.")
        self.new_solutions.message.grid()
    
    def lose(self):
        if self.ct==0:
            self.perte=Tk()
            self.perte.message = Label(self.perte, text = "T'es naze\n\nTon score final est de {}".format(score[0]))
            self.perte.message.grid()
            self.perte.bouton_cliquer = Button(self.perte, text="Recommencer", fg="red",
                    command=self.recommencer1)
            self.perte.bouton_cliquer.grid(column=0,row=1)
            self.ct+=1
        
    def victory(self):
        if self.ct==0:
            self.gagne=Tk()
            self.gagne.message = Label(self.gagne, text = "Bravoooooo tu as gagné !\n\nTon score final est de {}\n\nPartage le sur les résaux !".format(score[0]))
            self.gagne.message.grid()
            self.gagne.bouton_cliquer = Button(self.gagne, text="Recommencer", fg="red",
                command=self.recommencer2)
            self.gagne.bouton_cliquer.grid(column=0,row=2)
            self.gagne.bouton_cliquer1 = Button(self.gagne, text="Continuer", fg="blue",
                command=self.continuer)
            self.gagne.bouton_cliquer1.grid(column=0,row=1)
            self.ct+=1
            if self.a == 0:
                V[len(self.D)-3][0] += 1
                save("victoires.npy",V)
            self.a = 1
        
    def recommencer1(self):
        self.D=jeurandom(len(self.D))
        score[0] = 0
        self.actualise(self.D)
        self.perte.destroy()
        self.ct=0
        self.v=0
        self.a=0
        A = []
        C = []
        save("derniercoup.npy",A)
        save("dernierscore.npy",C)
    
    def recommencer2(self):
        self.D=jeurandom(len(self.D))
        score[0] = 0
        self.actualise(self.D)
        self.gagne.destroy()
        self.ct=0
        self.v=0
        self.a = 0
        A = []
        C = []
        save("derniercoup.npy",A)
        save("dernierscore.npy",C)
    
    def continuer(self):
        self.gagne.destroy()
        self.ct=0
        self.v=1



fenetre = Tk()
interface = Interface(fenetre)

interface.mainloop()
