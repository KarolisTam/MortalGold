# Generated by Django 4.2.2 on 2023-07-03 15:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created_at')),
                ('loser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matches_lost', to=settings.AUTH_USER_MODEL, verbose_name='loser')),
                ('player1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matches_created', to=settings.AUTH_USER_MODEL, verbose_name='Player 1')),
                ('player2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='matches_joined', to=settings.AUTH_USER_MODEL, verbose_name='Player 2')),
                ('winner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matches_won', to=settings.AUTH_USER_MODEL, verbose_name='winner')),
            ],
            options={
                'verbose_name': 'match',
                'verbose_name_plural': 'matches',
            },
        ),
        migrations.CreateModel(
            name='GameAction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('action', models.PositiveIntegerField(choices=[(0, 'idle'), (1, 'run'), (2, 'jump'), (3, 'punch'), (4, 'kick'), (5, 'gethit'), (6, 'death'), (7, 'block')], default=0, verbose_name='Action')),
                ('player_hp_change', models.IntegerField(default=0, verbose_name='Player HP Change')),
                ('opponent_hp_change', models.IntegerField(default=0, verbose_name='Opponent HP Change')),
                ('player_position_x', models.IntegerField(blank=True, null=True, verbose_name='Player position x')),
                ('player_position_y', models.IntegerField(blank=True, null=True, verbose_name='Player position y')),
                ('opponent_position_x', models.IntegerField(blank=True, null=True, verbose_name='Opponent position x')),
                ('opponent_position_y', models.IntegerField(blank=True, null=True, verbose_name='Opponent position y')),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='game_actions', to='gameapp.match', verbose_name='match')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='game_actions', to=settings.AUTH_USER_MODEL, verbose_name='player')),
            ],
            options={
                'verbose_name': 'game',
                'verbose_name_plural': 'games',
            },
        ),
    ]
