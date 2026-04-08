from django.http import JsonResponse


def api_root(request):
    """Root endpoint showing available API routes"""
    return JsonResponse({
        'message': 'CrypToCare API Server',
        'version': '1.0.0',
        'status': 'running',
        'endpoints': {
            'api_base': '/api/',
            'donations': '/api/donations/',
            'stats': '/api/stats/',
            'health': '/api/health/',
            'admin': '/admin/',
        },
        'docs': 'Visit /api/ to explore the API'
    })
