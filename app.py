import streamlit as st

# Configuración de la página
st.set_page_config(page_title="Blackjack Pro Analyzer", page_icon="🃏", layout="centered")

# Estilos visuales
st.markdown("""
    <style>
    .stButton button { width: 100%; border-radius: 8px; font-weight: bold; height: 3em; }
    div[data-testid="stMetricValue"] { font-size: 24px; }
    </style>
""", unsafe_allow_html=True)

# Inicialización de la memoria del sistema
if 'running_count' not in st.session_state: st.session_state.running_count = 0
if 'decks_used' not in st.session_state: st.session_state.decks_used = 0
if 'cards_dealt' not in st.session_state: st.session_state.cards_dealt = 0

def update_count(card_val):
    """Actualiza el conteo Hi-Lo y el número de cartas jugadas."""
    if card_val in ['2', '3', '4', '5', '6']: 
        st.session_state.running_count += 1
    elif card_val in ['10', 'J', 'Q', 'K', 'A']: 
        st.session_state.running_count -= 1
    
    st.session_state.cards_dealt += 1
    st.session_state.decks_used = st.session_state.cards_dealt / 52

def get_recommendation(p1, p2, dealer):
    """Matriz completa y minuciosa de Estrategia Básica Perfecta."""
    val = lambda c: 11 if c == 'A' else (10 if c in ['J', 'Q', 'K', '10'] else int(c))
    v1, v2, d = val(p1), val(p2), val(dealer)
    total = v1 + v2
    is_soft = (p1 == 'A' or p2 == 'A')

    # 1. Lógica de Parejas (Splits)
    if p1 == p2:
        if p1 in ['A', '8']: return "SPLIT (Dividir)"
        if p1 in ['10', 'J', 'Q', 'K'] or v1 == 10: return "STAND (Plantarse)"
        if p1 == '9': 
            return "STAND (Plantarse)" if d in [7, 10, 11] else "SPLIT (Dividir)"
        if p1 == '7': 
            return "SPLIT (Dividir)" if d <= 7 else "HIT (Pedir)"
        if p1 == '6': 
            return "SPLIT (Dividir)" if d <= 6 else "HIT (Pedir)"
        if p1 == '5': 
            return "DOUBLE (Doblar)" if d <= 9 else "HIT (Pedir)"
        if p1 == '4': 
            return "SPLIT (Dividir)" if d in [5, 6] else "HIT (Pedir)"
        if p1 in ['2', '3']: 
            return "SPLIT (Dividir)" if d <= 7 else "HIT (Pedir)"

    # 2. Lógica de Manos Blandas (Soft Totals - Con un As)
    if is_soft and p1 != p2:
        other = v2 if p1 == 'A' else v1
        if other >= 8: 
            return "STAND (Plantarse)"
        if other == 7: 
            if d in [3, 4, 5, 6]: return "DOUBLE (Doblar)"
            if d in [2, 7, 8]: return "STAND (Plantarse)"
            return "HIT (Pedir)"
        if other == 6: 
            return "DOUBLE (Doblar)" if d in [3, 4, 5, 6] else "HIT (Pedir)"
        if other in [4, 5]: 
            return "DOUBLE (Doblar)" if d in [4, 5, 6] else "HIT (Pedir)"
        if other in [2, 3]: 
            return "DOUBLE (Doblar)" if d in [5, 6] else "HIT (Pedir)"

    # 3. Lógica de Manos Duras (Hard Totals)
    if not is_soft and p1 != p2:
        if total >= 17: 
            return "STAND (Plantarse)"
        if total >= 13 and total <= 16: 
            return "STAND (Plantarse)" if d <= 6 else "HIT (Pedir)"
        if total == 12: 
            return "STAND (Plantarse)" if d in [4, 5, 6] else "HIT (Pedir)"
        if total == 11: 
            return "DOUBLE (Doblar)"
        if total == 10: 
            return "DOUBLE (Doblar)" if d <= 9 else "HIT (Pedir)"
        if total == 9: 
            return "DOUBLE (Doblar)" if d in [3, 4, 5, 6] else "HIT (Pedir)"
        if total <= 8: 
            return "HIT (Pedir)"
            
    return "HIT (Pedir)"

# --- INTERFAZ GRÁFICA ---

st.title("🃏 Blackjack Pro Analyzer")

# Panel de Registro
st.subheader("1. Registrar Cartas de la Mesa")
cols = st.columns(4)
cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
for i, c in enumerate(cards):
    if cols[i % 4].button(c, key=f"btn_{c}"):
        update_count(c)
        st.rerun()

# Métricas Matemáticas
c1, c2 = st.columns(2)
c1.metric("Running Count (Hi-Lo)", st.session_state.running_count)

# Cálculo de True Count basado en 6 mazos estándar
decks_remaining = max(1.0, 6.0 - st.session_state.decks_used)
true_count = st.session_state.running_count / decks_remaining
c2.metric("True Count", round(true_count, 1))

if st.button("🔄 Reiniciar Zapato (6 Mazos)"):
    st.session_state.running_count = 0
    st.session_state.cards_dealt = 0
    st.session_state.decks_used = 0
    st.rerun()

st.divider()

# Motor de Decisiones
st.subheader("2. Analizador de Decisiones")
p1 = st.selectbox("Tu 1ª Carta", cards, key="p1")
p2 = st.selectbox("Tu 2ª Carta", cards, key="p2")
dealer = st.selectbox("Carta Visible del Crupier", cards, key="d")

rec = get_recommendation(p1, p2, dealer)
st.success(f"🔥 JUGADA MATEMÁTICAMENTE PERFECTA: {rec}")
