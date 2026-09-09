# --- POPUP COOKIE (VISIBILE, SEMPLICE E GARANTITO) ---
if st.session_state.cookie_consent is None:
    # Spazio sopra
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    
    # Blocco centrato (semplice, senza CSS)
    with st.container():
        st.markdown("""
        <div style="background: #1a1a24; border: 1px solid rgba(255,255,255,0.1); border-radius: 20px; padding: 30px; max-width: 700px; margin: 0 auto; box-shadow: 0 10px 40px rgba(0,0,0,0.5); color: #e0e0e0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
            <h3 style="color: #6ab0e6; text-align: center; font-size: 20px; margin-bottom: 15px;">🍪 Cookie Policy</h3>
            <p style="font-size: 14px; line-height: 1.8;">
                Questo sito o gli strumenti terzi da questo utilizzati si avvalgono di cookie necessari al funzionamento ed utili alle finalità illustrate nella cookie policy. 
                Se vuoi saperne di più o negare il consenso a tutti o ad alcuni cookie, <a href="#">consulta la cookie policy</a>. 
                Chiudendo questo banner, scorrendo questa pagina, cliccando su un link o proseguendo la navigazione in altra maniera, acconsenti all'uso dei cookie.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Pulsanti nativi Streamlit (funzionano SEMPRE)
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Solo tecnici", key="decline_cookies", use_container_width=True):
                st.session_state.cookie_consent = "declined"
                st.rerun()
        with col2:
            if st.button("Accetta tutti", key="accept_cookies", type="primary", use_container_width=True):
                st.session_state.cookie_consent = "accepted"
                st.rerun()
