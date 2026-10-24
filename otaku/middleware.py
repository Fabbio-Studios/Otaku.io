from django.conf import settings
from django.http import HttpResponse


class ReadOnlyDeploymentMiddleware:
    legacy_get_mutations = {
        'confirmar_solicitacao',
        'rejeitar_solicitacao',
        'limpar_solicitacoes',
        'excluir_solicitacao',
        'excluir_opiniao',
    }
    safe_methods = {'GET', 'HEAD', 'OPTIONS', 'TRACE'}

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if settings.READ_ONLY_MODE and request.method not in self.safe_methods:
            return self.read_only_response()
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        if (
            settings.READ_ONLY_MODE
            and request.method in self.safe_methods
            and view_func.__name__ in self.legacy_get_mutations
        ):
            return self.read_only_response()
        return None

    @staticmethod
    def read_only_response():
        return HttpResponse(
            'O site esta temporariamente em modo de leitura. '
            'Configure um banco de dados persistente e o armazenamento de arquivos '
            'na Vercel para habilitar esta acao.',
            status=503,
            content_type='text/plain; charset=utf-8',
        )
