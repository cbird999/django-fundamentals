from django.shortcuts import render, redirect

def welcome(request):
    if request.user.is_authenticated:
        return redirect('player_home') # redirect by name, otherwise URL redirect('/player/home') -- but hard coding the URL can be problematic
    else:
        return render(request, 'tictactoe/welcome.html')