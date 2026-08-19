import streamlit as st

st.set_page_config(
    page_title="Blackjack Analyzer",
    page_icon="🃏",
    layout="centered"
)

st.markdown("""
    <style>
    .stButton button {
        width: 100%;
        border-radius: 8px;
        font-weight: bold;
        height: 3em;
    }
    </style>
""", unsafe_allow_html=True)

class MobileBlackjackAnalyzer:
    def __init__(self, num_decks=6):
        self.num_decks = num_decks
        if 'deck' not in st.session_state:
            st.session_state.deck = self._initialize_deck()
        if 'visible_cards' not in st.session_state:
            st.session_state.visible_cards = []

    def _initialize_deck(self):
        values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        single_deck = [{'value': v} for v in values for _ in range(4)]
        return single_deck * self.num_decks

    def reset_shoe(self):
        st.session_state.deck = self._initialize_deck()
        st.session_state.visible_cards = []

    def register_card(self, value):
        for c in st.session_state.deck:
            if c['value'] == value:
                st.session_state.deck.remove(c)
                st.session_state.visible_cards.append(value)
                break

    def calculate_hand_value(self, hand_values):
        total = 0
        aces = 0
        for val in hand_values:
            if val in ['J', 'Q', 'K', '10']:
                total += 10
            elif val == 'A':
                aces += 1
                total += 11
            else:
                total += int(val)
        
        while total > 21 and aces > 0:
            total -= 10
            aces -= 1
        return total

    def bust_probability(self, current_total):
        if current_total >= 21:
            return 100.0 if current_total > 21 else 0.0

        total_cards_left = len(st.session_state.deck)
        if total_cards_left == 0:
            return 0.0

        cards_causing_bust = 0
        for card in st.session_state.deck:
            val = card['value']
            card_val = 10 if val in ['J', 'Q', 'K', '10'] else (11 if val == 'A' else int(val))
            if current_total + card_val > 21:
                cards_causing_bust += 1

        return round((cards_causing_bust / total_cards_left) * 100, 2)

analyzer = MobileBlackjackAnalyzer()

st.title("🃏 Blackjack Real-Time Analyzer")

st.subheader("Registrar carta que sale en la mesa:")
card_options = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

cols = st.columns(4)
for i, card in enumerate(card_options):
    with cols[i % 4]:
        if st.button(card, key=f"btn_{card}_{i}"):
            analyzer.register_card(card)
            st.rerun()

st.markdown("---")

st.write(f"**Cartas registradas en la mesa:** {len(st.session_state.visible_cards)}")
if st.session_state.visible_cards:
    st.write(", ".join(st.session_state.visible_cards))

if st.button("🔄 Reiniciar Zapato (Shoe)"):
    analyzer.reset_shoe()
    st.rerun()

st.markdown("---")

st.subheader("Tu Mano Actual")
col1, col2 = st.columns(2)
with col1:
    card1 = st.selectbox("Carta 1", card_options, index=0)
with col2:
    card2 = st.selectbox("Carta 2", card_options, index=8)

dealer_card = st.selectbox("Carta visible del Crupier", card_options, index=8)

player_total = analyzer.calculate_hand_value([card1, card2])
bust_prob = analyzer.bust_probability(player_total)

st.metric(label="Valor de tu Mano", value=player_total)
st.metric(label="Probabilidad de Pasarte (Bust) si Pides Carta", value=f"{bust_prob}%", delta_color="inverse")
