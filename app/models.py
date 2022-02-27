from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
import pytz
import datetime

# Create your models here.
class Record(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    score = models.IntegerField()
    score_addition = models.IntegerField()
    score_substraction = models.IntegerField()
    score_multiplication = models.IntegerField()
    score_division = models.IntegerField()
    date = models.DateTimeField(default=now, blank=True, null=True)

    def __str__(self):
        if self.user != None:
            return self.user.username
        else:
            return 'Anonymous'

class DailyQuest(models.Model):
    QUEST_TYPE = (
        ("A", "Akumulatif"),
        ("B", "")
    )
    QUEST_TARGET_TYPE = (
        ("S", "Score"),
        ("+", "Addition"),
        ("-", "Substraction"),
        ("*", "Multiplication"),
        ("/", "Division")
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quest_name = models.CharField(max_length=50)
    quest_target = models.IntegerField()
    quest_target_type = models.CharField(max_length=1, choices=QUEST_TARGET_TYPE)
    quest_type = models.CharField(max_length=1, choices=QUEST_TYPE)
    reward = models.IntegerField(default=0)
    date = models.DateField(default=datetime.datetime.now)
    current_progress = models.IntegerField(default=0)
    complete = models.BooleanField(default=False)

    def get_current_percentage(self):
        percent = (self.current_progress/self.quest_target)*100
        if percent > 100:
            percent = 100
        return "{:.2f}%".format(percent)

    def __str__(self):
        return self.quest_name

class Feedback(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=128, null=True, blank=True)
    feed_value = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User,related_name="profile", on_delete=models.CASCADE)
    level = models.IntegerField(default=0)
    exp = models.IntegerField(default=0)
    exp_needed = models.IntegerField(default=100)
    daily_quest = models.BooleanField(default=False)
    def __str__(self):
        return self.user.username

    def calculate_level(self):
        self.level = self.exp // 100
        self.exp_needed = ((self.level // 10) * 10) + 100

    def exp_to_next_level(self):
        return self.exp_needed - (self.exp % 100)

    def get_exp_percentage(self):
        exp = self.exp % self.exp_needed
        return "{}%".format(exp)

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
