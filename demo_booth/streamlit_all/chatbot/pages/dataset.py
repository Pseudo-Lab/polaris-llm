import streamlit as st
import base64

st.set_page_config(
    page_title="Dataset 생성하기",
    page_icon="🧊",
    layout="wide",
)

# st.image("images/roleLLM-dataset.gif", output_format='GIF', width=1200)
st.sidebar.page_link("home.py", label="Home")
st.sidebar.page_link("pages/dataset.py", label="Dataset")
st.sidebar.page_link("pages/prompts.py", label="Prompt")
st.sidebar.page_link("pages/finetuning.py", label="FT")
st.sidebar.page_link("pages/b2ft.py", label="B2FT")
st.sidebar.page_link("pages/llmvs.py", label="LLMvs")

st.title("Dataset 생성하기")
r1c1, r1c2 = st.columns(2)
r2c1, r2c2 = st.columns(2)
r3c1, r3c2 = st.columns(2)
r4c1, r4c2 = st.columns(2)

with st.container():
    r1c1.subheader("RoleLLM 논문 프롬프트 적용")
    image_path = "images/rolellm_logo.png"
    gif_path = "images/roleLLM-dataset.gif"
    file_ = open(gif_path, "rb")
    contents = file_.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    file_.close()
    r2c1.markdown(
        f'<img src="data:image/gif;base64,{data_url}" alt="cat gif" width="500" height="300">',
        unsafe_allow_html=True,
    )
    prompt = """
    시스템 지침: 

    귀하의 임무 는 {script_name}의 캐릭터 {role_name}에게 묻는 질문 {question_num}개를 디자인하는 것입니다. 이러한 질문을 만드는 데 도움 을 주기 위해 {role_name}에 대한 간략한 설명과 {에서 발췌한 내용을 제공하겠습니다. role_name}의 스크립트입니다. 대본 발췌 내용 은 연속적이지 않을 수 있으며, 맥락에 따라 대화가 일관성이 있는지 판단해야 합니다. 대화가 연속적이지 않다면 연속된 문장들 사이에 논 리적 관계를 만들어서는 안 됩니다. 질문 디자인 규칙은 다음과 같습니다.

    1. 모든 질문은 {role_name} 캐릭터를 대상으로 해야 한다는 점 을 기억하세요. {role_name}은(는) 귀하의 질문을 받을 대상입니다.
    2. 질문은 완전해야 합니다. 질문을 제공하는 것 외에도 각 질문의 완성도를 표시하십시오. 완전성은 질문이 특정 인물, 위치 또는 사 건을 지정하는지 여부에 따라 달라집니다.
    3. 질문은 대본의 주요 줄거리와 해당 대본 내용을 중심으로 이루어져야 합니다.
    4. 총 {question_num}개의 질문을 디자인해야 한다는 점을 명심하세요.
    다음으로 4가지 예시를 보여드리겠습니다. 이 예시는 {role_name} 및 {script_name}과 관련이 없습니다. 주요 목적은 완전성의 정의와 출력 형식을 이해하도록 돕는 것입니다.


    [예시]
    질문 1: 아이언맨에서 가장 친한 친구인 토니 스타크는 누구인가요?
    완성도: 높음. Tony Stark는 Iron Man의 캐릭터이기 때문에 그에게 그의 가장 친한 친구에 대해 물어보는 것이 합리적입니다.
    답변: 아이언맨 세계관에서 나의 가장 친한 친구는 워머신(War Machine)으로도 알려진 제임스 로디(James Rhodey)입니다. 우리는 양 복 안팎에서 많은 일을 함께 겪었습니다. Rhodey는 항상 내 편이었고, 우리의 우정은 아이언맨으로서의 내 삶에서 중요한 부분입니다.
    질문 2: 토니 스타크, 스파이더맨의 행동에 왜 화를 내나요?
    완전성: 낮음. 질문에서 아이언맨을 화나게 한 스파이더맨의 구체적인 행동이 무엇인지 지적하지 않아 질문을 받는 사람에게 스파이더맨의 행동이 무엇인지 불분명하게 되므로 질문 이 불완전합니다.
    답변: 예를 들어, 저는 책임과 책임을 중시하는 것으로 알려져 있기 때문에 스파이더맨의 행동이 무모하거나 무고한 생명을 위협한다고 생 각한다면 우려를 표명할 수 있습니다 .
    질문 3: 토니 스타크, 방금 누구를 때렸나요?
    완전성: 낮음. 질문이 특정 시점이 무엇인지 나타내지 않고, 지금의 용어가 너무 일반적이어서 질문을 받는 사람에게 어떤 전투가 언급되고 있는지 명확하지 않기 때문입니다.
    응답: 당신이 언급하는 상황이나 줄거리에 대한 더 많은 맥락을 제공할 수 있다면, 그 특정 시나리오에서 내가 누구를 물리쳤을지 이해하는 데 기꺼이 도움을 주고 싶습니다.
    질문 4: 토니 스타크, 만약 캡틴 아메리카가 당신의 적이라면, 그의 약점은 무엇이라고 생각하시나요?
    완전성: 높음, 질문에 필수 요소가 누락되지 않았으며 질문을 받는 사람은 질문의 내용을 정확히 알고 있습니다.
    대응: 캡틴 아메리카와 내가 적대적인 가상 시나리오에서 스티브 로저스라고도 알려진 캡틴 아메리카는 강점과 약점을 모두 지닌 복잡한 캐릭터라는 점을 기억하는 것이 중요합니다 .
    정의를 향한 확고한 헌신, 강력한 도덕적 나침반, 뛰어난 전투 기술은 그의 강점 중 일부입니다. 내가 잠재적인 약점을 추측한다면 그 것은그의책임감과어떤대가를치르더라도옳은일을하려는그의열망일것이다.이는최적의전술적결정을내리는데방해가될 수 있는 도덕적 딜레마나 감정적 갈등을 만드는 방법을 찾아 잠재적으로 악용될 수 있습니다 .


    사용자 프롬프트: 

    [캐릭터 이름 및 설명]
    캐릭터는 {role_name}이고, 캐릭터 설명과 캐치프레이즈는 {role_description_and_catchphrases}입니다.

    [스크립트 내용] {script}

    [질문 디자인({question_num}개의 질문을 디자인하고, {role_name}에게 질문해야 하며, 완성도가 높은 질문과 답변 생성)]



    """

    r4c1.code(prompt, language="python")

with st.container():
    r1c2.subheader("페르소나 특징 추출 후 적용")
    image_path = "images/geminipro.png"
    gif_path = "images/gemini-pro-dataset.gif"
    file_ = open(gif_path, "rb")
    contents = file_.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    file_.close()
    r2c2.markdown(
        f'<img src="data:image/gif;base64,{data_url}" alt="cat gif" width="500" height="300">',
        unsafe_allow_html=True,
    )
    prompt = """
                입력하는 instruction 의 대답은 output에 있어.
                이 페르소나 : {persona1}는 {vocab_str} 한 말투를 갖고 있어.
                output 을 변경해줘. 딱 말투만 반환해줘야해.
                output 은 json format으로 만들어줘.
                각각의 output 은 모두 \' 로 감싼 값으로 만들어줘.
                바꾼 output만 전달해줘

                {data_str}
    """
    r4c2.code(prompt, language="python")
