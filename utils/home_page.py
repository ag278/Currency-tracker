from sanic_ext import render


class HomePage:
    class_variable = ''

    @classmethod
    def home_page_handler(cls):
        return render('home.html')
