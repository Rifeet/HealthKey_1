from django.shortcuts import render
import json
from django.http import HttpResponse

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .supabase_client import SupabaseClient
from django.http import HttpResponse
import random, string
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import OTPCode


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
        # authentication/views.py

def _generate_code(n=6):
    return ''.join(random.choices(string.digits, k=n))

@api_view(['POST'])
def request_otp(request):
    national_id = (request.data.get('national_id') or '').strip()
    if not national_id:
        return Response({'error': 'national_id required'}, status=status.HTTP_400_BAD_REQUEST)

    # امسح الأكواد السابقة لنفس الرقم (اختياري)
    OTPCode.objects.filter(national_id=national_id).delete()

    code = _generate_code()
    otp = OTPCode.objects.create(national_id=national_id, code=code)

    # لاحقاً اربط SMS؛ حالياً نطبع بالكوماند
    print(f"[OTP] national_id={national_id} code={code} (expires in ~5 minutes)")

    return Response({'ok': True, 'message': 'OTP sent (console for now).'}, status=200)

@api_view(['POST'])
def verify_otp(request):
    national_id = (request.data.get('national_id') or '').strip()
    code = (request.data.get('code') or '').strip()

    if not national_id or not code:
        return Response({'error': 'national_id and code required'}, status=400)

    try:
        otp = OTPCode.objects.filter(national_id=national_id, code=code).latest('created_at')
    except OTPCode.DoesNotExist:
        return Response({'ok': False, 'error': 'Invalid code'}, status=400)

    # التحقق من الصلاحية (لو فعلته في model)
    if hasattr(otp, 'is_expired') and otp.is_expired:
        return Response({'ok': False, 'error': 'Code expired'}, status=400)

    # نجاح — احذف السجل (اختياري)
    otp.delete()

    return Response({'ok': True}, status=200)
