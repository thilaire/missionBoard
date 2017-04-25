# Fonctionnalités

## Oxygène
Oxygène dans la navette spatiale

- bargraph indiquant le niveau
- bouton "pompe oxygène" :
  - active la pompe pendant 15s (bruit + led clignotante bleue + augmentation du niveau)
  - voyant bleu clignotant qd la pompte fonctionne, éteind sinon
  - voyant rouge clignotant si la pompe ne fonctionne plus ()
  
  
  
  
  
  
# notes diverses  
MissionBoard

8 switchs 3 pos. :
navette/ordinateur/jeux
Com1/off/Com2
Lumières
Pompe Toilettes/eau
Pompe moteurs/carburant 1 et 2
Ordinateur de secours

8 boutons :
Moteur principal 1
Moteurs auxiliaires 2
Parachute
Freinage
Pilote automatique
Pompe oxygène 
Ouverture sas/porte
Train d'atterrissage 

3 missile switch + gros bouton :
trois phases pour le décollage

2 bargraph :
oxygène 
Carburant

Fonctionnalités
sas/porte
Oxygene
Carburant (booster, fusée, navette)
Communication
Séquence de lancement (missile switch+gros bouton)


RPi i/o:
4 pour les deux TM1638 (clk+data, et un Enable par TM)
4 pour le joystick
6 pour les boutons jeux/commande
le gros boutons

1er TM1638:
2 afficheurs 4x7seg. (1 sur la carte, 1 à côté)
4 switch 3 positions
8 leds (4 switchs 3 pos)
2eme TM1638:
1 afficheur 7seg.
2 bargraph 10seg.
2 boutons jeux/commande
3 switchs 3 pos (sans led?) v  