from flask import Flask, request, Response
from logging.config import dictConfig
import traceback
from random import choice
import string
import sys
from utils import logging_func, NotAwaitingError

app = Flask(__name__)


dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] -- %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'file': {
        'class': 'logging.FileHandler',
        'filename': 'log.txt',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['file']
    }
})


logger = app.logger


@logging_func(logger)
def process1(req: request):
    print(req.args.to_dict())


@logging_func(logger)
def process2(req: request):
    if req.args.get('notawaiting') == '1':
        logger.error('%s: %s %s %s %s %s ERROR IN FUNC pocess2: notawaiting=1',
                     request.id,
                     request.remote_addr,
                     request.method,
                     request.scheme,
                     request.full_path,
                     request.form.to_dict())
        raise NotAwaitingError(logger, req)
    print(req.method)


@logging_func(logger)
def process3(req: request):
    print(req.headers)


@app.route('/api')
def query():
    process1(request)
    process2(request)
    process3(request)
    return Response(status=200)


# Берем все все все пасы, и возвращаем пользователю 200 код
@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE']) # У меня тут че то решил дурить flask и не видел запросы, поэтому
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])             # я насильно в него засунул основные методы, но возможно я что то
def catch_all(path):                                                             # не увидел или забыл
    method = request.method
    # Если нам отправили не GET запрос логируем это и кидаем пользователю 200 код
    if method != 'GET':
        logger.error('%s: %s %s %s %s %s METHOD NOT ALLOWED',
                     request.id,
                     request.remote_addr,
                     request.method,
                     request.scheme,
                     request.full_path,
                     request.form.to_dict())
    # Если же пользователь скинул нам GET с параметром invalid=1, то говорим ему что он нехороший человек,
    # снова логируем это и кидаем тот же двухсотый
    elif method == 'GET' and request.args.get('invalid') == '1':
        logger.error('%s: %s %s %s %s %s PARAM INVALID=1',
                     request.id,
                     request.remote_addr,
                     request.method,
                     request.scheme,
                     request.full_path,
                     request.form.to_dict())
    # Ну и если GET пришел без инвалидов, то логируем как неизвестный пас и опять по схеме - двухсотый)
    else:
        logger.error('%s: %s %s %s %s %s UNKNOWN URL PATH - 404',
                     request.id,
                     request.remote_addr,
                     request.method,
                     request.scheme,
                     request.full_path,
                     request.form.to_dict())
    return Response(status=200)


# Даем запросу id, чтобы знал кто он есть (по жизни)
# чтобы потом легко отслеживать жизнь запроса и где она оборвалась
@app.before_request
def before_request():
    chars = string.ascii_letters + string.digits
    request.id = ''.join([choice(chars) for i in range(10)])
    logger.info('%s: %s %s %s %s %s',
                 request.id,
                 request.remote_addr,
                 request.method,
                 request.scheme,
                 request.full_path,
                 request.form.to_dict())


# Отлавливаем всякие ошибки (как говорится НА ВСЯКИЙ СЛУЧАЙ)
@app.errorhandler(Exception)
def exceptions(e):
    tb = traceback.format_exc()
    logger.error('%s: %s %s %s %s %s 5xx INTERNAL SERVER ERROR\n%s',
                 request.id,
                 request.remote_addr,
                 request.method,
                 request.scheme,
                 request.full_path,
                 request.form.to_dict(),
                 tb)
    return Response(status=200)


# В ТЗ вы написали, чтобы файл мог запускаться PORT=**** kek.py
# если честно, я в душе не знаю как так сделать, потому что обычно же
# в консоли пишут python <имя запускаемого файла>.py, а потом уже параметры,
# ну собственно я так и сделал, файл запускается python app.py PORT=5000
# (ну я не валидировал имя PORT, как видно ниже, просто не стал усложнять, но я это могу
# сделать, просто добавить name, port после сплита убрать срез и проверить name,
# но зачем оно нам сейчас нужно, правильно? :)
if __name__ == '__main__':
    port = sys.argv[-1].split('=')[-1]
    app.run(port=port)
