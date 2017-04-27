# Fonctionnalités

## Oxygène
Oxygène dans la navette spatiale
- bargraph indiquant le niveau
- bouton "pompe oxygène" :
  - active la pompe pendant 15s (bruit + led clignotante bleue + augmentation du niveau)
  - voyant bleu clignotant qd la pompte fonctionne, éteind sinon
  - voyant rouge clignotant si la pompe ne fonctionne plus (réparable en activant l'ordinateur de secours)
- voyant "oxygène" (peut être supprimé, redondant avec bargraph):
    - vert si le niveau est ok
    - orange clignotant si niveau bas
    - rouge si niveau dangereux
  
## Démarrage
Démarrage du RPi
- clé  
- led verte (directement alimentée sur le 5V du RPi), à côté de la clé
- switch 3 positions : jeux, ordinateur, navette
- prise jack d'alimentaiton générale (chassis)  
  
## Audio
Son par le haut-parleur ou le casque
- haut-parleurs (TODO)
- prises casque et/ou micro (TODO)
- swith 2 positions : COM1 (du son enregistré avec la base) / off (pas de communication radio)
- bouton poussoir pour parler ??
- potentiomètre pour le volume ? (volume software ou hardware??)

TODO: mono (HP, casque, micro) ? ou bien stéréo ?
1 possibilité : HP en mono, 1 prise pour le casque micro mono, et 1 prise jack pour l'audio (pas de micro dans ce cas)

## Portes/sas  
Ouverture du sas (2 portes) + schéma?
- switch rotatif 3 positions : porte 1 (pos 1)/ sas fermé (pos 2)/ porte 2 (pos 3)
   - les deux portes ne peuvent être ouvertes en même temps
   - (2) -> (3) pompe oxygène 10s (niveau augmente) puis ouverture porte 2  
   - (3) -> (2) fermeture porte 2 puis pompe à oxygène 10s (niveau oxygène diminue) 
   - (1) -> (2) fermeture porte 1
   - (2) -> (1) ouverture porte 1
- deux voyant lumineux pour les portes:
  - porte 1 : vert qd porte fermée, orange clignotante qd fermeture/ouverture, jaune qd porte ouverte
  - porte 2 : vert qd porte fermée, orange clignotante qd fermeture/ouverture et rouge clignotant qd porte fermée
- l'ouverture/fermeture de porte dure pendant 5s -> son
- tout s'arrête, voyant qui clignotent en rouge (+ message sonore alerte) si on passe trop vite de (1)<->(2)<->(3), ne s'arrête que si repassé en position (2)

## Lumière
Allume ou éteind les lumières de la navette (peut ne pas être connecté)
- switch on/off pour la lumière dans la navette
- led verte associée

## Pompe eau
déclenche la pompe à eau (toilette)
- switch on/off
- bruit associé

## Ordinateur de bord
Gestion de l'ordinateur de bord et des pannes
- switch ordinateur de bord / ordinateur de secours
- voyant lumineux
  - vert qd ordinateur de bord et que tout va bien
  - rouge qd ordinateur de bord en panne (+ message audio?)
  - orange qd on a basculé sur l'ordintaeur de secours
  - clignotant quelques secondes pour simuler le temps de reboot

## Altitude/Vitesse
Trois groupes d'afficheur 7-seg
- deux afficheurs pour la position (position/altitude) (on est bien d'accord que ça n'a pas de sens)
- un pour la vitesse

 
## Compte à rebours - durée mission
Huit afficheurs 7-segments (2 groupes de 4 collés).
Deux fonctions
- compte à rebours (décompte 20s qd il est déclenché, avec les centièmes de sec; clignote qd on arrive à zéro si on n'a pas lancé)
- puis compte la durée de la mission (ne peut être remis à zéro qu'à l'atterrissage)

## Électricité
- Séries de switchs, avec sa led 
  - panneaux solaires (on/off), led verte en direct
  - batteries (on/off), led verte
  - piles à combustible (on/off), led verte
- voyant lumineux "électricité" -> vert qd tout est ok, orange si un seul élément de branché, rouge si tout est à off

Si tout est à off, le panneau s'éteind, saut le voyant lumineux "électricité" qui passe au rouge (+ son alerte). On perd la batterie au bout de 5min, et la piles à combustible au bout de 15min ?

## Carburant



  
# I/O (remplis au fur et à mesure des fonctionalités)

##### Bargraphs (max 4, dont 3 panneau haut) :
- niveau Oxygène
  
##### Blocs de 4 afficheurs 7-segment (max 3 panneau haut, 4 bas):
- vitesse
- position
- altitude
- compte à rebours (x2)
  
##### Leds :
- démarrage
- lumière
- panneau solaire
- batteries
- pile à combustible


##### Switch 2 positions (max 10) :
- audio COM1/Off
- lumière
- pompe eau
- ordinateur de bord/de secours
- panneau solaire
- batteries
- piles à combustible 


##### Switch 3 positions (max 10) :
- démarrage (jeux/ordinateur/navette)

##### Boutons poussoirs (max 10 normaux + 1 gros) :
- pompe oxygène
- micro ?  
  
##### Voyants lumineux (12 ?) :
  - oxygène  
  - porte 1
  - porte 2
  - électricité
  
##### Potentiomètres (1 en ligne, max 5 rotatif) :
- son ?

##### Clé (1) :
  - démarrage du Rpi

##### Switch rotatif 3 positions (max 2): 
- sas

#### Autres :
- Joystick :
- Hauts-parleurs : son
- Prises USB :
- Prises audio Jack 3.5mm : son
- Prise alimentation (sur chassis) : démarrage
  
  
  
  
  
  
  
  
  
  
# notes diverses  
MissionBoard

####8 switchs 3 pos. :
+ navette/ordinateur/jeux
+ Com1/off/Com2
+ Lumières
+ Pompe Toilettes/eau
- Pompe moteurs/carburant 1 et 2
+ Ordinateur de secours

####8 boutons :
- Moteur principal 1
- Moteurs auxiliaires 2
- Parachute
- Freinage
- Pilote automatique
+ Pompe oxygène 
+ Ouverture sas/porte
- Train d'atterrissage 

####3 missile switch + gros bouton :
trois phases pour le décollage

####2 bargraph :
+ oxygène 
- Carburant

###Fonctionnalités
+ sas/porte
+ Oxygene
- Carburant (booster, fusée, navette)
+ Communication
- Séquence de lancement (missile switch+gros bouton)


###RPi i/o:
- 5 pour les trois TM1638 (clk+data, et un Enable par TM)
- 4 pour le joystick
- 6 pour les boutons jeux/commande
- 1 pour le gros bouton
- 2 pour le switch jeu/navette/ordinateur
- 2 (ou plus) pour le µC (leds WQ2812b, potentiomètres analogiques)

###RPi USB:
- 1 ou 2 ports libres (souris, clavier, joystick, etc.)
- 1 port touchscreen du LCD
- 1 port carte son ?
- 1 port pour carte USB I/O (Zero delay arcade) ?



####1er TM1638:
2 afficheurs 4x7seg. (1 sur la carte, 1 à côté)
4 switch 3 positions
8 leds (4 switchs 3 pos)
2eme TM1638:
1 afficheur 7seg.
2 bargraph 10seg.
2 boutons jeux/commande
3 switchs 3 pos (sans led?) v  