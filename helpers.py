from time import gmtime, strftime


class PrtDecorator:
	last_output = None
def print_decorator(func):
	def wrapped_func(*args, **kwargs):
		prt = args[0]
		if PrtDecorator.last_output and len(prt) < len(PrtDecorator.last_output):
			prt = prt + (' ' * (len(PrtDecorator.last_output) - len(prt)))
			PrtDecorator.last_output = None
		for key, value in kwargs.items():
			if key == "end":
				PrtDecorator.last_output = prt

		return func(prt, '', **kwargs)
	return wrapped_func
	


def prttime():
	return strftime("%d/%m %H:%M", gmtime())