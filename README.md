如何创建restful project：

mkdir project-name

pip install virtualenv

virtualenv env

source env/bin/activate

pip install flask/flask-restful/...

flask run

数据库迁移的 python3 app.py db migrate


python3 manager.py

1 http://127.0.0.1:5000/user------get

2 http://127.0.0.1:5000/auth------post({
                                        "password": "4331",
                                        "email": "roxep82842@otodir.com"
                                    })
                                    
3http://127.0.0.1:5000/api/auth/forgot------post({
                                                  "email": "roxep82842@otodir.com"
                                                })
                                                
4http://127.0.0.1:5000/api/auth/reset------post({
                                                  "password": "new password",
                                                  "token": "The token obtained in the previous step“
                                                })
                                                

(roxep82842@otodir.com) is a temporary mailbox
