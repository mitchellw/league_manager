from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from basketball.models import League, Team, Player, LeagueMembership
from basketball.views import draft_league


class PlayerModelTestCase(TestCase):
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


class DraftTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.superuser = User.objects.create_superuser('testsuperuser', 'super@user.com', 'supersecret')

    def test_full_draft_min_players(self):
        league = League.objects.create(name='Test League 1', max_number_teams=8, min_number_players_per_team=5)
        # Should be 8 teams, each with 5 players
        for i in xrange(0, 40):
            user = User.objects.create_user('testuser%d' % i, email='test%d@test.com' % i, password='testing')
            player = Player.objects.create(name='Test Player League 1 %d' % i, age=22, user=user)
            player.register_for_league(league)

        request = self.factory.post(reverse('basketball:draft-league', args=[league.pk]))
        request.user = self.superuser
        draft_league(request, league.pk)

        self.assertEqual(league.team_set.count(), 8)
        for team in list(league.team_set.all()):
            self.assertEqual(LeagueMembership.objects.filter(team=team).count(), 5)

    def test_full_draft_with_number_of_players_not_divisible_by_number_teams(self):
        league = League.objects.create(name='Test League 1', max_number_teams=8, min_number_players_per_team=5)
        # Should be 5 teams with 7 players and 3 teams with 6 players
        for i in xrange(0, 53):
            user = User.objects.create_user('testuser%d' % i, email='test%d@test.com' % i, password='testing')
            player = Player.objects.create(name='Test Player League 1 %d' % i, age=22, user=user)
            player.register_for_league(league)

        request = self.factory.post(reverse('basketball:draft-league', args=[league.pk]))
        request.user = self.superuser
        draft_league(request, league.pk)

        self.assertEqual(league.team_set.count(), 8)
        seven_player_team_count = 0
        six_player_team_count = 0
        for team in list(league.team_set.all()):
            num_on_team = LeagueMembership.objects.filter(team=team).count()
            if num_on_team == 7:
                seven_player_team_count += 1
            elif num_on_team == 6:
                six_player_team_count += 1

        self.assertEqual(seven_player_team_count, 5)
        self.assertEqual(six_player_team_count, 3)

    def test_draft_with_less_than_max_number_teams(self):
        league = League.objects.create(name='Test League 1', max_number_teams=8, min_number_players_per_team=5)
        # Should be only 7 total teams, 3 with 6 players and 4 with 5 players
        for i in xrange(0, 38):
            user = User.objects.create_user('testuser%d' % i, email='test%d@test.com' % i, password='testing')
            player = Player.objects.create(name='Test Player League 1 %d' % i, age=22, user=user)
            player.register_for_league(league)

        request = self.factory.post(reverse('basketball:draft-league', args=[league.pk]))
        request.user = self.superuser
        draft_league(request, league.pk)

        self.assertEqual(league.team_set.count(), 7)
        six_player_team_count = 0
        five_player_team_count = 0
        for team in list(league.team_set.all()):
            num_on_team = LeagueMembership.objects.filter(team=team).count()
            if num_on_team == 6:
                six_player_team_count += 1
            elif num_on_team == 5:
                five_player_team_count += 1

        self.assertEqual(six_player_team_count, 3)
        self.assertEqual(five_player_team_count, 4)

    def test_draft_with_too_few_players_for_two_teams(self):
        league = League.objects.create(name='Test League 1', max_number_teams=8, min_number_players_per_team=5)
        # Should not create any teams because there are not enough players to even have 2 teams in the league
        for i in xrange(0, 9):
            user = User.objects.create_user('testuser%d' % i, email='test%d@test.com' % i, password='testing')
            player = Player.objects.create(name='Test Player League 1 %d' % i, age=22, user=user)
            player.register_for_league(league)

        request = self.factory.post(reverse('basketball:draft-league', args=[league.pk]))
        request.user = self.superuser
        draft_league(request, league.pk)

        self.assertEqual(league.team_set.count(), 0)
