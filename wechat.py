import itchat
import requests
import time
import os

quit_users={u'\u5b59\u6dfc\u6dfc':100}
blank_users={'itchat':True}

# get reply from tuling
def get_response(msg):
  apiUrl = 'http://www.tuling123.com/openapi/api'
  data = {
    'key': '92e67a3a17d14e3f989c5a55d044ea00',
    'info': msg,
    'userid': 'wechat-robot',
  }

  r = requests.post(apiUrl, data=data).json()
  re_msg = r.get('text') + '(this is auto reply from liuchang\'s robot, say\'quit\' to avoid)'
#  return r.get('text')
  return re_msg

@itchat.msg_register(itchat.content.TEXT)
def print_content(msg):
  print(msg)
  #print(dir(msg))
  print(msg['User'])
  print(msg['Text'])
  print('------------------------------------------')
  msg_txt = msg['Text']
  # add user to quit_list, to avoid reply to them
  if msg_txt == 'quit' :
    quit_user = {msg['User']['NickName']:100}
    quit_users.update(quit_user)
  # start robot by remove user from quit_list
  if msg_txt == 'start' :
    user = msg['User']['NickName']
    quit_users.pop(user)

  # dont reply to blank_list
  if blank_users.has_key(msg['User']['NickName']):
    return
  # dont reply to quit_user, but remind them after 100 times dialog
  if quit_users.has_key(msg['User']['NickName']):
    value = quit_users.get(msg['User']['NickName'])
    value = value - 1
    quit_user = {msg['User']['NickName']:value}
    quit_users.update(quit_user)
    if value == 0:
      value == 100
      return 'if you want robot u can type \'start\''
    else:
      return
  else:
    return get_response(msg['Text'])

# GroupChat
#@itchat.msg_register([itchat.content.TEXT], isGroupChat=False)
#def print_content(msg):
#  return get_response(msg['Text'])

# start auto reply
itchat.auto_login(True)
itchat.run()
