CREDENTIALS_FILE = 'analytics/services/algo360_credentials.json'

CREDIT_LIMIT_VARIABLES = ['monthly_average_balance_lifetime', 'monthly_average_balance_12',
                          'monthly_average_balance_6', 'monthly_average_balance_3', 'monthly_average_balance_1', 'salary']

ALGO360_UPWARDS_MAPPING = {
    'var201093': 'monthly_average_balance_lifetime',
    'var201094': 'monthly_average_balance_12',
    'var201095': 'monthly_average_balance_6',
    'var201096': 'monthly_average_balance_3',
    'var201097': 'monthly_average_balance_1',
    'var201204': 'number_of_cheque_bounce_1',
    'var201203': 'number_of_cheque_bounce_3',
    'var202003': 'is_credit_card_overlimited',
    'var202064': 'credit_card_last_payment_due',
    'var101003': 'salary',
}


CREDIT_REPORT_MAPPING = {
    'Algo360': {
        'monthly_average_balance_lifetime': 'monthly_average_balance_lifetime',
        'monthly_average_balance_12': 'monthly_average_balance_12',
        'monthly_average_balance_6': 'monthly_average_balance_6',
        'monthly_average_balance_3': 'monthly_average_balance_3',
        'monthly_average_balance_1': 'monthly_average_balance_1',
        'number_of_cheque_bounce_1': 'number_of_cheque_bounce_1',
        'number_of_cheque_bounce_3': 'number_of_cheque_bounce_3',
        'is_credit_card_overlimited': 'is_credit_card_overlimited',
        'credit_card_last_payment_due': 'credit_card_last_payment_due',
        'salary': 'algo360_salary',
    },

    'Profession': {
        'salary': 'user_input_salary',

    },
}
