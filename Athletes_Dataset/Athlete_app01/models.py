from django.db import models

# create table app01_SoccerAthlete(id+全部变量) =》SQL
# create tables in MySQL
class Soccer_athlete(models.Model):
    #Athlete_ID = models.IntegerField(unique=True)
    Name = models.CharField(max_length=50, blank=True)
    Nationality = models.CharField(max_length=50, blank=True)
    Continent = models.CharField(max_length=50, blank=True)
    Birthday = models.DateField(blank=True)
    Rating = models.IntegerField(blank=True)
    National_Position = models.CharField(max_length=10, blank=True)
    National_Kit = models.CharField(max_length=10,blank=True)

class Soccer_club(models.Model):
    Club_ID = models.IntegerField(unique=True)
    Club = models.CharField(max_length=50, blank=True)
    Club_alias = models.CharField(max_length=10, blank=True)
class Soccer_contract(models.Model):
    Contract_ID = models.IntegerField(unique=True)
    Club_Joining = models.DateField(blank=True)
    Contract_Expiry = models.IntegerField(blank=True)
class Soccer_affiliation(models.Model):
    # constrains:
    pl = models.ForeignKey(to='Soccer_athlete', to_field='id',on_delete=models.CASCADE)
    cl = models.ForeignKey(to='Soccer_club', to_field='Club_ID',on_delete=models.CASCADE)
    co = models.ForeignKey(to='Soccer_contract', to_field='Contract_ID',on_delete=models.CASCADE)
    # Player_ID = models.IntegerField()
    # Club_ID = models.IntegerField()
    # contract_ID = models.IntegerField()
    Club_Position = models.CharField(max_length=50, blank=True)
    Club_Kit = models.CharField(max_length=10, blank=True)
    # Height = models.IntegerField(blank=True)
    # Weight = models.IntegerField(blank=True)
    Preffered_Foot = models.CharField(max_length=10, blank=True)
    Preffered_Position = models.CharField(max_length=10, blank=True)
    Work_rate = models.CharField(max_length=50, blank=True)
    Weak_foot = models.IntegerField(blank=True)
    Skill_Moves = models.IntegerField(blank=True)
    Ball_Control = models.IntegerField(blank=True)
    Dribbling = models.IntegerField(blank=True)
    Marking = models.IntegerField(blank=True)
    Sliding_Tackle = models.IntegerField(blank=True)
    Standing_Tackle = models.IntegerField(blank=True)
    Aggression = models.IntegerField(blank=True)
    Reactions = models.IntegerField(blank=True)
    Attacking_Position = models.IntegerField(blank=True)
    Interceptions = models.IntegerField(blank=True)
    Vision = models.IntegerField(blank=True)
    Composure = models.IntegerField(blank=True)
    Crossing = models.IntegerField(blank=True)
    Short_Pass = models.IntegerField(blank=True)
    Long_Pass = models.IntegerField(blank=True)
    Acceleration = models.IntegerField(blank=True)
    Speed = models.IntegerField(blank=True)
    Stamina = models.IntegerField(blank=True)
    Strength = models.IntegerField(blank=True)
    Balance = models.IntegerField(blank=True)
    Agility = models.IntegerField(blank=True)
    Jumping = models.IntegerField(blank=True)
    Heading = models.IntegerField(blank=True)
    Shot_Power = models.IntegerField(blank=True)
    Finishing = models.IntegerField(blank=True)
    Long_Shots = models.IntegerField(blank=True)
    Curve = models.IntegerField(blank=True)
    Freekick_Accuracy = models.IntegerField(blank=True)
    Penalties = models.IntegerField(blank=True)
    Volleys = models.IntegerField(blank=True)
    GK_Positioning = models.IntegerField(blank=True)
    GK_Diving = models.IntegerField(blank=True)
    GK_Kicking = models.IntegerField(blank=True)
    GK_Handling = models.IntegerField(blank=True)
    GK_Reflexes = models.IntegerField(blank=True)
class Tennis_athlete(models.Model):
    TennisPlayer_ID = models.IntegerField(unique=True)
    Player = models.CharField(max_length=50, blank=True)
    Age = models.FloatField(blank=True)  # do not need
    Elo = models.FloatField(blank=True)
    Peak_Match = models.CharField(max_length=100, blank=True)
    Peak_Age = models.FloatField(blank=True)
    Peak_Elo = models.FloatField(blank=True)
    Gender = models.CharField(max_length=10, blank=True)
    Tennis_rank = models.IntegerField(blank=True)
class Tennis_hard(models.Model):
    t = models.ForeignKey(to='Tennis_athlete', to_field='TennisPlayer_ID',on_delete=models.CASCADE)
    HardRaw = models.FloatField(blank=True)
    Hard_Court_Elo_Rating = models.FloatField(blank=True)
class Tennis_clay(models.Model):
    t = models.ForeignKey(to='Tennis_athlete', to_field='TennisPlayer_ID',on_delete=models.CASCADE)
    ClayRaw = models.FloatField(blank=True)
    Clay_Court_Elo_Rating = models.FloatField(blank=True)
class Tennis_grass(models.Model):
    t = models.ForeignKey(to='Tennis_athlete', to_field='TennisPlayer_ID',on_delete=models.CASCADE)
    GrassRaw = models.FloatField(blank=True)
    Grass_Court_Elo_Rating = models.FloatField(blank=True)
class userInfo2(models.Model):
    name = models.CharField (max_length=30)
    password = models.CharField(max_length=64)
    age = models.IntegerField()
# python manage.py makemigrations
# python manage.py migrate

# insert data
#userInfo.objects.create(name='Mardy',password='123',age=24)




