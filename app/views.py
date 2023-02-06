from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from django.core.cache import cache

def getClientIp(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def rateLimiting(request):
    ip = getClientIp(request)
    if cache.get(ip):
        if cache.get(ip)>=5:
            return JsonResponse({'Status':501,'message':f'Too many tries, try after {cache.ttl(ip)} seconds'})
        else:
            cache.set(ip, cache.get(ip)+1,timeout=10)
            return JsonResponse({'Status':200,'ip':ip,'tries left':5-cache.get(ip)})
    cache.set(ip,1,timeout=10)
    return JsonResponse({'Status':200,'ip':ip,'tries left':5-cache.get(ip)})