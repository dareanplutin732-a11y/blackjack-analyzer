import streamlit as st

st.set_page_config(page_title="Blackjack Real-Time Analyzer", page_icon="🃏", layout="centered")

st.markdown("""
    <style>
    .stButton button {
        width: 100%;
        border-radius: 8px;
        font-weight: bold;
        height: 3em;
        background-color: #1e293b;
        color: white;
    }
    div[data-testid="stMetricValue"] {
        font-size: 26px;
        font-weight: bold;
    }
    .decision-box {
        padding: 15px;
        border-radius: 10px;
        background-color: #0f172a;
        border: 2px solid #10b981;
        text-align: center;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# 1. Inicialización de Variables de Estado
if 'running_count' not in st.session_state:
    st.session_state.running_count = 0
if 'cards_dealt' not in st.session_state:
    st.session_state.cards_dealt = 0

total_decks = 6

def update_count(card_val):
    st.session_state.cards_dealt += 1
    if card_val in ['2', '3', '4', '5', '6']:
        st.session_state.running_count += 1
    elif card_val in ['10', 'J', 'Q', 'K', 'A']:
        st.session_state.running_count -= 1

def reset_game():
    st.session_state.running_count = 0
    st.session_state.cards_dealt = 0

def get_card_value(c):
    if c in ['J', 'Q', 'K', '10']: return 10
    if c == 'A': return 11
    return int(c)

def get_perfect_strategy(c1, c2, dealer):
    v1 = get_card_value(c1)
    v2 = get_card_value(c2)
    dv = get_card_value(dealer)
    
    total = v1 + v2
    
    # AISLAMIENTO ESTRICTO DE PAREJAS: Solo entra aquí si son la misma carta
    is_pair = (c1 == c2)
    
    if is_pair:
        if v1 == 11 or v1 == 8: 
            return "🔥 JUGADA MATEMÁTICAMENTE: SPLIT (Dividir)"
        if v1 == 10: 
            return "🟢 JUGADA MATEMÁTICAMENTE: STAND (Plantarse)"
        if v1 == 9: 
            return "🟢 STAND (Plantarse)" if dv in [7, 10, 11] else "🔥 SPLIT (Dividir)"
        if v1 == 7: 
            return "🔥 SPLIT (Dividir)" if dv <= 7 else "🟡 HIT (Pedir)"
        if v1 == 6: 
            return "🔥 SPLIT (Dividir)" if dv in [3, 4, 5, 6] else "🟡 HIT (Pedir)"
        if v1 == 5: 
            return "🔵 DOUBLE (Doblar)" if dv <= 9 else "🟡 HIT (Pedir)"
        if v1 == 4: 
            return "🔥 SPLIT (Dividir)" if dv in [5, 6] else "🟡 HIT (Pedir)"
        if v1 in [2, 3]: 
            return "🔥 SPLIT (Dividir)" if dv in [4, 5, 6, 7] else "🟡 HIT (Pedir)"

    # AISLAMIENTO DE MANOS BLANDAS: Hay un As, pero no son dos Ases (eso se filtró en is_pair)
    is_soft = (c1 == 'A' or c2 == 'A')
    
    if is_soft:
        if total >= 20: return "🟢 JUGADA MATEMÁTICAMENTE: STAND (Plantarse)"
        if total == 19: return "🔵 DOUBLE (Doblar)" if dv == 6 else "🟢 STAND (Plantarse)"
        if total == 18:
            if dv in [2, 3, 4, 5, 6]: return "🔵 DOUBLE (Doblar)"
            if dv in [7, 8]: return "🟢 STAND (Plantarse)"
            return "🟡 HIT (Pedir)"
        if total == 17: return "🔵 DOUBLE (Doblar)" if dv in [3, 4, 5, 6] else "🟡 HIT (Pedir)"
        if total in [15, 16]: return "🔵 DOUBLE (Doblar)" if dv in [4, 5, 6] else "🟡 HIT (Pedir)"
        if total in [13, 14]: return "🔵 DOUBLE (Doblar)" if dv in [5, 6] else "🟡 HIT (Pedir)"

    # LÓGICA FINAL: MANOS DURAS (12 a 21 sin Ases, o Ases convertidos a valor 1)
    if total >= 17: return "🟢 JUGADA MATEMÁTICAMENTE: STAND (Plantarse)"
    if total in [13, 14, 15, 16]: 
        return "🟢 JUGADA MATEMÁTICAMENTE: STAND (Plantarse)" if dv <= 6 else "🟡 HIT (Pedir)"
    if total == 12: 
        return "🟢 JUGADA MATEMÁTICAMENTE: STAND (Plantarse)" if dv in [4, 5, 6] else "🟡 HIT (Pedir)"
    if total == 11: return "🔵 JUGADA MATEMÁTICAMENTE: DOUBLE (Doblar)"
    if total == 10: return "🔵 DOUBLE (Doblar)" if dv <= 9 else "🟡 HIT (Pedir)"
    if total == 9: return "🔵 DOUBLE (Doblar)" if dv in [3, 4, 5, 6] else "🟡 HIT (Pedir)"
    
    return "🟡 JUGADA MATEMÁTICAMENTE: HIT (Pedir)"

st.title("🃏 Blackjack Real-Time Analyzer")

# Interfaz visual de botones estilo columna izquierda
st.subheader("Registrar carta que sale en la mesa:")
cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

cols = st.columns(4)
for i, c in enumerate(cards):
    with cols[i % 4]:
        if st.button(c, key=f"btn_mesa_{c}"):
            update_count(c)
            st.rerun()

st.divider()

# Cálculo de True Count
remaining_decks = max(0.5, total_decks - (st.session_state.cards_dealt / 52))
true_count = round(st.session_state.running_count / remaining_decks, 1)

c1, c2 = st.columns(2)
with c1:
    st.metric("Running Count (Hi-Lo)", st.session_state.running_count)
with c2:
    st.metric("True Count", true_count)

if st.button("🔄 Reiniciar Zapato (6 Mazos)"):
    reset_game()
    st.rerun()

st.divider()

st.subheader("2. Analizador de Decisiones")

c_u1, c_u2, c_d = st.columns(3)
with c_u1:
    u1 = st.selectbox("Tu 1ª Carta", cards, index=0) # Por defecto 2
with c_u2:
    u2 = st.selectbox("Tu 2ª Carta", cards, index=9) # Por defecto J
with c_d:
    dealer = st.selectbox("Carta Visible del Crupier", cards, index=4) # Por defecto 6

decision = get_perfect_strategy(u1, u2, dealer)

st.markdown(f"""
    <div class="decision-box">
        <h3 style="color:#34d399;">{decision}</h3>
    </div>
""", unsafe_allow_html=True)
