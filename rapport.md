% IFT3335 --- Jeu de Sudoku

# État

L'état est représenté par une grille carrée de 81 cases pouvant contenir un
chiffre entre 1 et 9 ou une valeur nulle sujette aux contraintes suivantes:

 - une ligne ne peut contenir deux fois le même nombre
 - une colonne ne peut contenir deux fois le même nombre
 - une sous-grille 3 par 3 aux positions 0, 4 et 7 ne peut contenir deux fois
   le même nombre

L'état initial est une grille initialisée avec certaines valeurs.

L'état final est une grille contenant aucune valeur nulle.

Un successeur constitue une grille dont l'une des cases nulle prend une valeur
entre 1 et 9. Le coût d'étape est le même pour toute les cases.

Il y a donc $9 * n$ successeurs possible pour une grille de $n$ cases nulles.

