from django.shortcuts import render
import json
from django.http import HttpResponse

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .supabase_client import SupabaseClient
from django.http import HttpResponse

def login_view(request):
    return HttpResponse("Login page")
@csrf_exempt
def supabase_login(request):
    if request.method == 'POST':
        try:
            supabase = SupabaseClient.get_client()
            data = json.loads(request.body)
            
            # Authenticate with Supabase
            response = supabase.auth.sign_in_with_password({
                'email': data['email'],
                'password': data['password']
            })
            
            return JsonResponse({
                'status': 'success',
                'user': response.user.model_dump()
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)