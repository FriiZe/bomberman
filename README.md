# Bomber Man #

Vérifiez s'il vous plaît que vous avez bien installé Python3 (https://www.python.org/downloads/) et la bibliothèque PyGame (https://www.pygame.org/download.shtml)

## Créer un serveur ##

- Ouvrez un terminal
- Placez-vous dans le répertoire du jeu (là où se trouvent les fichiers bomber_server.py, bomber_client.py et bomber.py)
- Tapez la commande suivante : ./bomber_server.py <PORT> [maps/<MAP_NAME>]
  Cette commande crée un serveur auquel les joueurs peuvent se connecter grâce à votre adresse IP et votre port numéro <PORT>. Vous pouvez spécifier une map particulière grâce à l'option maps/<MAP_NAME>, ce qui chargera la map au nom <MAP_NAME> contenue dans le dossier "maps" de votre répertoire principal.

Vous avez créé un serveur !

## Se connecter au serveur ##

- Ouvrez un terminal
- Placez-vous dans le répertoire du jeu (là où se trouvent les fichiers bomber_server.py, bomber_client.py et bomber.py)
- Tapez la commande suivante : ./bomber_client.py <IP_ADDRESS> <PORT> <NICKNAME>
  Cette commande lance une fenêtre de jeu, charge la map du serveur (pas besoin d'avoir la map dans vos fichiers), en vous connectant au serveur situé sur l'ip <IP_ADDRESS> au port <PORT>, sous le pseudonyme <NICKNAME>. ATTENTION : si quelqu'un joue déjà avec le même pseudo que vous, vous ne pourrez pas vous connecter !

Vous êtes maintenant prêt à jouer !

## JOUER ##

- Déplacements : flèches directionnelles
- Lâcher une bombe : touche "espace"
- Quitter le jeu : touche "échap"

Toutes les X secondes, une flopée de bombes est lâchée aléatoirement sur la map. Le nombre de bombes augmente au fur et à mesure de la partie, puis revient à UNE bombe lâchée pour recommencer un cycle.
Toutes les X secondes, une flopée de fruits est lâchée si le nombre de fruits présents sur la map ne dépasse pas un certain seuil. L'apparition des fruits se fait à des positions aléatoires, et leur nombre est aussi aléatoire, variant entre 0 fruits et X fruits.

(L'imprécision à l'aide des "X" est volontaire, afin de vous laisser découvrir par vous-même...)

Vous vous connectez avec 50 points de vie.
Si vous êtes touché par une ou plusieurs bombes, vous perdez 10 points de vie.
Si vous ramassez un fruit, vous gagnez 10 points de vie.

Si vous quittez la partie, que ce soit par une mort violente (coupure de réseau, d'électricité...) ou une déconnexion de votre part, et que vous vous reconnectez avec la même adresse IP et le même nickname, vous serez automatiquement remis au même endroit, avec la même apparence et le même nom de points de vie.

Si vous mourrez, vous devrez vous reconnecter pour rejoueren revenant au point de départ (50 points de vie, placement et apaprence aléatoires).