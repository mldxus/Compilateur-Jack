class LabelGenerator:
    """
    Classe responsable de générer des labels uniques avec un compteur interne.
    Le label généré sera basé sur un nom de base et un compteur qui s'incrémente à chaque appel.
    """
    def __init__(self):
        self.counter = 0  # Initialise le compteur à 0

    def generate_label(self, base_name):
        """
        Génère un label unique en combinant un nom de base et un compteur.

        Args:
            base_name (str): Le nom de base pour le label.

        Returns:
            str: Un label unique basé sur le nom de base et le compteur.
        """
        label = f"{base_name}{self.counter}"  # Construit le label unique
        self.counter += 1  # Incrémente le compteur pour les prochains labels
        return label


    """
    Mettre 'self.label_generator = LabelGenerator()' dans __init__
    Mettre 'unique_label = self.label_generator.generate_label(command['label'])' pour generer un label
    """