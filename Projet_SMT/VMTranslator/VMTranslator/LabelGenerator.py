class LabelGenerator:
    """
    Classe responsable de générer des labels uniques avec un compteur interne.
    """
    def __init__(self):
        self.counter = 0

    def generate_label(self, base_name):
        label = f"{base_name}{self.counter}"
        self.counter += 1
        return label
    
class SomeClass:
    def __init__(self):
        self.label_generator = LabelGenerator()

    def some_method(self, command):
        unique_label = self.label_generator.generate_label(command['label'])
        print(f"Generated label: {unique_label}")


