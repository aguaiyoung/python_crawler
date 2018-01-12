# -*- coding: utf-8 -*-
"""Train tickets query from CLI.

Usage:
    tickets [-dgktz] <from> <to> <date>

Options:
    -h --help     Show this screen.
    -d            动车
    -g            高铁
    -k            快速
    -t            特快
    -z            直达
"""
import requests
import stations
import json
from datetime import datetime
from docopt import docopt
from prettytable import PrettyTable
from colorama import Fore
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class TrainCollection(object):

    headers = '车次 车站 时间 历时 一等座 二等座 高级软卧 软卧 硬卧 软座 硬座 无座'.split()

    def __init__(self, raw_trains, options):
        self.raw_trains = raw_trains
        self.options = options

    def colored(self, color, string):
        return ''.join([getattr(Fore, color.upper()), string, Fore.RESET])

    def get_from_to_station_name(self, data_list):
        from_station_telecode = data_list[6]
        to_station_telecode = data_list[7]
        return '\n'.join([
            self.colored('green', stations.get_name(from_station_telecode)),
            self.colored('red', stations.get_name(to_station_telecode))
        ])

    def get_start_arrive_time(self, data_list):
        return '\n'.join([
            self.colored('green', data_list[8]),
            self.colored('red', data_list[9])
        ])

    def get_train_color(self, data_list, index, color):
        return '\n'.join([
            self.colored(color, data_list[int(index)]),
        ])

    def parse_train_data(self, data_list):
        #print (data_list)
        value = {
            '11': data_list[3],
            '10': self.get_from_to_station_name(data_list),
            '12': self.get_start_arrive_time(data_list),
            '1': data_list[10],
            '3': data_list[31] or '--',
            '2': data_list[30] or '--',
            '5':data_list[21] or '--',
            #'4': data_list[23] or '--',
            '4': self.get_train_color(data_list, '23', 'yellow') or '--',
            #'7': data_list[28] or '--',
            '7': self.get_train_color(data_list, '28', 'red') or '--',
            '6': data_list[24] or '--',
            '9': data_list[29] or '--',
            '8': data_list[33] or '--'
            }
        #print value
        return value

    def need_print(self, data_list):
        station_train_code = data_list[3]
        initial = station_train_code[0].lower()
        #print self.options + station_train_code + initial
        return (not self.options or initial in self.options)

    @property
    def trains(self):
        for train in self.raw_trains:
            data_list = train.split('|')
            if self.need_print(data_list):
                value = self.parse_train_data(data_list).values()
                #print value
                yield value

    def pretty_print(self):
        pt = PrettyTable()
        pt._set_field_names(self.headers)
        for train in self.trains:
            #print train
            pt.add_row(train)
        print(pt)


class Cli(object):
    url_template = (
        'https://kyfw.12306.cn/otn/'
        'leftTicket/{}?'
        'leftTicketDTO.'
        'train_date={}&'
        'leftTicketDTO.from_station={}&'
        'leftTicketDTO.to_station={}&'
        'purpose_codes=ADULT'
    )

    def __init__(self):
        self.arguments = docopt(__doc__, version='Tickets 1.0')
        self.parse_station()
        print self.arguments['<from>']
        print self.arguments['<to>']
        self.leftTicket = 'queryZ'
        self.from_station = stations.get_telecode(self.arguments['<from>'])
        self.to_station = stations.get_telecode(self.arguments['<to>'])
        self.date = self.arguments['<date>']
        self.check_arguments_validity()
        self.options = ''.join([key for key, value in self.arguments.items() if value is True])

    @property
    def request_url(self):
        return self.url_template.format(self.leftTicket, self.date, self.from_station, self.to_station)

    def parse_station(self):
        if self.arguments['<from>'] == 'bj':
           self.arguments['<from>'] = '北京'
        if self.arguments['<from>'] == 'bjx':
           self.arguments['<from>'] = '北京西'
        if self.arguments['<from>'] == 'jj':
           self.arguments['<from>'] = '九江'
        if self.arguments['<to>'] == 'bj':
           self.arguments['<to>'] = '北京'
        if self.arguments['<to>'] == 'bjx':
           self.arguments['<to>'] = '北京西'
        if self.arguments['<to>'] == 'jj':
           self.arguments['<to>'] = '九江'
        if self.arguments['<to>'] == 'nc':
           self.arguments['<to>'] = '南昌'
        if self.arguments['<to>'] == 'hf':
           self.arguments['<to>'] = '合肥'  
        return

    def check_arguments_validity(self):
        if self.from_station is None or self.to_station is None:
            print(u'请输入有效的车站名称')
            exit()
        try:
            if datetime.strptime(self.date, '%Y-%m-%d') < datetime.now():
                raise ValueError
        except:
            print(u'请输入有效日期 如2017-12-25')
            exit()

    def run(self):
        print (self.request_url)
        r = requests.get(self.request_url, verify=False)
        status = r.json()['status']
        print status
        if status == False:
           print r.json()['c_url']
           url = r.json()['c_url']
           self.leftTicket = url[11:len(url)]
           print self.request_url
           r = requests.get(self.request_url, verify=False)
           status = r.json()['status']
        if status == False:
           exit()
        messages = r.json()['messages']
        if messages == [] or messages == "":
           messages = json.dumps(messages, ensure_ascii = False, encoding = 'utf-8')
           trains = r.json()['data']['result']
           print '                        '+ '\033[1;31;43m' +self.date + u' 火车票剩余情况' +'\033[0m'
           TrainCollection(trains, self.options).pretty_print()
        else:
            messages = json.dumps(messages, ensure_ascii = False, encoding = 'utf-8')
            print '\033[1;31;40m' + messages + '\033[0m'
            exit()


if __name__ == '__main__':
    Cli().run()
