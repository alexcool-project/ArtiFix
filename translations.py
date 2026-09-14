    if st.button(t("nav_privacy"), key="privacy_link", use_container_width=True):
        st.session_state.page_attuale = "Privacy Policy"
        st.rerun()

    if st.button(t("nav_cookie"), key="cookie_link", use_container_width=True):
        st.session_state.page_attuale = "Cookie Policy"
        st.rerun()

    # ✅ Pulsante Termini di Servizio (link esterno alla landing page)
    st.markdown(
        f"""
        <a href="https://www.artifix.it/termini.html" target="_blank" style="display:block; text-align:center; background:#f0f2f6; color:#333; padding:8px; border-radius:6px; text-decoration:none; font-weight:600; font-size:13px; margin-top:8px;">
            {t("nav_terms")}
        </a>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <a href="{DONATE_LINK}" target="_blank" style="display:block; text-align:center; background:#f0f2f6; color:#333; padding:8px; border-radius:6px; text-decoration:none; font-weight:600; font-size:13px; margin-top:15px;">
            {t("nav_donate")}
        </a>
        """,
        unsafe_allow_html=True
    )
