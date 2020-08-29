#Litedb for Webtree version 1.0. beta
#LICENSED BY HILLASEN 2020
#HILLASEN EULA
#Please install flask, os, hashlib, configparser
#Running stable in python 3.8.1

import configparser

def getPassword(id):
    config = configparser.ConfigParser()
    config.read('files/'+ id +'/info.ini')
    sec = config.sections()
    login = config['Login']
    return login['ps']

def getFileinfo(id, ver):
    config = configparser.ConfigParser()
    config.read('files/'+ id +'/'+ ver + '/info.ini')
    sec = config.sections()
    info = config['Fileinfo']
    return info

def getAdmin():
    config = configparser.ConfigParser()
    config.read('files/admin.ini')
    sec = config.sections()
    login = config['Login']
    return login
