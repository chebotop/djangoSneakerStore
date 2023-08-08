from django.shortcuts import render


def index(request):
    return render(request, 'main/index.html')


def sheets_bot(request):
    return render(request, 'main/sheets_bot.html')