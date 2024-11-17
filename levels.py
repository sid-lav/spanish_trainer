from typing import Dict, List

# Vocabulary organized by CEFR levels
VOCABULARY: Dict[str, List[Dict[str, str]]] = {
    'A1': [
        {'english': 'hello', 'spanish': 'hola'},
        {'english': 'goodbye', 'spanish': 'adiós'},
        {'english': 'yes', 'spanish': 'sí'},
        {'english': 'no', 'spanish': 'no'},
        {'english': 'please', 'spanish': 'por favor'},
        {'english': 'thank you', 'spanish': 'gracias'},
        {'english': 'excuse me', 'spanish': 'disculpe'},
        {'english': 'sorry', 'spanish': 'lo siento'},
        {'english': 'cat', 'spanish': 'gato'},
        {'english': 'dog', 'spanish': 'perro'},
        {'english': 'house', 'spanish': 'casa'},
        {'english': 'car', 'spanish': 'coche'},
        {'english': 'food', 'spanish': 'comida'},
        {'english': 'water', 'spanish': 'agua'},
        {'english': 'coffee', 'spanish': 'café'},
        {'english': 'tea', 'spanish': 'té'},
        {'english': 'milk', 'spanish': 'leche'},
        {'english': 'bread', 'spanish': 'pan'},
        {'english': 'egg', 'spanish': 'huevo'},
        {'english': 'fruit', 'spanish': 'fruta'},
    ],
    'A2': [
        {'english': 'big', 'spanish': 'grande'},
        {'english': 'small', 'spanish': 'pequeño'},
        {'english': 'new', 'spanish': 'nuevo'},
        {'english': 'old', 'spanish': 'viejo'},
        {'english': 'good', 'spanish': 'bueno'},
        {'english': 'bad', 'spanish': 'mal'},
        {'english': 'hot', 'spanish': 'caliente'},
        {'english': 'cold', 'spanish': 'frío'},
        {'english': 'fast', 'spanish': 'rápido'},
        {'english': 'slow', 'spanish': 'lento'},
    ],
    # Add more levels as needed
}

# Common verbs for conjugation practice
VERBS: List[Dict[str, str]] = [
    {'infinitive': 'comer', 'stem': 'com', 'type': 'er'},
    {'infinitive': 'beber', 'stem': 'beb', 'type': 'er'},
    {'infinitive': 'vivir', 'stem': 'viv', 'type': 'ir'},
    {'infinitive': 'hablar', 'stem': 'habl', 'type': 'ar'},
    {'infinitive': 'escribir', 'stem': 'escrib', 'type': 'ir'},
    {'infinitive': 'leer', 'stem': 'le', 'type': 'er'},
    {'infinitive': 'venir', 'stem': 'ven', 'type': 'ir'},
    {'infinitive': 'venir', 'stem': 'ven', 'type': 'ir'},
    {'infinitive': 'ir', 'stem': 'v', 'type': 'ir'},
    {'infinitive': 'ser', 'stem': 's', 'type': 'er'},
    {'infinitive': 'estar', 'stem': 'est', 'type': 'ar'},
    {'infinitive': 'tener', 'stem': 'ten', 'type': 'er'},
    {'infinitive': 'hacer', 'stem': 'hac', 'type': 'er'},
    {'infinitive': 'decir', 'stem': 'dic', 'type': 'ir'},
    {'infinitive': 'dar', 'stem': 'd', 'type': 'ar'},
    {'infinitive': 'ver', 'stem': 'v', 'type': 'er'},
    {'infinitive': 'poder', 'stem': 'pod', 'type': 'er'},
    {'infinitive': 'saber', 'stem': 'sab', 'type': 'er'},
    {'infinitive': 'querer', 'stem': 'quer', 'type': 'er'},
    {'infinitive': 'poner', 'stem': 'pon', 'type': 'er'},
]
