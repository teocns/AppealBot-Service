class Constants:

	FORM_SUBMITS_DELAY = 84600  # How much to wait minimum between one appeal and another

	APPEAL_STATUS_PENDING = 'PENDING'
	APPEAL_STATUS_FORM_SUBMITTED = 'FORM_SUBMITTED'
	APPEAL_STATUS_VERIFICATION_CODE_RECEIVED = 'CODE_RECEIVED'
	APPEAL_STATUS_EMAIL_SENT = 'EMAIL_SENT'
	APPEAL_STATUS_REJECTED = 'APPEAL_REJECTED'
	APPEAL_STATUS_REACTIVATED = 'REACTIVATED'
	APPEAL_STATUS_REQUIRES_DIFFERENT_FORM = 'REQUIRES_DIFFERENT_FORM'
	APPEAL_STATUS_DOCUMENTS_REQUIRED = 'DOCUMENTS_REQUIRED'
	APPEAL_STATUS_PROBLEM_LOGGING_IN = 'PROBLEM_LOGGING_IN'
	APPEAL_STATUS_FORM_SUBMIT_IMAGE_ERROR = 'IMAGE_ERROR'
	APPEAL_STATUS_UNKNOWN = 'UNKNOWN'

	EMAIL_RESPONSE_STATUSES = {
		'CODE_RECEIVED':
		[b'\x87\xe0\xb8\xa5\xe0\xb9\x88\xe0\xb8\xb2\xe0\xb8\x87\xe0\xb8\x99\xe0\xb8\xb5\xe0\xb9\x89',
		 b'Please attach a photo of yourself holding a hand-written copy of the code below',
		 b'Please reply to this email and attach a photo of yourself holding a hand-written copy of the code below',
		 b'reply to this email and attach a photo of yourself holding'
		 b'ein Foto von dir bei, auf dem du ein Blatt Papier mit dem handschriftlich vermerkten, nachfolgenden Code',
		 b'Ti preghiamo di rispondere a questa e-mail allegando una tua foto in cui reggi il codice scritto a mano riportato di seguito',
		 b'crit sur une feuille de papier propre, suivi de votre nom',
		 b'n duke mbajtur nj', #albanian fags
		 b've received a photo that meets'
		 ],

		'ACCOUNT_REACTIVATED':
		[	b'Your account has been reactivated, and you should be able to access it now',
		  b'ponovo aktiviran, pa biste mu sada trebali',
	 	  b'investigated your report and it looks like this is no longer an issue',
			b'account has been reactivated'
		],

		'PROBLEM_LOGGING_IN':
		[	b"It looks like you're having a problem logging in"],

		'REJECTED':
		[b"account has been disabled for",
		 b'If you think your account was disabled by mistake, you can let us know from within the app',
		 b"We disable Instagram accounts that don't follow our Terms of Use",
		 b"determined that you're ineligible to use Instagram",
		 b'https://help.instagram.com/contact/606967319425038',
   
		],

		'IMAGE_ERROR':
		[	b"We can't accept images that are too small, dark or blurry",
		  b"received an acceptable image to verify account ownership"],

		'DOCUMENTS_REQUIRED':
		[	b'Please reply to this email with an attached digital copy of any of the following documents that match']

	}
