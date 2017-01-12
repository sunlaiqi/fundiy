from django.views import generic


class HomePage(generic.TemplateView):

    template_name = "shop/product_list.html"


class AboutPage(generic.TemplateView):
    template_name = "about.html"
