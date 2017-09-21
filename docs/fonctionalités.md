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
+ clé  
+ led verte (directement alimentée sur le 5V du RPi), à côté de la clé
+ switch rotatif 3 positions : navette, jeux, ordinateur
+ prise jack d'alimentaiton générale (chassis)  

  (le switch rotatif peut avoir une 4ème position bonus)

## Audio
Son par le haut-parleur ou le casque
- haut-parleurs (TODO)
- prises casque et/ou micro (TODO)
- swith 3 positions : COM1 (du son enregistré avec la base) / off (pas de communication radio) / COM2 (autre son)
- bouton poussoir pour parler ??
- potentiomètre pour le volume ? (volume software ou hardware??)

TODO: mono (HP, casque, micro) ? ou bien stéréo ?
1 possibilité : HP en mono, 1 prise pour le casque micro mono, et 1 prise jack pour l'audio (pas de micro dans ce cas)

## Portes/sas  
Ouverture du sas (2 portes) + schéma?
- switch 3 positions : porte 1 (pos 1)/ sas fermé (pos 2)/ porte 2 (pos 3)
   - les deux portes ne peuvent être ouvertes en même temps
   - (2) -> (3) pompe oxygène 10s (niveau augmente) puis ouverture porte 2  
   - (3) -> (2) fermeture porte 2 puis pompe à oxygène 10s (niveau oxygène diminue) 
   - (1) -> (2) fermeture porte 1
   - (2) -> (1) ouverture porte 1
- deux voyant lumineux pour les portes:
  - porte 1 : vert qd porte fermée, orange clignotante qd fermeture/ouverture, jaune qd porte ouverte
  - porte 2 : vert qd porte fermée, orange clignotante qd fermeture/ouverture et rouge clignotant qd porte fermée

L'ouverture/fermeture de porte dure pendant 5s (+ son)
Tout s'arrête, voyant qui clignotent en rouge (+ message sonore alerte) si on passe trop vite de (1)<->(2)<->(3), ne s'arrête que si repassé en position (2)

## Lumière
Allume ou éteind les lumières de la navette (éventuellement peut ne pas être connecté)
- switch on/off pour la lumière dans la cabine
- switch on/off pour la lumière extérieure
- leds vertes associées (s'allume en on, sauf si il n'y a plus d'électricité)

## Pompe eau
déclenche la pompe à eau (toilette)
- switch 3 pos. eau / off / toilettes 
- bruit associé (chasse d'eau ou pompe)

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

## Laser
- missile swith pour armer le laser
- switch 2 positions pour la couleur du laser (bleu/rouge)
- un bouton lumineux pour tirer
  - passe au rouge ou bleu qd armé
  - fait du son qd on tire

 
## Compte à rebours - durée mission
Huit afficheurs 7-segments (2 groupes de 4 collés).
Deux fonctions
- compte à rebours (décompte 20s qd il est déclenché, avec les centièmes de sec; clignote qd on arrive à zéro si on n'a pas lancé)
- puis compte la durée de la mission (ne peut être remis à zéro qu'à l'atterrissage)

## Électricité
Gestion de l'électricité produite
- Séries de switchs, avec sa led 
  - panneaux solaires (on/off), led verte en direct
  - batteries (on/off), led verte
  - piles à combustible (on/off), led verte
- voyant lumineux "électricité" -> vert qd tout est ok, orange si un seul élément de branché, rouge si tout est à off

Si tout est à off, le panneau s'éteind, saut le voyant lumineux "électricité" qui passe au rouge (+ son alerte). On perd la batterie au bout de 5min, et la piles à combustible au bout de 15min ?


## Carburant
Gestion du carburant
- deux bargraph : moteurs fusée, moteurs navette/vaisseau (ou bien moteur 1 et moteur 2)
- switch 3 pos. pompe fusée / off / pompe vaisseau (ne sert qu'avant le décollage)
- deux leds (vertes) allumée qd le remplissage s'effectue (1 led en face de "pompe fusée", l'autre pour "pompe vaisseau"), puis s'éteind qd le remplissage est fini (10s ?)

Le carburant fusée se vide rapidement après décollage (1min?), le carburant navette se vide en fct de la puissance moteurs
Les bargraph carburant moteurs clignotent en rouge qd plus de carburant

## Pilote automatique
- switch pilote automatique / commandes manuelles
- voyant lumineux "pilote automatique"
  - en vert quand enclenché
  - éteind qd mis sur off (ou en bleu)
  - passe en orange en cas de problème (doit être désactivé, ou bien on passe sur l'ordinateur de secours)
- active la LED "commandes manuelles" qd on n'est pas en pilote automatique
 
Le pilote automatique fait bouger doucement les compteurs d'altitude/position et vitesse en mode "stationnaire" (ou bcp en mode "décollage"/"atterissage").
Les commandes manuelles font bouger les compteurs altitude/position/vitesse plus vite

## Commande manuelles
- joystick
- potentiomètre linéaire : puissance moteurs
- 2 potentiomètres : lacet/roulis
- LED verte allumée qd mode "commande manuelle"

-> influent sur les compteurs vitesse/position/altitude en mode "commandes manuelles" (et sur la vitesse de consommation carburant ?)

# Alarme
- voyant lumineux alarme
  - éteint lorsqu'un aucun problème
  - rouge (clignotant ou non) lorsque problème, avec signal sonore
le voyant s'allumera lorsque qu'une panne sera détectée (simulée), en complément d'un autre voyant indiquant le pb


## Moteurs
- voyant lumineux de survitesse (qd vitesse trop grande ou >50 en fin d'atterrissage)
- bouton moteurs fusée
- bouton moteurs navette
- potentiomètre en ligne pour régler la puissance des moteurs
- 2 switchs pour le turbo (gaz tuyères et boost)
  -> change la vitesse, c'est tout
- 2 leds associées
Lien avec le carburant


## train d'atterrissage
- bouton poussoir train
  - un appui pour le sortir (10s en oragne le temps qu'il sorte + son, et ensuite en vert pour dire qu'il est sorti)
  - un appui pour le rentrer (idem, voyant éteind qd il est rentré)

Utilisable uniquement pendant le mode d'atterissage (sinon inactif, ou bien provoque une alarme de quelques secondes: voyant alarme + voyant du bouton en rouge clignotant 5s)


## Pilotage
- un bouton rotatif 3 pos. permet de choisir le mode
  - décollage
  - orbite
  - atterrissage
- 3 voyants lumieux (décollage/orbit/atterrissage) pour indiquer dans quel état on est

l'alarme retentit (+son?) et le voyant correspondant passe en orange (rouge?) si on change de mode alors qu'une séquence n'est pas terminée (tant qu'on n'est pas revenu dans le bon mode) 

### Décollage
Séquence à suivre (pour finir le décollage et passer à un autre mode) :
- enclencher le bouton rocket "Phase 1" (ou "début séquence décollage")
- mettre tous les niveaux (carburant et oxygène) à max pour passer à la phase suivante
- enclencher le bouton rocket "Phase 2" (ou "Préchauffage des moteurs")
  - erreur si les niveaux ne sont pas à max et bouton "Phase 1" enclenché
- activer le moteur fusée (bouton poussoir, qui passe en bleu si c'est ok)
- fermeture du sas
- pilote automatique enclenché
- enclencher le bouton rocket "Phase 3" (ou "Paré au décollage")
  - erreur si moteur fusée non activé, sas non fermé, pilote auto non enclenché
- le compte à rebours se déclenche (avec son?)
- il faut appuyer sur le bouton rouge Go!
- décollage en cours (les moteurs s'allument, donc voyant moteur qui clignote/change de couleur, altitude qui augmente, carburant fusée qui diminue)
- au bout de 30s on peut décrocher la fusée (bouton "décrochage fusée" qui clignote qd c'est près, qui passe au rouge qd ça se fait, et puis s'éteind)
- il faut allumer les moteurs de la navette (bouton "moteur navette", qui clignote qd c'est près, passe au vert qd ils s'allument, carburant moteur diminue)
- la séquence est finie (voyant qui clignote ?), on peut passer au mode "orbite"

### Orbite 
Mode normal
- on peut passer en pilote manuel, augmenter la puissance, piloter avec le joystick, etc.

### Atterrissage
Séquence à suivre:
- allumage des moteurs navette (bouton moteurs navette)
- pilote automatique
- sortie du train d'atterrissage (bouton train aterrissage)
- maintenir le lacet/roulis autour de zéro (potards) ???? voyant 
- diminuer la vitesse qd altitude <50 (sinon voyant survitesse en rouge + clignotement afficheur vitesse)
- qd altitude arrive à zero, il faut sortir le parachute (bouton parachute, passe en vert quand ouvert)
- freinage (bouton poussoir freinage)
- extinction des moteurs

  
# I/O (remplis au fur et à mesure des fonctionalités)

#### Bargraphs (max 4, dont 3 panneau haut) :
+ niveau Oxygène
+ niveau carburant fusée
+ niveau carburant navette
  
#### Blocs de 4 afficheurs 7-segment (max 3 panneau haut, 4 bas):
- vitesse
- position
- altitude
+ compte à rebours (x2), panneau bas
- lacet/roulis ???
  
#### Leds :
+ démarrage (directe sur Alim)
+ lumière cabine
+ lumière extérieure
+ panneau solaire (en directe sur switch associé ?)
+ batteries
+ pile à combustible
- pompe carburant fusée
- pompe carburant navette
+ commandes manuelles


#### Switch 2 positions (max 10) :

+ lumière cabine
+ lumière extérieure
+ ordinateur de bord/de secours
+ panneau solaire
+ batteries
+ piles à combustible
+ pilote automatique/commandes manuelles
+ couleur de laser

+ turbo gaz tuyères
+ turbo boost



#### Switch 3 positions (max 10) :
+ sas (porte 1 / sas fermé / porte 2)
+ pompe eau (eau/off/toilettes)
+ pompe carburant (réservoir fusée/off/réservoir navette)
+ audio COM1/Off/COM2

#### Boutons poussoirs (max 10 normaux + 1 gros) :
+ pompe oxygène
+ moteurs fusée
+ décrochage fusée
+ moteurs navette
+ Go! (gros bouton rouge)
+ train d'atterissage
+ ouverture parachute
+ freinage
+ laser
  
#### Voyants lumineux (12 ?) :
+ oxygène  
+ porte 1
+ porte 2
+ électricité
+ pilote automatique
+ alarme/anomalie
+ décollage
+ orbite
+ atterrissage
+ indicateur de survitesse
  
  
#### Potentiomètres (1 en ligne, max 5 rotatif) :
+ son
+ puissance moteurs (en ligne)
+ lacet
+ roulis

#### Clé (1) :
+ démarrage du Rpi

#### Switch rotatif x positions (max 2, x<12): 
+ démarrage (jeux/ordinateur/navette)
- mode de vol (décollage, orbite, attérrissage)

#### Boutons "rocket" (avec LED)
+ phase 1
+ phase 2
+ phase 3

##### Autres :
+ Joystick : commande manuelle
- Hauts-parleurs : son
+ Prises USB :
+ Prises audio Jack 3.5mm : son
- Prise alimentation (sur chassis) : démarrage
+ Raspberry  
  
  
  
  
  
  
  
  
  
# notes diverses  

à mettre à jour

###RPi i/o:
- 6 pour les quatre TM1638 (clk+data, et un Enable par TM)
- 4 pour le joystick
- 6 pour les boutons jeux/commande
- 1 pour le gros bouton
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

#### µC
- i2C (2 I/O) + interrupt (1 output) ?
- APA106 (2 outputs)
- potentiometer (3 Analog inputs)
- 9 push buttons + 4-way joystick (3 outputs, 5 inputs)


