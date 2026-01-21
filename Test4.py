import matplotlib.pyplot as plt
import numpy as np

# --- Paramètres Simplifiés ---
R_CAPT = 1.2  # Suffisant pour couvrir les diagonales proches
R_COM = 2.0   # Rayon de communication strict

def plot_simple_scenario(ax, sensors, title, step):
    """
    sensors: dictionnaire {Nom: (x, y)}
    step: 1 (Init), 2 (Move), 3 (Drop)
    """
    # 1. Configuration de la grille et du Puits
    # Les cibles potentielles (Grid)
    targets = [(1,0), (1,1), (2,0), (3,0)]
    for tx, ty in targets:
        ax.plot(tx, ty, 'k+', markersize=8, zorder=1) # Cibles en croix noires
    
    # Le Puits P(0,0)
    ax.plot(0, 0, 'rs', markersize=12, label='Puits (0,0)', zorder=10)
    
    # Configuration Axes
    ax.set_title(title, fontsize=10, fontweight='bold')
    ax.set_xlim(-0.5, 4.0)
    ax.set_ylim(-0.5, 2.0)
    ax.set_aspect('equal')
    ax.grid(True, linestyle=':', alpha=0.6)
    
    # 2. Dessin des Capteurs et Rayons
    for name, (x, y) in sensors.items():
        color = 'blue'
        
        # Rayon de Captation (Vert rempli léger)
        # On ne le dessine que pour les capteurs actifs
        capt = plt.Circle((x, y), R_CAPT, color='green', alpha=0.1)
        ax.add_artist(capt)
        
        # Le point du capteur
        ax.plot(x, y, 'o', color=color, markersize=10, zorder=5)
        ax.text(x, y+0.2, name, ha='center', fontsize=9, fontweight='bold', color=color)

    # 3. Logique Spécifique par étape
    
    # ETAPE 1 : Initiale (Besoin de S2)
    if step == 1:
        # P(0,0) -> S1(1,1) -> S2(2,0) -> S3(3,0)
        ax.plot([0, 1], [0, 1], 'k-', lw=1)
        ax.plot([1, 2], [1, 0], 'k-', lw=1)
        ax.plot([2, 3], [0, 0], 'k-', lw=1)
        
        # Pourquoi pas direct S1->S3 ?
        dist = np.sqrt((3-1)**2 + (0-1)**2) # sqrt(5) approx 2.23
        ax.plot([1, 3], [1, 0], 'r:', alpha=0.5)
        ax.text(2, 0.8, f"Dist={dist:.2f} > 2\n(S2 indispensable)", color='red', fontsize=8, ha='center')

    # ETAPE 2 : Déplacement (S1 descend)
    elif step == 2:
        # S1 bouge de (1,1) vers (1,0)
        ax.plot(1, 1, 'bo', alpha=0.2) # Fantome
        ax.annotate("", xy=(1, 0.1), xytext=(1, 1), arrowprops=dict(arrowstyle="->", color='orange', lw=2))
        ax.text(0.5, 0.5, "Move", color='orange', fontweight='bold')
        
        # On garde les connexions temporaires pour visualiser
        ax.plot([0, 1], [0, 0], 'k-', lw=1)
        ax.plot([1, 2], [0, 0], 'k-', lw=1)
        ax.plot([2, 3], [0, 0], 'k-', lw=1)

    # ETAPE 3 : Drop (S2 supprimé)
    elif step == 3:
        # S1(1,0) couvre maintenant S3(3,0) car distance = 2
        ax.plot([0, 1], [0, 0], 'k-', lw=1)
        ax.plot([1, 3], [0, 0], 'g-', lw=2, label="Connexion Directe")
        
        # S2 supprimé
        ax.plot(2, 0, 'rx', markersize=12)
        ax.text(2, -0.3, "S2 Inutile", color='red', ha='center')
        
        # Preuve de couverture
        # Cercle vert autour de S1 montre qu'il touche (1,1) et (2,0)
        ax.text(1, 1.3, "S1 couvre (1,1)!", color='green', fontsize=8, ha='center')
        ax.text(2, 0.3, "S1 couvre (2,0)!", color='green', fontsize=8, ha='center')

# --- Données ---
# Puits fixe à (0,0)

# 1. Situation Initiale
sensors_1 = {'S1': (1,1), 'S2': (2,0), 'S3': (3,0)}

# 2. Situation après Move (S1 descend en 1,0)
sensors_2 = {'S1': (1,0), 'S2': (2,0), 'S3': (3,0)}

# 3. Situation après Drop (S2 part)
sensors_3 = {'S1': (1,0), 'S3': (3,0)}

# --- Affichage ---
fig, axes = plt.subplots(3, 1, figsize=(6, 10))
plt.subplots_adjust(hspace=0.4)

plot_simple_scenario(axes[0], sensors_1, "1. Init : S1(1,1) est trop loin de S3", 1)
plot_simple_scenario(axes[1], sensors_2, "2. Move : S1 descend en (1,0)", 2)
plot_simple_scenario(axes[2], sensors_3, "3. Drop : S1(1,0) connecte S3 et couvre tout", 3)

plt.show()