from django.db import models


class SexType(models.TextChoices):
    MALE = 'Male'
    FEMALE = 'Female'


class Difficulty(models.TextChoices):
    BEGINNER = "Beginner"
    INTERMEDIATE = "Intermediate"
    PRO = "Pro"


class Intensity(models.TextChoices):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "HIGH"


class Rank(models.TextChoices):
    WARRIOR = 1, "Warrior"
    GUARDIAN = 2, "Guardian"
    DEFENDER = 3, "Defender"
    PALADIN = 4, "Paladin"
    MODEL = 5, "MODEL"
    EXEMPLAR = 6, "Exemplar"
    RESCUER = 7, "Rescuer"
    CHAMPION = 8, "Champion"
