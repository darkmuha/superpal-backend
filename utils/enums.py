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
    HIGH = "High"


class Rank(models.IntegerChoices):
    WARRIOR = 1
    GUARDIAN = 2
    DEFENDER = 3
    PALADIN = 4
    MODEL = 5
    EXEMPLAR = 6
    RESCUER = 7
    CHAMPION = 8


class SuperPalWorkoutRequestStatus(models.TextChoices):
    PENDING = 'Pending'
    ACCEPTED = 'Accepted'
    COMPLETED = 'Completed'
    CANCELED = 'Canceled'
    DECLINED = 'Declined'
