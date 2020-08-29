#-*- coding:utf-8 -*-
#Webtree version 1.0 Beta
#LICENSED BY HILLASEN 2020
#HILLASEN EULA
#Please install flask, os, hashlib, configparser
#Running stable in python 3.8.1

from flask import Flask, request, send_file, jsonify
import os
import litedb
import os
import hashlib

print("Webtree version 1.0.0 beta")
print("LICENSED BY HILLASEN 2020")

app = Flask(__name__)

host_addr = "0.0.0.0"
port_num = "7070" #default webtree port


def bridgeInit(id, passwd):
    ps = hashlib.sha256(passwd.encode())
    print("bridge ps: "+ ps.hexdigest())
    con = "[Login]\nid="+ id +"\nps="+ ps.hexdigest()
    f = open("./files/"+ id + "/info.ini", "w")
    f.write(con)
    f.close()
    return 1

def fileInit(id, ver, name):
    con = "[Fileinfo]\nversion="+ ver +"\nname="+ name +"\nisReleased=true"
    f = open("./files/"+ id + "/" + ver + "/info.ini", 'w')
    f.write(con)
    f.close()
    return 1

def userValid(id, password):
    ps = hashlib.sha256(password.encode())
    return ps.hexdigest() == litedb.getPassword(id)

def getVersions(id):
    path = "./files/" + id + "/"
    file_list = os.listdir(path)
    return file_list

def fileDownload(id, version):
    return true;

@app.route("/versions", methods=['POST'])
def returnVersions():
    print(request.form['id'] + " requested returnVersion")
    if(userValid(request.form['id'], request.form['ps'])):
        print("Showed versions")
        return format(getVersions(request.form['id']))
    else:
        print("Request denied, Error non valid user")
        return "Error non valid user"

@app.route("/download", methods=['POST'])
def fileDownload():
    print(request.form['id'] + " requested fileDownload")
    if(userValid(request.form['id'], request.form['ps'])):
        info = litedb.getFileinfo(request.form['id'], request.form['version'])
        print("Download " + info['name'])
        return send_file("./files/"+ request.form['id'] + "/" + request.form['version'] + "/" + info['name'],  attachment_filename = info['name'], as_attachment=True)
    else:
        print("Request denied, Error non valid user")
        return "Error non valid user"


@app.route("/upload", methods=['POST'])
def fileUpload():
    print(request.form['id'] + " requested fileUpload")
    if(userValid(request.form['id'], request.form['ps'])):
        ver = getVersions(request.form['id'])
        if(request.form['version'] in ver):
            print("(Error) Same version is uploaded!")
            return "(Error) Same version is uploaded!"
        else:
            os.makedirs("./files/"+ request.form['id'] + "/" + request.form['version'])
            f = request.files['file']
            f_name = f.filename
            f_name = f_name.replace("\"", "")
            print(f_name)
            f.save("./files/"+ request.form['id'] + "/" + request.form['version'] + "/" + f_name)
            fileInit(request.form['id'], request.form['version'], f_name)
            print("Uploaded version " + request.form['version'] + " successfully")
            return "Upload success"
    else:
        print("Request denied, Error non valid user")
        return "Error non valid user"

@app.route("/createBridge", methods=['POST'])
def createBridge():
    print(request.form['id'] + " requested createBridge")
    admin = litedb.getAdmin()
    ps = hashlib.sha256(request.form['ps'].encode())
    if(admin['id'] == request.form['id'] and admin['ps'] == ps.hexdigest()):
        print("Admin logged in by " + request.remote_addr)
        os.makedirs("./files/"+ request.form['bridge_id'])
        bridgeInit(request.form['bridge_id'], request.form['bridge_ps'])
        print("Bridge building success! Bridge_id: " + request.form['bridge_id'])
        return "Bridge building success!"
    else:
        print("Request denied, Error non valid admin user")
        return "Error non valid user"

if __name__ == "__main__":              
    app.run(host=host_addr, port=port_num)
