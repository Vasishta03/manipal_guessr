from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json
import random

from .models import Location, GameSession, GameRound


def home(request):
    """Landing page with nickname entry."""
    top_scores = GameSession.objects.filter(is_complete=True).order_by('-total_score')[:5]
    total_locations = Location.objects.filter(is_active=True).count()
    total_games = GameSession.objects.filter(is_complete=True).count()
    context = {
        'top_scores': top_scores,
        'total_locations': total_locations,
        'total_games': total_games,
    }
    return render(request, 'game/home.html', context)


def start_game(request):
    """Create a new game session and redirect to first round."""
    if request.method == 'POST':
        nickname = request.POST.get('nickname', '').strip()
        if not nickname:
            return redirect('home')
        nickname = nickname[:30]

        num_rounds = int(request.POST.get('num_rounds', 5))
        num_rounds = max(3, min(10, num_rounds))

        locations = list(Location.objects.filter(is_active=True))
        if len(locations) < num_rounds:
            num_rounds = len(locations)

        if num_rounds == 0:
            return redirect('home')

        selected = random.sample(locations, num_rounds)

        session = GameSession.objects.create(
            nickname=nickname,
            total_rounds=num_rounds
        )

        for i, loc in enumerate(selected, 1):
            GameRound.objects.create(
                session=session,
                location=loc,
                round_number=i
            )

        request.session['game_session_id'] = session.id
        return redirect('game_round', session_id=session.id, round_num=1)

    return redirect('home')


def game_round(request, session_id, round_num):
    """Show the current round with the location image."""
    session = get_object_or_404(GameSession, id=session_id)

    if session.is_complete:
        return redirect('game_result', session_id=session.id)

    round_obj = get_object_or_404(GameRound, session=session, round_number=round_num)

    if round_obj.completed:
        next_round = round_num + 1
        if next_round > session.total_rounds:
            return redirect('game_result', session_id=session.id)
        return redirect('game_round', session_id=session.id, round_num=next_round)

    completed_rounds = session.rounds.filter(completed=True)

    context = {
        'session': session,
        'round': round_obj,
        'round_num': round_num,
        'total_rounds': session.total_rounds,
        'completed_rounds': completed_rounds,
        'progress_pct': round((round_num - 1) / session.total_rounds * 100),
    }
    return render(request, 'game/round.html', context)


@require_POST
def submit_guess(request, session_id, round_num):
    """Handle the map pin drop and calculate score."""
    session = get_object_or_404(GameSession, id=session_id)
    round_obj = get_object_or_404(GameRound, session=session, round_number=round_num)

    if round_obj.completed:
        return JsonResponse({'error': 'Round already completed'}, status=400)

    try:
        data = json.loads(request.body)
        guessed_lat = float(data['lat'])
        guessed_lng = float(data['lng'])
        time_taken = int(data.get('time_taken', 0))
    except (KeyError, ValueError, json.JSONDecodeError):
        return JsonResponse({'error': 'Invalid data'}, status=400)

    actual_lat = round_obj.location.latitude
    actual_lng = round_obj.location.longitude

    distance = GameRound.calculate_distance(guessed_lat, guessed_lng, actual_lat, actual_lng)
    score = GameRound.calculate_score(distance)

    round_obj.guessed_lat = guessed_lat
    round_obj.guessed_lng = guessed_lng
    round_obj.distance_meters = distance
    round_obj.score = score
    round_obj.time_taken = time_taken
    round_obj.completed = True
    round_obj.save()

    session.total_score += score
    session.rounds_played += 1

    if session.rounds_played >= session.total_rounds:
        session.is_complete = True

    session.save()

    is_last = session.is_complete

    return JsonResponse({
        'score': score,
        'distance': round(distance),
        'actual_lat': actual_lat,
        'actual_lng': actual_lng,
        'location_name': round_obj.location.name,
        'location_description': round_obj.location.description,
        'hint': round_obj.location.hint,
        'total_score': session.total_score,
        'is_last': is_last,
        'next_round': round_num + 1 if not is_last else None,
        'session_id': session.id,
    })


def game_result(request, session_id):
    """Show final results after all rounds."""
    session = get_object_or_404(GameSession, id=session_id)

    if not session.is_complete:
        current = session.rounds.filter(completed=False).first()
        if current:
            return redirect('game_round', session_id=session.id, round_num=current.round_number)

    rounds = session.rounds.all().order_by('round_number')

    # Rank on leaderboard
    rank = GameSession.objects.filter(
        is_complete=True,
        total_score__gt=session.total_score
    ).count() + 1

    context = {
        'session': session,
        'rounds': rounds,
        'rank': rank,
        'accuracy': session.get_accuracy(),
    }
    return render(request, 'game/result.html', context)


def leaderboard(request):
    """Global leaderboard of all completed games."""
    scores = GameSession.objects.filter(is_complete=True).order_by('-total_score', 'created_at')[:50]
    context = {'scores': scores}
    return render(request, 'game/leaderboard.html', context)


def how_to_play(request):
    return render(request, 'game/how_to_play.html')
