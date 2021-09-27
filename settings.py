from os import environ

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']
# participant_settings = {
#     'student_id':0,
# }
mturk_hit_settings = {
    'keywords': ['financial', 'tax', 'study', 'academic'],
    'title': 'Trust game (few minutes to complete, earn real money!)',
    'description': 'Assess corporate tax strategies of companies for $1.05 for about 7 minutes.',
    'frame_height': 500,
    #'preview_template': 'global/MTurkPreview.html',
    'template': 'global/mturk_template.html',
    'minutes_allotted_per_assignment': 45,
    'expiration_hours': 7*24, # 7 days
    #'grant_qualification_id': 'YOUR_QUALIFICATION_ID_HERE',# to prevent retakes
    'qualification_requirements': [
        # No-retakers
        {
            'QualificationTypeId': "30LLG2NWCXJ09FSUO3LGVGEKYUS095",
            'Comparator': "DoesNotExist",
        },
        # Only US
        {
            'QualificationTypeId': "00000000000000000071",
            'Comparator': "EqualTo",
            'LocaleValues': [{'Country': "US"}]
        },
        # At least x HITs approved
        {
            'QualificationTypeId': "00000000000000000040",
            'Comparator': "GreaterThanOrEqualTo",
            'IntegerValues': [500]
        },
        # At least x% of HITs approved
        {
            'QualificationTypeId': "000000000000000000L0",
            'Comparator': "GreaterThanOrEqualTo",
            'IntegerValues': [98]
        },
        ]
}

SESSION_CONFIG_DEFAULTS = {
    'real_world_currency_per_point': 1.00,
    'participation_fee': 0.00,
    'doc': "",
    'mturk_hit_settings': mturk_hit_settings,
}

SESSION_CONFIGS = [

    dict(
        name='select_game_12',
        display_name="select_game_12",
        num_demo_participants=12,
        #num_rounds=2,
        app_sequence=['my_trust'],
    ),
    dict(
        name='select_game_25',
        display_name="select_game_25",
        num_demo_participants=25,
        #num_rounds=2,
        app_sequence=['my_trust_25'],
    ),

]


# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ROOMS = []

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = 'v*lczl+n+of(f6r@hjn$g9y-b)1e5(to4)um646i(8hux$5gq)'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']

AWS_ACCESS_KEY_ID = environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET_ACCESS_KEY')