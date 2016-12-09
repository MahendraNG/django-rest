from oauth2_provider.views.generic import ProtectedResourceView

class ApiEndpoint(ProtectedResourceView):
	def get(self, request, *args, **kwargs):
		return HttpResponse('Protected with Oauth2')