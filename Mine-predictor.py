import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Prédicteur de Mines", layout="centered")
st.title("🧠 Prédicteur de Mines")

if "history" not in st.session_state:
    st.session_state.history = [
        [0, 5, 20], [4, 24], [4, 24], [4], [3, 13], [9, 14, 24], [20, 24], [4, 9, 24],
        [6, 21], [13, 24], [3, 13], [4, 9, 24], [9, 14], [4, 9, 24], [9, 14], [4, 24],
        [6, 13], [9], [13], [13], [], [], []
    ]

def compute_probabilities(history):
    freq = np.zeros(25)
    for game in history:
        for pos in game:
            freq[pos] += 1
    prob_map = freq / len(history)
    return prob_map.reshape((5, 5))

def suggest_safe_moves(prob_grid, top_n=5):
    flat_probs = prob_grid.flatten()
    sorted_indices = np.argsort(flat_probs)
    return [(idx, flat_probs[idx]) for idx in sorted_indices[:top_n]]

st.subheader("➕ Ajouter une nouvelle grille de mines")
new_input = st.text_input("Entrer les positions des mines (séparées par des virgules, ex: 3,7,14)")
if st.button("Ajouter à l'historique"):
    try:
        new_positions = [int(x.strip()) for x in new_input.split(",") if x.strip().isdigit() and 0 <= int(x.strip()) <= 24]
        st.session_state.history.append(new_positions)
        st.success("Nouvelle grille ajoutée !")
    except Exception as e:
        st.error("Entrée invalide. Entrez des nombres entre 0 et 24 séparés par des virgules.")

prob_grid = compute_probabilities(st.session_state.history)
safe_moves = suggest_safe_moves(prob_grid, top_n=5)

st.subheader("🧊 Carte de chaleur des mines")
fig, ax = plt.subplots(figsize=(5, 5))
cax = ax.imshow(prob_grid, cmap='hot', interpolation='nearest')
fig.colorbar(cax, label='Probabilité relative de mine')
ax.set_xticks(range(5))
ax.set_yticks(range(5))
ax.set_title("Grille 5x5 - Risque de mines")

for i in range(5):
    for j in range(5):
        ax.text(j, i, f"{prob_grid[i][j]:.2f}", ha='center', va='center', color='white')

st.pyplot(fig)

st.subheader("✅ Suggestions de cases sûres")
for idx, prob in safe_moves:
    x, y = idx % 5, idx // 5
    st.write(f"Case ({x}, {y}) [index {idx}] - Risque estimé : {prob:.2f}")
