def get_tracer_info(env):
    return env.get('HTTP_X_APM_TRACER', "null:null")
