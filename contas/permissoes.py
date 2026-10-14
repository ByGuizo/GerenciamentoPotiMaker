from django.core.exceptions import PermissionDenied


def exigir_coordenador(usuario):
    if not usuario.e_coordenador:
        raise PermissionDenied
