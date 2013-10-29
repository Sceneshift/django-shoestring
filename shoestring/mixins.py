from django.views.decorators.cache import cache_page
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django.conf import settings

## Django 1.5+ compat
try:
	import json
except ImportError:  # pragma: no cover
	from django.utils import simplejson as json

class CacheMixin(object):
	cache_timeout = 60

	def get_cache_timeout(self):
		return self.cache_timeout
 
	def dispatch(self, *args, **kwargs):
		return cache_page(self.get_cache_timeout())(super(CacheMixin, self).dispatch)(*args, **kwargs)

class CsrfExemptMixin(object):
	"""
	Exempts the view from CSRF requirements.

	NOTE:
	    This should be the left-most mixin of a view.
	"""
	@method_decorator(csrf_exempt)
	def dispatch(self, *args, **kwargs):
		return super(CsrfExemptMixin, self).dispatch(*args, **kwargs)

class AccessMixin(object):
	"""
	'Abstract' mixin that gives access mixins the same customizable
	functionality.
	"""
	login_url = settings.LOGIN_URL  # LOGIN_URL from project settings
	raise_exception = False  # Default whether to raise an exception to none
	redirect_field_name = REDIRECT_FIELD_NAME  # Set by django.contrib.auth

	def get_login_url(self):
		"""
		Override this method to customize the login_url.
		"""
		if self.login_url is None:
			raise ImproperlyConfigured("%(cls)s is missing the login_url. "
				"Define %(cls)s.login_url or override "
				"%(cls)s.get_login_url()." % {"cls": self.__class__.__name__})

		return self.login_url

	def get_redirect_field_name(self):
		"""
		Override this method to customize the redirect_field_name.
		"""
		if self.redirect_field_name is None:
			raise ImproperlyConfigured("%(cls)s is missing the "
				"redirect_field_name. Define %(cls)s.redirect_field_name or "
				"override %(cls)s.get_redirect_field_name()." % {
				"cls": self.__class__.__name__})

		return self.redirect_field_name


class LoginRequiredMixin(AccessMixin):
    """
    View mixin which verifies that the user is authenticated.

    NOTE:
        This should be the left-most mixin of a view.
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            if self.raise_exception:
                raise PermissionDenied  # return a forbidden response
            else:
                return redirect_to_login(request.get_full_path(),
                    self.get_login_url(), self.get_redirect_field_name())

        return super(LoginRequiredMixin, self).dispatch(request, *args,
            **kwargs)

class JSONResponseMixin(object):
	"""
	A mixin that allows you to easily serialize simple data such as a dict or
	Django models.
	"""
	content_type = "application/json"
	json_dumps_kwargs = None

	def get_content_type(self):
		if self.content_type is None:
			raise ImproperlyConfigured("%(cls)s is missing a content type. "
				"Define %(cls)s.content_type, or override "
				"%(cls)s.get_content_type()." % {
				"cls": self.__class__.__name__
			})
		return self.content_type

	def get_json_dumps_kwargs(self):
		if self.json_dumps_kwargs is None:
			self.json_dumps_kwargs = {}
			self.json_dumps_kwargs.setdefault('ensure_ascii', False)
		return self.json_dumps_kwargs

	def render_json_response(self, context_dict):
		"""
		Limited serialization for shipping plain data. Do not use for models
		or other complex or custom objects.
		"""
		json_context = json.dumps(context_dict, cls=DjangoJSONEncoder, **self.get_json_dumps_kwargs())
		return HttpResponse(json_context, content_type=self.get_content_type())