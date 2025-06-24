def impersonation_flag(request):
    return {
        'is_impersonating': 'impersonator_id' in request.session
    }