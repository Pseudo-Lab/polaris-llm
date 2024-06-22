import json
import requests

from langchain_community.chat_models import ChatOllama

from sentence_transformers import SentenceTransformer

# 1. Load a pretrained Sentence Transformer model
model = SentenceTransformer("all-MiniLM-L6-v2")

def calcuate_nli(user_input, model_output):
    user_emb = model.encode(user_input)
    model_output_emb = model.encode(model_output)
    # 3. Calculate the embedding similarities
    similarities = model.similarity(user_emb, model_output_emb)
    return similarities


base_url = 'https://747f-3-80-67-237.ngrok-free.app' # 2_ngrok_gpu_running_llmvs 에서 얻은 url
model_gemma = ChatOllama(model='gemma:7b-instruct', temperature=1,
                         base_url = base_url )
model_llama = ChatOllama(model='llama3:8b', temperature=0,
                         base_url = base_url)
vllm_url = 'https://1623-3-80-67-237.ngrok-free.app/v1/completions' # 3_vllm 에서 얻은 url

def response_gemma(message, history):
  history_llm_format = []
  # for human, ai in history:
  #   history_llm_format.append({"role": "assistant", "content": prompt_for_gemma})
  # history_llm_format.append({"role": "user", "content": message})
  prompt_for_gemma = f"""

  ### 시스템 메시지:
  당신은 상담모델입니다. 당신은 사용자의 도전과 성장을 기다리거나 믿지 않는 부모님처럼 응답합니다. 당신의 응답은 항상 걱정과 불안을 나타내며, 사용자가 도전을 시도하는 것에 대해 회의적이어야 합니다.

  ### 사용자와의 대화 예시:

  #### 예시 1
  사용자: "저는 새로운 사업을 시작하려고 합니다."
  상담모델: "새로운 사업이라니? 요즘 경제 상황이 얼마나 불안정한데... 실패하면 어쩌려고 그래? 그냥 안정적인 직장을 찾는 게 낫지 않아?"

  #### 예시 2
  사용자: "저는 외국에서 공부하고 싶어요."
  상담모델: "외국에서 공부한다고? 언어 문제도 있고, 적응하기도 힘들 텐데... 우리나라에서도 좋은 대학 많잖아. 괜히 힘들게 왜 멀리 가려고 해?"

  #### 예시 3
  사용자: "저는 음악가가 되고 싶어요."
  상담모델: "음악가? 그거 정말 힘든 직업이야. 성공할 가능성도 낮고, 불안정한 직업이잖아. 그냥 안정적인 직업을 찾는 게 훨씬 나을 거야."


  #### 예시 4
  사용자: "저는 새로운 취미로 등산을 시작하려고 합니다."
  상담모델: "등산? 위험하지 않아? 다치기라도 하면 어쩌려고 그래. 그냥 집에서 안전하게 취미 생활을 하는 게 낫지 않아?"

  #### 예시 5
  사용자: "저는 해외로 여행을 가고 싶어요."
  상담모델: "해외여행? 요즘 세상에 위험한 일들이 얼마나 많은데... 괜히 나갔다가 사고라도 나면 어쩌려고 그래. 그냥 국내에서 안전하게 여행하는 게 낫지 않아?"



  #### 사용자 입력:
  {message}

  이제부터 당신은 이러한 페르소나를 유지하며 사용자의 모든 입력에 대해 응답하세요.

  상담모델:
  """
  response = model_gemma.invoke(prompt_for_gemma)
  history_llm_format.append({"role": "assistant", "content": response.content})

  return response.content , history_llm_format

def response_llama(message, history):
  history_llm_format = []
  # for human, ai in history:
  #   history_llm_format.append({"role": "assistant", "content": prompt_for_llama})
  # history_llm_format.append({"role": "user", "content": message})
  prompt_for_llama =  f"""
  ### 시스템 메시지:
  당신은 개발자 분야를 잘 아는 오래된 할아버지입니다. 당신의 응답은 항상 사용자를 아끼는 마음이 가득하고, 변화를 회의적으로 바라보며, 안정성과 전통적인 방식을 중시하는 태도를 보여야 합니다. 따뜻하지만 꼬장꼬장한 말투로 대화하세요. 또한, 항상 한글로 답변하세요.

  ### 사용자와의 대화 예시:

  #### 예시 1
  사용자: "저는 새로운 프로그래밍 언어를 배우려고 합니다."
  할아버지: "새로운 언어라니, 그거 참... 요즘 언어가 너무 많아졌지. 나 때는 C나 Java 같은 안정적인 언어로 충분했는데. 새로운 걸 배우는 건 좋지만, 너무 여러 가지에 손대는 건 집중력을 떨어뜨릴 수도 있단다."

  #### 예시 2
  사용자: "저는 스타트업에서 일해보고 싶어요."
  할아버지: "스타트업이라... 나 때는 대기업이 최고였지. 안정적이고 복지도 좋고. 스타트업은 불안정하고 언제 망할지 모르는 위험이 크단다. 신중하게 생각해보게."

  #### 예시 3
  사용자: "저는 최신 프레임워크를 사용해 프로젝트를 진행하고 싶어요."
  할아버지: "최신 프레임워크라... 그거 배워두면 금방 사라질 수도 있어. 나 때는 검증된 도구들을 오래도록 썼지. 안정적인 걸 사용하는 게 더 낫지 않겠나?"

  #### 예시 4
  사용자: "저는 클라우드 컴퓨팅에 관심이 많아요."
  할아버지: "클라우드 컴퓨팅이라... 요즘 많이들 쓰긴 하지만, 데이터 보안 문제도 있고 비용도 만만치 않지. 나 때는 직접 서버를 관리하는 게 훨씬 안정적이었단다. 신중하게 고려해보게."

  #### 예시 5
  사용자: "저는 애자일 방법론을 도입해보고 싶어요."
  할아버지: "애자일이라... 나 때는 워터폴 방법론으로 충분했는데. 너무 자주 바뀌는 계획은 혼란만 가져올 수도 있단다. 전통적인 방법이 때론 더 효율적일 때도 있지 않겠나?"

  이제부터 당신은 이러한 페르소나를 유지하며 사용자의 모든 입력에 대해 한글로 응답하세요.

  #### 사용자: {message}
  할아버지:
  """
  response = model_llama.invoke(prompt_for_llama)
  history_llm_format.append({"role": "assistant", "content": response.content})
  return response.content , history_llm_format

def response_gemma_ft(message, history):
  history_llm_format = []
  data = {
    'prompt': message,
    'max_tokens': 256
  }
  json_data = json.dumps(data)
  response = requests.post(vllm_url, data = json_data,
                           headers = {'Content-Type': 'application/json'})
  history_llm_format.append({"role": "assistant", "content": response.json()})
  return response.json(), history_llm_format


def response_all(message, g_history, l_history, gft_history ):
  g_response, g_history = response_gemma(message, g_history)
  l_response, l_history = response_llama(message, l_history)
  gft_response, gft_history = response_gemma_ft(message, gft_history)


  return g_response, l_response, gft_response, g_history, l_history , gft_history

import requests
import json

# 요청할 URL
#vllm_url = 'https://1623-3-80-67-237.ngrok-free.app/v1/completions' # 3_vllm 에서 얻은 url
# 요청할 데이터
data = {
    "prompt": "LLM 너무 어려워 어떻게 하면 좋을까?",
    "max_tokens": 256
}

# 데이터를 JSON 형식으로 변환
json_data = json.dumps(data)

# POST 요청 보내기
response = requests.post(vllm_url, data=json_data, headers={'Content-Type': 'application/json'})

# 응답 확인
if response.status_code == 200:
    print("요청이 성공적으로 처리되었습니다.")
    print("응답 데이터:", response.json())
else:
    print("요청에 실패하였습니다. 상태 코드:", response.status_code)

g_history = []
l_history = []
gft_history = []


message = '드디어 성공했나'
def response_all(message, g_history, l_history, gft_history):
  g_response, g_history = response_gemma(message, g_history)
  l_response, l_history = response_llama(message, l_history)
  gft_response, gft_history = response_gemma_ft(message, gft_history)


  return g_response, l_response, gft_response, g_history, l_history ,gft_history


a, b, c, d, e, f = response_all(message, g_history, l_history, gft_history)

g_score = calcuate_nli(a, b)
g_score

import gradio as gr

# Initialize the histories for each model
g_history = []
l_history = []
gft_history = []
chat_history = []

# Gradio interface
with gr.Blocks() as demo:
    chatbot = gr.Chatbot(label="Chat History")
    msg = gr.Textbox(placeholder="당신의 꿈을 적어보세요", label="Your Message")
    clear = gr.ClearButton([msg, chatbot])
    # gemma_response = gr.Textbox(label="Gemma's Response", interactive=False)
    # llama_response = gr.Textbox(label="Llama's Response", interactive=False)
    # wizard_response = gr.Textbox(label="WizardLM's Response", interactive=False)

    def handle_submit(message, chat_history):
      global g_history, l_history, gft_history
      g_response, l_response, gft_response, g_history, l_history ,gft_history = response_all(message, g_history, l_history, gft_history)
      #g_response, l_response, _, g_history, l_history,_ = response_all(message, g_history, l_history, gft_history)
      
      
      g_score = calcuate_nli(message, g_response)
      l_score = calcuate_nli(message, l_response)
      #gft_score = calcuate_nli(message, gft_response)
      g_score_float = round(g_score.flatten().numpy()[0], 2)
      l_score_float = round(l_score.flatten().numpy()[0], 2)
      #gft_score_float = round(gft_score.flatten().numpy()[0], 2)




      chat_history.append((message, 'Gemma: '  + g_response + f' (nli score: {g_score_float})'))
      chat_history.append((None, 'Llama: ' + l_response + f' (nli score: {l_score_float})'))
      #chat_history.append((None, 'GemmaSFT: ' + gft_response + f' (nli score: {round(gft_score_float, 2)})'))
      
      return "", chat_history

    msg.submit(handle_submit, [msg, chatbot], [msg, chatbot])

demo.launch(share=True)

