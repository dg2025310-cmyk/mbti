import streamlit as st
import requests
import random

# =========================
# 기본 설정
# =========================
st.set_page_config(
    page_title="MBTI 포켓몬 추천소",
    page_icon="✨",
    layout="centered"
)

# =========================
# CSS 꾸미기
# =========================
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #fff6f6 0%, #f4fbff 50%, #fffbea 100%);
    }

    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: 900;
        color: #ff6b81;
        margin-bottom: 5px;
    }

    .sub-title {
        text-align: center;
        font-size: 18px;
        color: #555;
        margin-bottom: 30px;
    }

    .pokemon-card {
        background-color: white;
        padding: 28px;
        border-radius: 25px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.12);
        text-align: center;
        border: 3px solid #ffe1e8;
        margin-top: 20px;
    }

    .pokemon-name {
        font-size: 34px;
        font-weight: 900;
        color: #ff6b81;
        margin-bottom: 10px;
    }

    .mbti-badge {
        display: inline-block;
        background-color: #ffdeeb;
        color: #d6336c;
        padding: 8px 16px;
        border-radius: 999px;
        font-weight: 800;
        margin-bottom: 12px;
    }

    .tag {
        display: inline-block;
        background-color: #e7f5ff;
        color: #1c7ed6;
        padding: 6px 12px;
        border-radius: 999px;
        font-size: 14px;
        margin: 4px;
        font-weight: 700;
    }

    .reason-box {
        background-color: #fff9db;
        padding: 18px;
        border-radius: 18px;
        margin-top: 18px;
        color: #444;
        line-height: 1.7;
        border: 2px dashed #ffd43b;
        text-align: left;
    }

    .small-card {
        background-color: white;
        border-radius: 18px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 4px 14px rgba(0,0,0,0.08);
        border: 2px solid #edf2ff;
        min-height: 390px;
    }

    .friend-mbti {
        display: inline-block;
        background-color: #fff0f6;
        color: #c2255c;
        padding: 5px 10px;
        border-radius: 999px;
        font-weight: 800;
        font-size: 13px;
        margin-top: 6px;
        margin-bottom: 4px;
    }

    .bad-mbti {
        display: inline-block;
        background-color: #f1f3f5;
        color: #495057;
        padding: 5px 10px;
        border-radius: 999px;
        font-weight: 800;
        font-size: 13px;
        margin-top: 4px;
        margin-bottom: 6px;
    }

    .footer {
        text-align: center;
        color: #777;
        font-size: 14px;
        margin-top: 40px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# MBTI별 포켓몬 데이터
# =========================
pokemon_data = {
    "ISTJ": {
        "pokemon": "Snorlax",
        "korean": "잠만보",
        "emoji": "😴",
        "number": 143,
        "title": "믿음직한 루틴의 수호자",
        "reason": "ISTJ는 성실하고 책임감이 강한 타입이에요. 잠만보처럼 묵직하고 안정적인 에너지를 가지고 있으며, 한번 마음먹은 일은 꾸준히 해내는 힘이 있어요.",
        "tags": ["성실함", "안정감", "꾸준함", "믿음직함"]
    },
    "ISFJ": {
        "pokemon": "Chansey",
        "korean": "럭키",
        "emoji": "🥚",
        "number": 113,
        "title": "따뜻한 마음의 힐러",
        "reason": "ISFJ는 주변 사람을 세심하게 챙기는 다정한 타입이에요. 럭키처럼 누군가를 돌보고 위로하는 데 큰 재능이 있어요.",
        "tags": ["배려", "친절", "보호본능", "따뜻함"]
    },
    "INFJ": {
        "pokemon": "Gardevoir",
        "korean": "가디안",
        "emoji": "🌙",
        "number": 282,
        "title": "깊은 통찰을 가진 조용한 이상가",
        "reason": "INFJ는 조용하지만 마음속에 강한 신념과 이상을 품고 있어요. 가디안처럼 소중한 사람을 위해 강해질 수 있는 타입이에요.",
        "tags": ["통찰력", "이상주의", "섬세함", "신념"]
    },
    "INTJ": {
        "pokemon": "Mewtwo",
        "korean": "뮤츠",
        "emoji": "🧠",
        "number": 150,
        "title": "전략적인 천재 연구가",
        "reason": "INTJ는 분석적이고 독립적인 사고를 잘하는 타입이에요. 뮤츠처럼 강력한 지성과 냉철함을 바탕으로 자신만의 길을 개척해요.",
        "tags": ["전략", "분석", "독립심", "집중력"]
    },
    "ISTP": {
        "pokemon": "Lucario",
        "korean": "루카리오",
        "emoji": "🥋",
        "number": 448,
        "title": "침착한 실전 해결사",
        "reason": "ISTP는 말보다 행동으로 보여주는 타입이에요. 루카리오처럼 상황을 빠르게 파악하고 필요한 순간에 정확하게 움직이는 능력이 있어요.",
        "tags": ["실용적", "침착함", "순발력", "해결사"]
    },
    "ISFP": {
        "pokemon": "Eevee",
        "korean": "이브이",
        "emoji": "🦊",
        "number": 133,
        "title": "가능성이 가득한 감성 아티스트",
        "reason": "ISFP는 자유롭고 감성적인 매력이 있는 타입이에요. 이브이처럼 다양한 가능성을 품고 있으며, 자신만의 방식으로 성장해요.",
        "tags": ["감성", "자유로움", "가능성", "개성"]
    },
    "INFP": {
        "pokemon": "Jirachi",
        "korean": "지라치",
        "emoji": "⭐",
        "number": 385,
        "title": "꿈을 품은 별빛 몽상가",
        "reason": "INFP는 마음속에 따뜻한 가치관과 상상력을 품고 있어요. 지라치처럼 누군가의 소원을 소중히 여기고, 순수한 꿈을 간직하는 타입이에요.",
        "tags": ["상상력", "순수함", "이상", "공감"]
    },
    "INTP": {
        "pokemon": "Alakazam",
        "korean": "후딘",
        "emoji": "🔮",
        "number": 65,
        "title": "끝없이 탐구하는 논리 마법사",
        "reason": "INTP는 호기심이 많고 논리적인 탐구를 좋아해요. 후딘처럼 지적인 에너지가 강하며, 복잡한 문제를 생각하는 데 즐거움을 느껴요.",
        "tags": ["논리", "호기심", "탐구", "아이디어"]
    },
    "ESTP": {
        "pokemon": "Charizard",
        "korean": "리자몽",
        "emoji": "🔥",
        "number": 6,
        "title": "무대 위의 불꽃 에이스",
        "reason": "ESTP는 에너지가 넘치고 도전을 즐기는 타입이에요. 리자몽처럼 강렬한 존재감과 추진력으로 분위기를 이끌어요.",
        "tags": ["도전", "활동적", "자신감", "추진력"]
    },
    "ESFP": {
        "pokemon": "Pikachu",
        "korean": "피카츄",
        "emoji": "⚡",
        "number": 25,
        "title": "모두를 웃게 하는 분위기 메이커",
        "reason": "ESFP는 밝고 사교적인 매력으로 주변을 즐겁게 만들어요. 피카츄처럼 귀엽고 활기찬 에너지가 가득한 타입이에요.",
        "tags": ["사교성", "밝음", "매력", "즐거움"]
    },
    "ENFP": {
        "pokemon": "Sylveon",
        "korean": "님피아",
        "emoji": "🎀",
        "number": 700,
        "title": "사랑스러운 아이디어 요정",
        "reason": "ENFP는 상상력과 에너지가 풍부하고 사람들과 연결되는 것을 좋아해요. 님피아처럼 따뜻하고 사랑스러운 분위기로 주변을 물들여요.",
        "tags": ["열정", "아이디어", "친화력", "긍정"]
    },
    "ENTP": {
        "pokemon": "Gengar",
        "korean": "팬텀",
        "emoji": "👻",
        "number": 94,
        "title": "장난기 넘치는 아이디어 발명가",
        "reason": "ENTP는 재치 있고 새로운 시도를 좋아하는 타입이에요. 팬텀처럼 장난스럽지만 똑똑하고, 예측할 수 없는 매력이 있어요.",
        "tags": ["재치", "창의성", "토론", "장난기"]
    },
    "ESTJ": {
        "pokemon": "Machamp",
        "korean": "괴력몬",
        "emoji": "💪",
        "number": 68,
        "title": "강력한 실행력의 리더",
        "reason": "ESTJ는 체계적이고 목표 달성에 강한 타입이에요. 괴력몬처럼 힘 있고 든든하게 팀을 이끄는 실행력이 돋보여요.",
        "tags": ["리더십", "실행력", "체계적", "책임감"]
    },
    "ESFJ": {
        "pokemon": "Togekiss",
        "korean": "토게키스",
        "emoji": "🪽",
        "number": 468,
        "title": "행복을 나누는 다정한 친구",
        "reason": "ESFJ는 사람들과 조화롭게 지내는 것을 중요하게 생각해요. 토게키스처럼 평화롭고 따뜻한 에너지를 나누는 타입이에요.",
        "tags": ["친화력", "배려", "조화", "다정함"]
    },
    "ENFJ": {
        "pokemon": "Dragonite",
        "korean": "망나뇽",
        "emoji": "🐉",
        "number": 149,
        "title": "모두를 품는 따뜻한 리더",
        "reason": "ENFJ는 사람들을 이끌고 응원하는 데 능숙한 타입이에요. 망나뇽처럼 강하지만 부드럽고, 주변 사람들에게 안정감을 줘요.",
        "tags": ["리더십", "따뜻함", "응원", "포용력"]
    },
    "ENTJ": {
        "pokemon": "Metagross",
        "korean": "메타그로스",
        "emoji": "🤖",
        "number": 376,
        "title": "전략과 실행의 강철 사령관",
        "reason": "ENTJ는 목표 지향적이고 전략적인 리더 타입이에요. 메타그로스처럼 냉철한 판단력과 강한 추진력으로 큰 목표를 향해 나아가요.",
        "tags": ["전략", "목표지향", "카리스마", "추진력"]
    }
}

# =========================
# 보너스 추천용 포켓몬
# 잘 맞는 MBTI, 잘 맞지 않는 MBTI 포함
# =========================
bonus_pokemon = [
    {
        "name": "꼬부기",
        "eng": "Squirtle",
        "number": 7,
        "emoji": "💧",
        "good_mbti": "ISFJ",
        "bad_mbti": "ENTP",
        "good_reason": "차분하고 다정하게 곁을 지켜주는 성향과 잘 어울려요.",
        "bad_reason": "꼬부기는 안정적인 분위기를 좋아해서 너무 즉흥적이고 장난기 많은 성향과는 가끔 삐걱거릴 수 있어요."
    },
    {
        "name": "이상해씨",
        "eng": "Bulbasaur",
        "number": 1,
        "emoji": "🌱",
        "good_mbti": "INFJ",
        "bad_mbti": "ESTP",
        "good_reason": "조용하지만 따뜻한 성장 에너지가 닮았어요.",
        "bad_reason": "이상해씨는 천천히 성장하는 스타일이라 빠른 자극과 모험을 좋아하는 성향과는 속도가 다를 수 있어요."
    },
    {
        "name": "파이리",
        "eng": "Charmander",
        "number": 4,
        "emoji": "🔥",
        "good_mbti": "ESTP",
        "bad_mbti": "ISFJ",
        "good_reason": "활발하고 도전을 즐기는 불꽃 같은 성향과 찰떡이에요.",
        "bad_reason": "파이리의 뜨거운 도전 정신이 조심스럽고 안정적인 성향에게는 조금 부담스러울 수 있어요."
    },
    {
        "name": "푸린",
        "eng": "Jigglypuff",
        "number": 39,
        "emoji": "🎤",
        "good_mbti": "ESFP",
        "bad_mbti": "INTJ",
        "good_reason": "사람들 앞에서 매력을 뽐내는 분위기 메이커와 잘 맞아요.",
        "bad_reason": "푸린은 관심과 리액션을 좋아해서 너무 냉정하고 분석적인 성향과는 서운함이 생길 수 있어요."
    },
    {
        "name": "고라파덕",
        "eng": "Psyduck",
        "number": 54,
        "emoji": "🤯",
        "good_mbti": "INTP",
        "bad_mbti": "ESTJ",
        "good_reason": "엉뚱하지만 생각이 많은 탐구형 성향과 귀엽게 어울려요.",
        "bad_reason": "고라파덕의 느긋하고 엉뚱한 모습이 계획과 효율을 중시하는 성향에게는 답답하게 느껴질 수 있어요."
    },
    {
        "name": "나옹",
        "eng": "Meowth",
        "number": 52,
        "emoji": "🐱",
        "good_mbti": "ENTP",
        "bad_mbti": "ISTJ",
        "good_reason": "재치 있고 장난기 많은 성향과 케미가 좋아요.",
        "bad_reason": "나옹의 즉흥적이고 능청스러운 태도가 규칙과 원칙을 중요하게 생각하는 성향과는 잘 안 맞을 수 있어요."
    },
    {
        "name": "토게피",
        "eng": "Togepi",
        "number": 175,
        "emoji": "🥚",
        "good_mbti": "ENFP",
        "bad_mbti": "ENTJ",
        "good_reason": "밝고 사랑스러운 에너지가 잘 통하는 조합이에요.",
        "bad_reason": "토게피는 순수하고 느긋한 분위기라 목표 중심적이고 빠른 결정을 좋아하는 성향과는 템포가 다를 수 있어요."
    },
    {
        "name": "마릴",
        "eng": "Marill",
        "number": 183,
        "emoji": "🫧",
        "good_mbti": "ISFP",
        "bad_mbti": "ENTJ",
        "good_reason": "부드럽고 감성적인 분위기가 잘 어울려요.",
        "bad_reason": "마릴은 감성적이고 여유로운 친구라 강한 추진력과 효율을 중시하는 성향과는 조금 어색할 수 있어요."
    },
    {
        "name": "치코리타",
        "eng": "Chikorita",
        "number": 152,
        "emoji": "🍃",
        "good_mbti": "INFP",
        "bad_mbti": "ESTJ",
        "good_reason": "순수하고 따뜻한 마음을 가진 성향과 잘 맞아요.",
        "bad_reason": "치코리타는 섬세하고 감정 표현이 중요한 타입이라 지나치게 현실적이고 직설적인 성향과는 상처받을 수 있어요."
    },
    {
        "name": "브케인",
        "eng": "Cyndaquil",
        "number": 155,
        "emoji": "🌋",
        "good_mbti": "ISTP",
        "bad_mbti": "ENFJ",
        "good_reason": "조용하지만 필요할 때 강한 힘을 내는 모습이 닮았어요.",
        "bad_reason": "브케인은 혼자만의 시간이 필요한 편이라 계속 감정을 나누고 이끌어주려는 성향과는 부담을 느낄 수 있어요."
    },
]

# =========================
# 함수
# =========================
def get_pokemon_image(number):
    return f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{number}.png"


@st.cache_data
def get_pokemon_type(pokemon_name):
    try:
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            data = response.json()
            types = [t["type"]["name"] for t in data["types"]]
            return types
        else:
            return []
    except:
        return []


def type_to_korean(type_name):
    type_dict = {
        "normal": "노말",
        "fire": "불꽃",
        "water": "물",
        "electric": "전기",
        "grass": "풀",
        "ice": "얼음",
        "fighting": "격투",
        "poison": "독",
        "ground": "땅",
        "flying": "비행",
        "psychic": "에스퍼",
        "bug": "벌레",
        "rock": "바위",
        "ghost": "고스트",
        "dragon": "드래곤",
        "dark": "악",
        "steel": "강철",
        "fairy": "페어리"
    }
    return type_dict.get(type_name, type_name)


def type_to_emoji(type_name):
    emoji_dict = {
        "normal": "⭐",
        "fire": "🔥",
        "water": "💧",
        "electric": "⚡",
        "grass": "🌿",
        "ice": "❄️",
        "fighting": "🥊",
        "poison": "☠️",
        "ground": "⛰️",
        "flying": "🪽",
        "psychic": "🔮",
        "bug": "🐛",
        "rock": "🪨",
        "ghost": "👻",
        "dragon": "🐉",
        "dark": "🌑",
        "steel": "⚙️",
        "fairy": "🧚"
    }
    return emoji_dict.get(type_name, "✨")


# =========================
# 화면 구성
# =========================
st.markdown('<div class="main-title">✨ MBTI 포켓몬 추천소 ✨</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">내 MBTI를 고르면 나와 찰떡인 포켓몬을 찾아드려요! 🐾</div>',
    unsafe_allow_html=True
)

st.divider()

with st.sidebar:
    st.header("🎒 사용 방법")
    st.write("1. 자신의 MBTI를 선택해요.")
    st.write("2. 추천 버튼을 눌러요.")
    st.write("3. 나와 어울리는 포켓몬을 확인해요.")
    st.write("4. 보너스 친구 포켓몬의 잘 맞는 MBTI와 잘 맞지 않는 MBTI도 확인해요! 🎁")
    st.write("")
    st.info("이 앱은 재미용 추천 앱이에요. MBTI 결과가 절대적인 성격 판단은 아니에요! 😊")

    st.divider()
    st.write("🌈 만든 사람")
    st.write("당곡고등학교 Streamlit 프로젝트")

mbti_list = list(pokemon_data.keys())

selected_mbti = st.selectbox(
    "너의 MBTI를 선택해줘! 🔍",
    mbti_list,
    index=0
)

recommend_button = st.button("나의 포켓몬 찾기! 🎁", use_container_width=True)

# =========================
# 추천 결과
# =========================
if recommend_button:
    data = pokemon_data[selected_mbti]

    pokemon_name = data["pokemon"]
    korean_name = data["korean"]
    pokemon_number = data["number"]
    pokemon_emoji = data["emoji"]

    image_url = get_pokemon_image(pokemon_number)
    types = get_pokemon_type(pokemon_name)

    st.balloons()

    st.success("🎉 당신의 찰떡 포켓몬을 찾았어요!")

    st.markdown(
        f"""
        <div class="pokemon-card">
            <div class="mbti-badge">{selected_mbti}</div>
            <div class="pokemon-name">{pokemon_emoji} {korean_name} {pokemon_emoji}</div>
            <h3>{data["title"]}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.image(image_url, width=280)

    if types:
        type_text = " ".join(
            [f"{type_to_emoji(t)} {type_to_korean(t)}" for t in types]
        )
        st.markdown(f"### 타입: {type_text}")

    tag_html = ""
    for tag in data["tags"]:
        tag_html += f'<span class="tag">#{tag}</span>'

    st.markdown(tag_html, unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="reason-box">
        <b>💌 추천 이유</b><br><br>
        {data["reason"]}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.subheader("📊 나와 포켓몬의 찰떡궁합 지수")

    score = random.randint(85, 99)
    st.progress(score)
    st.write(f"💖 궁합 점수: **{score}점**")

    if score >= 95:
        st.write("🌟 완전 운명적인 조합이에요!")
    elif score >= 90:
        st.write("✨ 아주 잘 어울리는 조합이에요!")
    else:
        st.write("🍀 은근히 매력적인 조합이에요!")

    st.divider()

    # =========================
    # 보너스 친구 포켓몬 추천
    # =========================
    st.subheader("🎁 보너스 친구 포켓몬 추천")
    st.caption("잘 맞는 MBTI와 잘 맞지 않는 MBTI를 함께 알려드려요! 단, 재미용이에요 😊")

    random_bonus = random.sample(bonus_pokemon, 3)
    cols = st.columns(3)

    for col, bonus in zip(cols, random_bonus):
        with col:
            st.markdown('<div class="small-card">', unsafe_allow_html=True)

            st.image(get_pokemon_image(bonus["number"]), width=120)

            st.write(f"### {bonus['emoji']} {bonus['name']}")
            st.caption(f"No. {bonus['number']}")

            st.markdown(
                f"""
                <div class="friend-mbti">
                💖 잘 맞는 MBTI: {bonus["good_mbti"]}
                </div>
                """,
                unsafe_allow_html=True
            )

            st.write(f"💬 {bonus['good_reason']}")

            st.markdown(
                f"""
                <div class="bad-mbti">
                💔 잘 맞지 않는 MBTI: {bonus["bad_mbti"]}
                </div>
                """,
                unsafe_allow_html=True
            )

            st.write(f"🌀 {bonus['bad_reason']}")

            st.markdown('</div>', unsafe_allow_html=True)

else:
    st.info("MBTI를 선택하고 버튼을 눌러보세요! 귀여운 포켓몬이 기다리고 있어요 🐥")

    st.image(
        "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/25.png",
        width=220
    )

st.markdown(
    """
    <div class="footer">
    Made with Streamlit 💻 | Pokemon data from PokeAPI 🎮 | 재미용 MBTI 추천 앱입니다 ✨
    </div>
    """,
    unsafe_allow_html=True
)
