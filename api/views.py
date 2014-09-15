from django.core import serializers
from django.http import HttpResponse

from basketball.models import League, Team, Player


def leagues(request):
    return HttpResponse(serializers.serialize('json', League.objects.all()), content_type="application/json")


def league_info(request, league_id):
    return HttpResponse(serializers.serialize('json', League.objects.filter(pk=league_id)), content_type="application/json")


def teams(request):
    return HttpResponse(serializers.serialize('json', Team.objects.all()), content_type="application/json")


def team_info(request, team_id):
    return HttpResponse(serializers.serialize('json', Team.objects.filter(pk=team_id)), content_type="application/json")


def players(request):
    return HttpResponse(serializers.serialize('json', Player.objects.all()), content_type="application/json")


def player_info(request, player_id):
    return HttpResponse(serializers.serialize('json', Player.objects.filter(pk=player_id)), content_type="application/json")
