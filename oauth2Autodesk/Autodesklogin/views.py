from django.http import response
from django.http.response import JsonResponse
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
import requests
# Create your views here.

redirect_uri = "https://developer.api.autodesk.com/authentication/v1/authorize?response_type=code&client_id=Yt5UEJmKFCSK9BVwUZaxyF00ZmTnNW26&redirect_uri=http%3A%2F%2Flocalhost:8000%2Foauth%2Fcallback%3Ffoo%3Dbar&scope=data:read"

def home(request: HttpRequest) -> HttpResponse:
    return JsonResponse({ "msg": "Hello"})

def autodesk_login(request: HttpRequest):
    return redirect(redirect_uri)

def autodesk_login_redirect(request: HttpRequest):
    code = request.GET.get('code')
    user = exchange_code(code)
    return JsonResponse({ "user": user })

def exchange_code(code: str):
    data = {
        "client_id": "Yt5UEJmKFCSK9BVwUZaxyF00ZmTnNW26",
        "client_secret": "6rrUPjgtq0EcUBdi",
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "http://localhost:8000/oauth/callback?foo=bar"
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.post("https://developer.api.autodesk.com/authentication/v1/gettoken", data=data, headers=headers)
    print(response)
    credentials = response.json()
    print(credentials)
    accesstoken = credentials['access_token']
    response = requests.get('https://developer.api.autodesk.com/project/v1/hubs', headers={
        'Authorization': 'Bearer %s' % accesstoken
    })
    print(response)
    user = response.json()
    print(user)
    return user
