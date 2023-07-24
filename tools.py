# -*- coding:utf-8 -*-
"""
Created on  # 15:45  15:45
@author: Gong Zhang
"""
from optparse import OptionParser

def options_func():
    optParser = OptionParser()
    optParser.add_option("--model", action="store", type="str", dest='model', default='snowboy/resources/models/ChatPi.pmdl',
                         help="Put your own model in snowboy/resources/models. The default model is ChatPi.pmdl")
    optParser.add_option("--duration", action="store", type="int", dest='duration', default=5,
                         help="How many seconds you question will last. The default duration is 5")
    options, arguments = optParser.parse_args()
    print('{:-^50}'.format('Options')+'\n\n')
    opt_dict =dict(eval(str(options)))
    print('{:-^43}'.format('-'))
    print('|{0:<20}|  {1:<20}|'.format('Parameter options', 'Value'))
    print('{:-^43}'.format('-'))
    for key, value in opt_dict.items():
        print('|{0:<20}|  {1:<20}|'.format(key, value))
        print('{:-^43}'.format('-'))
    print('\n\n'+'{:-^50}'.format('End'))
    return options, arguments