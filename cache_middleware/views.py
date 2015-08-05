from util import controller, Response, Router
from random import randint


@controller
def index(request):
    return Response(200, str(randint(0, 100)))


router = Router({
    '/index': index,
})
