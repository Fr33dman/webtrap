from flask import request, Flask


# Декоратор, который будет нам помогать понимать, закрашилась какая-то функция
# или нет, логирует начало функции и конец, и ошибку если такая произошла
def logging_func(logger: Flask.logger):
    def wrapper(func):
        def wrapped_func(request: request):
            logger.info('%s: %s %s %s %s %s FUNC %s START WORKING',
                        request.id,
                        request.remote_addr,
                        request.method,
                        request.scheme,
                        request.full_path,
                        request.form.to_dict(),
                        func.__name__)
            try:
                func(request)
                logger.info('%s: %s %s %s %s %s FUNC %s END WORKING',
                            request.id,
                            request.remote_addr,
                            request.method,
                            request.scheme,
                            request.full_path,
                            request.form.to_dict(),
                            func.__name__)
            except Exception as error:
                logger.error('%s: %s %s %s %s %s FUNC %s CATCHES ERROR\n%s',
                             request.id,
                             request.remote_addr,
                             request.method,
                             request.scheme,
                             request.full_path,
                             request.form.to_dict(),
                             func.__name__,
                             error)
        return wrapped_func
    return wrapper


# Ошибка специально для функции process2, которая вызывается если notawaiting=1
class NotAwaitingError(Exception):

    def __init__(self, logger: Flask.logger, req: request):
        self.message = 'notawaiting param can`t be set 1'
        logger.error('%s: %s %s %s %s %s NowAwaitingError: param \'notawaiting\' can`t be set 1',
                     req.id,
                     req.remote_addr,
                     req.method,
                     req.scheme,
                     req.full_path,
                     req.form.to_dict())
        super().__init__(self.message)
