import os
import environ
from openai import OpenAI
from .system_role import BASE_ROLE, DETAIL_ROLE

""" Memo
temperature 조정
- 0.5 ~ 1 사이로 설정
- 기본값은 0.7
- 낮을수록 팩트에 기반, 높을수록 창의적

활용 가능 모델
- gpt-4o-mini
- gpt-3.5-turbo
- dall-e-3
"""


def get_old_messages(messages):
  # database에서 꺼낸 기존 대화 내용
  old_messages = []

  # 요청, 응답 나누어 OpenAI API 포맷에 맞추기
  for message in messages:
    if message.type == 'request':
      old_message = {
        "role": 'user',
        "content": message.content
      }
    else:
      old_message = {
        "role": 'assistant',
        "content": message.content
      }

    old_messages.append(old_message)

  return old_messages


def get_full_messages(message_type, old_messages, user_input):
  # 시스템 역할
  messages = [
    {
      "role": "system",
      "content": BASE_ROLE
    },
    {
      "role": "system",
      "content": DETAIL_ROLE[message_type]
    },
  ]
  
  # 이전 대화 내용
  if old_messages:
    messages += old_messages
  
  # 유저 질문
  messages.append({
      "role": "user",
      "content": user_input
    })
  
  return messages
  
  
def generate_completion(messages):
  env = environ.Env(DEBUG=(bool, True))
  environ.Env.read_env(
    env_file = os.path.join('', '.env')
  )
  OpenAI.api_key = env('OPENAI_API_KEY')
  client = OpenAI()

  completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages
  )

  return completion.choices[0].message.content.strip()
