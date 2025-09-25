def impersonation_flag(request):
    try:
        return {"is_impersonating": "impersonator_id" in request.session}
    except Exception:
        return {"is_impersonating": False}