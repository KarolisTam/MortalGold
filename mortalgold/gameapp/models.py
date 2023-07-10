from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()

class Match(models.Model):
    player1 = models.ForeignKey(
        User, 
        verbose_name=_("Player 1"),
        related_name="matches_created",
        on_delete=models.CASCADE)
    player2 = models.ForeignKey(
        User, 
        verbose_name=_("Player 2"),
        related_name="matches_joined",
        on_delete=models.CASCADE, 
        null=True,
        blank=True)
    created_at = models.DateTimeField(_("Created_at"), auto_now_add=True)
    winner = models.ForeignKey(
        User,
        verbose_name=_("winner"),
        related_name='matches_won',
        on_delete=models.CASCADE,
        null=True, blank=True)
    loser = models.ForeignKey(
        User,
        verbose_name=_("loser"),
        related_name='matches_lost',
        on_delete=models.CASCADE,
        null=True, blank=True)
    CHARACTERS = (
        (0, "Putin"),
        (1, "Musk"),
    )
    player1_character = models.PositiveSmallIntegerField(_("Player 1 Character"), null=True, blank=True, choices=CHARACTERS)
    player2_character = models.PositiveSmallIntegerField(_("Player 2 Character"), null=True, blank=True, choices=CHARACTERS)
    
    class Meta:
        verbose_name = _("match")
        verbose_name_plural = _("matches")

    def __str__(self):
        return f"{self.id}: {self.player1.username} vs {self.player2.username}"

    def get_absolute_url(self):
        return reverse("match_detail", kwargs={"pk": self.pk})


class GameAction(models.Model):
    match = models.ForeignKey(
        Match,
        verbose_name=_("match"),
        related_name='game_actions',
        on_delete=models.CASCADE)
    created_at = models.DateTimeField(_("created"), auto_now_add=True)
    player = models.ForeignKey(
        User,
        verbose_name=_("player"),
        related_name='game_actions',
        on_delete=models.CASCADE)
    ACTION_CHOICES = (
        (0, "idle"),
        (1, "run"),
        (2, "jump"),
        (3, "punch"),
        (4, "kick"),
        (5, "gethit"),
        (6, "death"),
        (7, "block"),
    )
    action = models.PositiveIntegerField(_("Action"), default=0, choices=ACTION_CHOICES) #choice
    player_hp_change = models.IntegerField(_("Player HP Change"), default=0)
    opponent_hp_change = models.IntegerField(_("Opponent HP Change"), default=0)
    player_position_x = models.IntegerField(_("Player position x"), null=True, blank=True)
    player_position_y = models.IntegerField(_("Player position y"), null=True, blank=True)
    opponent_position_x = models.IntegerField(_("Opponent position x"), null=True, blank=True)
    opponent_position_y = models.IntegerField(_("Opponent position y"), null=True, blank=True)

    class Meta:
        verbose_name = _("game")
        verbose_name_plural = _("games")

    def __str__(self):
        return f'{self.match.id}: {self.player.username}'

    def get_absolute_url(self):
        return reverse("game_detail", kwargs={"pk": self.pk})
