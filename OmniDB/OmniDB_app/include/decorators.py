from functools import wraps
from django.shortcuts import redirect
from django.http import JsonResponse


def omnidb_session_required_in_get(p_view=None):
    """Decorator requiring OmniDB session to exist in django get request. Will redirect to login page with an alert message if does not exist.

        Args:
            p_view (function): some view to be decorated. Defaults to None.

        Returns:
            function: final function decorator code.
    """

    @wraps(p_view)
    def wrapper(*args, **kwargs):
        """Decorator wrapper code.

            Args:
                args (tuple): position arguments of p_view.
                    Notes:
                        Must have the following structure:
                            (
                                django.core.handlers.wsgi.WSGIRequest: the user django request in a browser.
                            )
                kwargs (dict): keyworded arguments of p_view.
        """

        v_request = args[0]

        #Invalid session
        if not v_request.session.get('omnidb_session'):
            v_request.session['omnidb_alert_message'] = 'Session object was destroyed, please sign in again.'
            return redirect('login')

        return p_view(*args, **kwargs)

    return wrapper


def omnidb_session_required_in_ajax(p_view=None):
    """Decorator requiring OmniDB session to exist in django ajax request. Will return a json response with error code if does not exist.

        Args:
            p_view (function): some view to be decorated. Defaults to None.

        Returns:
            function: final function decorator code.
    """

    @wraps(p_view)
    def wrapper(*args, **kwargs):
        """Decorator wrapper code.

            Args:
                args (tuple): position arguments of p_view.
                    Notes:
                        Must have the following structure:
                            (
                                django.core.handlers.wsgi.WSGIRequest: the user django request in a browser.
                            )
                kwargs (dict): keyworded arguments of p_view.
        """

        v_request = args[0]

        #Invalid session
        if not v_request.session.get('omnidb_session'):
            v_return = {
                'v_data': '',
                'v_error': True,
                'v_error_id': 1
            }

            return JsonResponse(v_return)

        return p_view(*args, **kwargs)

    return wrapper
