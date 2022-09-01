python3 manager.py

http://127.0.0.1:5000/user------get
http://127.0.0.1:5000/auth------post({
                                        "password": "4331",
                                        "email": "roxep82842@otodir.com"
                                    })
http://127.0.0.1:5000/api/auth/forgot------post({
                                                  "email": "roxep82842@otodir.com"
                                                })
http://127.0.0.1:5000/api/auth/reset------post({
                                                  "password": "新密码",
                                                  "token": "上一步得到的token“
                                                })
