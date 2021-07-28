from django.db import models
from django.views import View
from django.utils.text import slugify

DAY_NAMES = (
    ('Poniedziałek', 'PONIEDZIAŁEK'),
    ('Wtorek', 'WTOREK'),
    ('Środa', 'ŚRODA'),
    ('Czwartek', 'CZWARTEK'),
    ('Piątek', 'PIĄTEK'),
    ('Sobota', 'SOBOTA'),
    ('Niedziela', 'NIEDZIELA')
)


class Recipe(models.Model):
    name = models.CharField(max_length=100)
    ingredients = models.TextField()
    description = models.TextField()
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    preparation_time = models.IntegerField(null=False)
    votes = models.IntegerField(default=0)
    dish_description = models.TextField(max_length=500, null=True)


class DayName(models.Model):
    name = models.TextField(max_length=16, choices=DAY_NAMES)
    order = models.IntegerField(null=False, unique=True)


class Plan(models.Model):
    name = models.TextField(max_length=255)
    description = models.TextField(max_length=2000)
    created = models.DateField(auto_now_add=True)
    recipe = models.ManyToManyField(Recipe, through='RecipePlan')


class RecipePlan(models.Model):
    meal_name = models.TextField(max_length=255)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    order = models.IntegerField(null=False)
    day_name = models.ForeignKey(DayName, on_delete=models.CASCADE)


class Page(models.Model):
    title = models.TextField(max_length=255)
    description = models.TextField(max_length=2000)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Page, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
