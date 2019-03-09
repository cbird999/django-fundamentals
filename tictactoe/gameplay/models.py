# for python2 unicode strings -- not needed in python3.x
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
# import model libraries
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User


GAME_STATUS_CHOICES = (
    ('F', 'First Player To Move'),
    ('S', 'Second Player to Move'),
    ('W', 'First Player Wins'),
    ('L', 'Second Player Wins'),
    ('D', 'Draw')
)

# custom QuerySet class
class GamesQuerySet(models.QuerySet):
    def games_for_user(self, user):

        return self.filter(
            Q(first_player=user) | Q(second_player=user)
        )

    def active(self):
        return self.filter(
            Q(status='F') | Q(status='S')
        )

@python_2_unicode_compatible    # add unicode capability to python2 code -- no effect on python3
class Game(models.Model):
    # foreign key relationships to User -- must be imported from auth.models
    first_player = models.ForeignKey(User, related_name='games_first_player')
    second_player = models.ForeignKey(User, related_name='games_second_player')

    start_time = models.DateTimeField(auto_now_add=True)
    last_active = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1, default='F', choices=GAME_STATUS_CHOICES)

    objects = GamesQuerySet.as_manager()

    # implement __str__ function for nice printing
    def __str__(self):
        return '{0} vs {1}'.format(self.first_player, self.second_player)

class Move(models.Model):
    x = models.IntegerField()
    y = models.IntegerField()
    comment = models.CharField(max_length=300, blank=True)
    by_first_player = models.BooleanField()

    # foreign key relationship to Game
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    # implement __str__ function for nice printing
    def __str__(self):
        return 'Move to x={0}, y={1}'.format(self.x, self.y)