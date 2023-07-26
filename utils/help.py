from sanic_ext import render


class Help:

    def __init__(self):
        pass

    @classmethod
    def help_handler(cls):
        return render("help.html", context={}, status=200)
