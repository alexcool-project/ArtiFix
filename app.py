# --- BARRA LATERALE ---
with st.sidebar:
    if LOGO_BASE64:
        st.markdown(f'<div class="sidebar-logo"><img src="data:image/png;base64,{LOGO_BASE64}" alt="ArtiFix Logo"></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="sidebar-logo"><h3 style="color:#1f77b4;margin:0;">🔧 ARTIFIX</h3></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("## Navigazione")
    
    if st.session_state.page_attuale == "Cookie Policy":
        st.session_state.navigation = "Dashboard"
        st.markdown("📍 **Sei nella pagina: Cookie Policy**")
    else:
        page = st.radio("Vai a:", ["Dashboard", "Ripara File", "Viewer 3D", "Converti Formati", "Progetto ArtiFix"], key="navigation", label_visibility="collapsed")
        st.session_state.page_attuale = page
    
    st.markdown("---")
    
    # LINK PURISSIMO, SENZA SFONDO E SENZA BORDO
    st.markdown("""
    <a href="#" style="color: #1f77b4; font-size: 0.9rem; text-decoration: none; display: block; padding-top: 5px;" onclick="parent.postMessage({type: 'streamlit:setComponentValue', value: 'policy'}, '*')">🍪 Consulta la Cookie Policy</a>
    """, unsafe_allow_html=True)
    
    # Il pulsante nascosto che il link "attiva"
    if st.button("Vai a Cookie Policy", key="go_policy", help="Apri la pagina Cookie Policy"):
        st.session_state.page_attuale = "Cookie Policy"
        st.rerun()
    st.markdown('<style>div[data-testid="stButton"] button { display: none; }</style>', unsafe_allow_html=True)
