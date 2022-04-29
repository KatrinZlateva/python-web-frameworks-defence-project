from news_website_project.web.views import error_404


def handle_exceptions(get_response):
    def middleware(request):
        response = get_response(request)
        if response.status_code == 404:
            return error_404(response)

        return response

    return middleware
