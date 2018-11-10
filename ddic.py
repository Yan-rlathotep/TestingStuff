import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib.patches as patches
from cards import *
from Events import *
plt.rcParams['image.cmap'] = 'gray'

ressources=['UM','fossile','électricité','nourriture','déchets','pollution']
jauges=['Economique','Environnemental','Social']
cols_mod = ['#8321d2','#1ca200','#af1d1d']
cols_mod_light = ['#e7d5ff','#dcffd5','#ffd5d5']
cols_res = ['#ffc800','#000000','#55bcff','#ff0000','#954e00','#8d8d8d']

    
# traitement des images

def load_image(name,crop_window=-1): 
    I=plt.imread(name)
    if crop_window!=-1:
        I=I[crop_window[0]:crop_window[1],crop_window[2]:crop_window[3]]
    I=I.astype('float')
    #if len(I.shape)>2 and I.shape[2]==3:
        #I=0.2989 * I[:,:,0] + 0.5870 * I[:,:,1] + 0.1140 * I[:,:,2]
    return I

def resize(name):
    I=load_image(name)
    # bande supérieure
    i=0
    j=I.shape[1]//2
    while I[i,j,0]==1:
        i+=1
    I=I[i:,:,:]
    # bande gauche
    j=0
    while I[i,j,0]==1:
        j+=1
    I=I[:,j:,:]
    # bande droite
    j=I.shape[1]-1
    while I[i,j,0]==1:
        j-=1
    I=I[:,:j+1,:]
    # bande inférieure
    i=I.shape[0]-1
    while I[i,j,0]==1:
        i-=1
    I=I[:i+1,:,:]
    plt.imsave(name,I,dpi=500)
    #plt.imshow(I)
    #plt.show()
    
    
def cm2inch(*tupl): # Conversion de cm vers inch
    inch = 2.54
    if isinstance(tupl[0], tuple):
        return tuple(i/inch for i in tupl[0])
    else:
        return tuple(i/inch for i in tupl)

W,H = cm2inch(21,29.7) # Dimensions d'une feuille A4
w,h = cm2inch(4.2,6.4) # Dimensions des cartes

def cards_grid():
    Nx = int(W//w)
    Ny = int(H//h)
    dx = (W%w)/(Nx+1)
    dy = (H%h)/(Ny+1)
    pos = []
    for ny in range(Ny):
        for nx in range(Nx):
            pos.append((dx + nx*(w + dx),H - dy - ny*(h + dy)))
    return pos

side = h/32
def disp_squares(x,y,n,color,subplot):
    for k in range(n):
        subplot.add_patch(patches.Rectangle((x+1.8*k*side,y),side,side,facecolor=color,linewidth=0.5))

def cut(string,n_char):
    i = min(n_char,len(string)-1)
    while string[i] != ' ' and i>=0:
        i -= 1
    return i

def write(x0,y0,string,fontsize,dy,n_char,latex=False):
	lines = []
	n = 0
	while len(string) > n_char:
		n = cut(string,n_char)
		lines.append(string[:n])
		string = string[n+1:]
	lines.append(string)
	for i in range(len(lines)):
		#if latex:
			#for k in range(len(lines[i])):
				#if lines[i][k] == ' ':
					#lines[i][k] = '~'
			#lines[i] = '$'+lines[i]+'$'
		plt.text(x0,y0 - i*dy,lines[i],fontsize = fontsize)

def trace_card(x0,y0,name,subplot):
    card=load_card(name)
    
    Nom=card['Nom']
    Type=card['Type']
    Cout=card['Cout']
    Desc=card['Description']
    Cons=card['Consommation']
    Prod=card['Production']
    Ere=card['Ere']
    Mod=card['Modificateurs']
    Nbex=card['Exemplaires']

    if Type == 'i':
    	Type = 'Infrastructures'
    elif Type == 'a':
    	Type = 'Accords'
    else:
    	Type = 'Décision'

    h0,h1,h2,h3,h4,h5,h6,h7,h8 = y0,y0-2*h/16,y0-3*h/16,y0-4*h/16,y0-9*h/16,y0-10*h/16,y0-11*h/16,y0-15*h/16,y0-h
    plt.plot([x0,x0+w,x0+w,x0,x0],[y0,y0,y0-h,y0-h,y0],color = 'k') #Contours
    subplot.add_patch(patches.Rectangle((x0,h1),w,h0-h1,facecolor='#fdffca'))
    plt.plot([x0,x0+w],[h1,h1],color='k',linewidth=0.8) #Cout/nom
    plt.plot([x0+2*w/10,x0+3*w/10],[h1,h0],color='k',linewidth=0.5)
    plt.plot([x0+5*w/10,x0+6*w/10,x0+w],[h1,h2,h2],color='k',linewidth=0.5) #Type
    plt.plot([x0,x0+2.2*w/10,x0+3.2*w/10],[h2-h/46,h2-h/46,h1],color='k',linewidth=0.5) #Ere
    plt.plot([x0+w/10,x0+9*w/10,x0+9*w/10,x0+w/10,x0+w/10],[h3,h3,h4,h4,h3],color='k',linewidth=0.5) #Texte
    plt.plot([x0,x0+4*w/10,x0+5*w/10,x0+6*w/10,x0+w],[h5,h5,h6,h5,h5],color='k',linewidth=0.5) #Consommation/production
    plt.plot([x0,x0+w],[h6,h6],color='k',linewidth=0.5)
    plt.plot([x0+w/2,x0+w/2],[h6,h7],color='k',linewidth=0.8)
    plt.plot([x0,x0+w],[h7,h7],color='k',linewidth=0.8) #Modificateurs
    subplot.add_patch(patches.Rectangle((x0,h8),w,h7-h8,facecolor='#e3e3e3'))
    plt.plot([x0+w/3,x0+w/3],[h7,h8],color='k',linewidth=0.8)
    plt.plot([x0+2*w/3,x0+2*w/3],[h7,h8],color='k',linewidth=0.8)
    
    plt.text(x0 + 1.5*w/20,h0 - 1.3*h/15,str(Cout),fontsize = 9)
    if len(Nom) < 10:
        plt.text(x0 + 3.5*w/10,h0 - 1.3*h/15,Nom,fontsize = 9)
    else:
        if len(Nom) < 15:
            plt.text(x0 + 3.5*w/10 - h/100,h0 - 1.3*h/15 + h/150,Nom,fontsize = 7)
        else:
            esp = cut(Nom,14)
            if esp == -1:
                Nom = 'XXXXXXXXXXXX'
            plt.text(x0 + 3.5*w/10,h0 - 1.3*h/15 + h/30,Nom[:esp],fontsize = 6)
            plt.text(x0 + 3.5*w/10,h0 - 1.3*h/15 - h/60,Nom[esp+1:],fontsize = 6)
    plt.text(x0 + 2*w/20 + + (3-Ere)*w/90,h1 - h/15.5,Ere*'I',fontsize = 8)
    plt.text(x0 + 6.3*w/10 + (16-len(Type))*w/150,h1 - 0.65*h/15,Type,fontsize = 4)
    write(x0 + 2.7*w/20,h3 - h/20,Desc,5,h/25,22)
    plt.text(x0 + 0.8*w/20,h5 - 0.65*h/15,'Consommation',fontsize = 4)
    plt.text(x0 + 12.8*w/20,h5 - 0.65*h/15,'Production',fontsize = 4)
    
    i = 0 #Affichage de la consommation
    for k in range(6):
        res = Cons[k]
        if res:
            i+=1
            yi = h6 - i*h/18
            plt.text(x0 + 0.5*w/10,yi,'-',fontsize = 8)
            if res < 5:
                disp_squares(x0 + 1.2*w/10,yi,res,cols_res[k],subplot)
            else :
                disp_squares(x0 + 1.2*w/10,yi,1,cols_res[k],subplot)
                plt.text(x0 + 1.2*w/10 + 2*side,yi + side/10,'x',fontsize = 5)
                plt.text(x0 + 1.2*w/10 + 3.5*side,yi,str(res),fontsize = 6)
    i = 0 #Affichage de la production
    for k in range(6):
        res = Prod[k]
        if res:
            i+=1
            yi = h6 - i*h/18
            plt.text(x0 + w/2 + 0.5*w/10,yi + side/8,'+',fontsize = 5)
            if res < 5:
                disp_squares(x0 + w/2 + 1.2*w/10,yi,res,cols_res[k],subplot)
            else :
                disp_squares(x0 + w/2 + 1.2*w/10,yi,1,cols_res[k],subplot)
                plt.text(x0 + w/2 + 1.2*w/10 + 2*side,yi + side/10,'x',fontsize = 5)
                plt.text(x0 + w/2 + 1.2*w/10 + 3.5*side,yi,str(res),fontsize = 6)

    for k in range(3):
        mod = Mod[k]
        if mod > 0:
            subplot.add_patch(patches.Rectangle((x0+k*w/3,h8),w/3,h/16,facecolor=cols_mod[k]))
            plt.text(x0 + w/8 + k*w/3,h7 - h/22,'+' + str(mod),fontsize = 6,color = 'w')
        elif mod < 0:
            subplot.add_patch(patches.Rectangle((x0+k*w/3,h8),w/3,h/16,facecolor=cols_mod[k]))
            plt.text(x0 + w/8 + k*w/3,h7 - h/22,'–' + str(-mod),fontsize = 6,color = 'w')

def trace_event(x0,y0,name,subplot):
	
    event = load_event(name)
    Nom=event['Nom']
    Type=event['Type']
    Piste=event['Piste']
    Agreg=event['Agreg']
    Ere=event['Ere']
    Seuils=event['Seuils']
    Desc=event['Description']
    Nbex=event['Exemplaires']
    n_seuils = len(Seuils)
    
    h0,h1,h3,h4 = y0,y0-2*h/16,y0-15*h/16,y0-h
    h2 = [h1 + k*(h3-h1)/n_seuils for k in range(1,n_seuils)]
    plt.plot([x0,x0+w,x0+w,x0,x0],[y0,y0,y0-h,y0-h,y0],color = 'k') #Contours
    subplot.add_patch(patches.Rectangle((x0,h1),w,h0-h1,facecolor='#fdffca'))
    plt.plot([x0,x0+w],[h1,h1],color='k',linewidth=0.8) #Ere/nom
    plt.plot([x0+2*w/10,x0+3*w/10],[h1,h0],color='k',linewidth=0.5)
    subplot.add_patch(patches.Rectangle((x0,h3),w/5,h1-h3,facecolor=cols_mod[Piste],linewidth=0.5)) #Coloriage desc
    subplot.add_patch(patches.Rectangle((x0+w/5,h3),4*w/5,h1-h3,facecolor=cols_mod_light[Piste],linewidth=0.5))
    for y in h2:
    	plt.plot([x0,x0+w],[y,y],color='k',linewidth=0.5) #Desc
    plt.plot([x0+w/5,x0+w/5],[h1,h3],color='k',linewidth=0.5)
    plt.plot([x0,x0+w],[h3,h3],color='k',linewidth=0.8) #Caracteristiques
    plt.plot([x0+w/2,x0+w/2],[h3,h4],color='k',linewidth=0.8)
    
    
    if len(Nom) < 8:
        plt.text(x0 + 3.5*w/10,h0 - 1.3*h/15,Nom,fontsize = 9)
    else:
        if len(Nom) < 13:
            plt.text(x0 + 3.5*w/10 - h/100,h0 - 1.3*h/15 + h/150,Nom,fontsize = 7)
        else:
            esp = cut(Nom,12)
            if esp == -1:
                Nom = 'XXXXXXXXXXXX'
            plt.text(x0 + 3.5*w/10,h0 - 1.3*h/15 + h/30,Nom[:esp],fontsize = 6)
            plt.text(x0 + 3.5*w/10,h0 - 1.3*h/15 - h/60,Nom[esp+1:],fontsize = 6)
    plt.text(x0 + 1.7*w/20 + (3-Ere)*w/80,h0 - 1.3*h/15,Ere*'I',fontsize = 9)
    
    for k in range(n_seuils):
    	latex = False
    	if Seuils[k] == 'min':
    		string = 'min'
    	elif Seuils[k] == 'effet':
    		string = ''
    		latex = True
    	else:
    		string = '$\leq$ ' + str(Seuils[k])
    	plt.text(x0+w/40,([h1]+h2)[k]-0.4*h/n_seuils,string,fontsize = 7)
    	write(x0+1.1*w/5,([h1]+h2)[k]-0.15*h/n_seuils,Desc[k],6,0.8*h/16,20,latex)
    
    if Agreg == 'm': #Moyenne vs Individuel
    	col = '#f88200'
    	Agreg = 'Moyenne'
    else:
    	col = '#ce69d3'
    	Agreg = 'Individuel'
    subplot.add_patch(patches.Rectangle((x0,h4),w/2,h/16,facecolor=col,linewidth=0.8))
    plt.text(x0+w/12+(10-len(Agreg))*w/150,h3-h/22,Agreg,fontsize=6,color='w')
    if Type == 'n': #Normal vs Final
    	col = '#008eea'
    	Type = 'Normal'
    else:
    	col = '#e50000'
    	Type = 'Final'
    subplot.add_patch(patches.Rectangle((x0+w/2,h4),w/2,h/16,facecolor=col,linewidth=0.8))
    plt.text(x0+w/2+w/8+(6-len(Type))*w/24,h3-h/22,Type,fontsize=6,color='w')
	

def print_deck(deck,events = False,save = False):
	prefix = 'Planche '
	if events:
		prefix += 'events '
	
	fig = plt.figure(figsize=(W,H))
	ax = fig.add_subplot(111,aspect = 'equal')
	plt.axis('equal')
	plt.axis('off')
	plt.plot([0,W,W,0,0],[H,H,0,0,H],color='k')

	testcard = ['USINES','Infrastructure',13,'blabla',[0,1,3,0,0,0],[6,0,0,2,1,1],2,[1,0,-4],10]

	testevent = ["VAGUE DE CHALEUR",'Final',0,'Moyenne',3,[7,4,'min'],["Perdez 2 productions de (nourriture)","Bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla",""],1]

	grid = cards_grid()
	
	pos = 0
	page = 1
	for i in range(deck.shape[0]):
		if events:
			card = load_event(deck[i])
		else:
			card = load_card(deck[i])
		Nbex=card['Exemplaires']
		for j in range(Nbex):
		  if pos > 15:
		    pos = 0
		    if save:
			    filename = prefix + str(page)
			    plt.savefig(filename + '.png',format='png',dpi=500)
			    resize(filename + '.png')
		    else:
			    plt.show()
		    page += 1
		    plt.cla() #Nettoyage de la page
		    plt.axis('equal')
		    plt.axis('off')
		    plt.plot([0,W,W,0,0],[H,H,0,0,H],color='k')
		  if events:
		  	trace_event(grid[pos][0],grid[pos][1],deck[i],ax)
		  else :
		  	trace_card(grid[pos][0],grid[pos][1],deck[i],ax)
		  pos += 1

	if save:
		filename = prefix + str(page)
		plt.savefig(filename + '.png',format='png',dpi=500)
		resize(filename + '.png')
	else:
		plt.show()