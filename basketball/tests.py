from django.test import TestCase
from django.contrib.auth.models import User
from basketball.models import League, Team, Player, LeagueMembership


class BasketballTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user('testuser', email='test@test.com', password='testing')
        self.test_player = Player.objects.create(name='Test Player', age=22, user=user)

        self.test_league1 = League.objects.create(name='Test League 1')
        self.test_league2 = League.objects.create(name='Test League 2')
        self.test_l1_team1 = Team.objects.create(name='League 1 Team 1', league=self.test_league1)
        self.test_l1_team2 = Team.objects.create(name='League 1 Team 2', league=self.test_league1)
        self.test_l2_team1 = Team.objects.create(name='League 2 Team 1', league=self.test_league2)
        self.test_l2_team2 = Team.objects.create(name='League 2 Team 2', league=self.test_league2)

    def test_register_for_league(self):
        player = self.test_player
        league = self.test_league1

        self.assertEqual(player.leagues.all().count(), 0)

        player.register_for_league(league)

        self.assertEqual(LeagueMembership.objects.filter(player=player).count(), 1)
        self.assertIsNotNone(LeagueMembership.objects.get(player=player, team=None))

    def test_assign_player_to_team(self):
        player = self.test_player
        league = self.test_league1
        team = self.test_l1_team1

        self.assertEqual(player.leagues.all().count(), 0)

        player.assign_to_team_in_league(league, team)

        self.assertEqual(player.leagues.all().count(), 1)
        self.assertIn(league, player.leagues.all())

        self.assertIsNotNone(LeagueMembership.objects.get(player=player, team=team))

    def test_assign_player_to_2_teams_in_same_league(self):
        player = self.test_player
        league = self.test_league1
        team1 = self.test_l1_team1
        team2 = self.test_l1_team2

        self.assertEqual(player.leagues.all().count(), 0)

        player.assign_to_team_in_league(league, team1)
        player.assign_to_team_in_league(league, team2)

        self.assertEqual(player.leagues.all().count(), 1)
        self.assertIn(league, player.leagues.all())

        self.assertEqual(LeagueMembership.objects.filter(player=player).count(), 1)
        self.assertIsNotNone(LeagueMembership.objects.get(player=player, team=team2))

        self.assertEqual(LeagueMembership.objects.filter(player=player, team=team1).count(), 0)

    def test_assign_player_to_2_teams_in_different_leagues(self):
        player = self.test_player
        league1 = self.test_league1
        league2 = self.test_league2
        l1_team = self.test_l1_team1
        l2_team = self.test_l2_team2

        self.assertEqual(player.leagues.all().count(), 0)

        player.assign_to_team_in_league(league1, l1_team)
        player.assign_to_team_in_league(league2, l2_team)

        self.assertEqual(player.leagues.all().count(), 2)
        self.assertIn(league1, player.leagues.all())
        self.assertIn(league2, player.leagues.all())
        self.assertEqual(LeagueMembership.objects.filter(player=player).count(), 2)
