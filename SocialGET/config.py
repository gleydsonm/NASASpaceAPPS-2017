# Enable Debug
VERBOSE = 0

# Using ISO3166 table country codes
LANGS = [ 'pt_BR', 'en_US' ]

# Light climate changes list
WEATHER_EXPRS_1 = {
    'pt_BR' : [ 'chovendo', 'chover', 'chuva', 'neblina', 'sol', 'precipitacao, ''quente' ],
    'en_US' : [ 'rain', 'sun', 'raining', 'sunny' ]
}

# Severe climate change list
WEATHER_EXPRS_2 = {
    'pt_BR' : [ 'tempestade', 'granizo', 'chuva torrencial',  ],
    'en_US' : [ 'storm', 'snow' ]
}

# Critical climate list
WEATHER_EXPRS_3 = {
    'pt_BR' : [ 'terremoto', 'tsunami', 'lava', 'vulcao', 'tremor', 'tornado', 'escala richter' ],
    'en_US' : [ 'tsunami', 'earthquake', 'vulcan', 'hurricane', 'magnitude scale', 'volcanic eruption' ]
}
