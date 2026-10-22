from django.conf import settings
from django.core.cache import cache


def ip_do_cliente(request):
    if settings.CONFIAR_X_REAL_IP:
        return request.META.get('HTTP_X_REAL_IP') or request.META.get('REMOTE_ADDR')
    return request.META.get('REMOTE_ADDR')


def limite_atingido(chave, limite):
    return cache.get(chave, 0) >= limite


def registrar_tentativa(chave, segundos):
    if cache.add(chave, 1, segundos):
        return
    try:
        cache.incr(chave)
    except ValueError:
        cache.add(chave, 1, segundos)


def zerar_tentativas(chave):
    cache.delete(chave)
