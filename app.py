/* ============================================================ */
/* v1.7: SIDEBAR FORZATA APERTA SU MOBILE                       */
/* Su schermi < 768px, la sidebar è sempre visibile             */
/* ============================================================ */
@media (max-width: 768px) {
    [data-testid="stSidebar"] {
        display: block !important;
        transform: translateX(0) !important;
        min-width: 75vw !important;
        max-width: 85vw !important;
        background: #ffffff !important;
        box-shadow: 2px 0 12px rgba(0,0,0,0.15) !important;
        z-index: 999 !important;
    }

    [data-testid="stSidebarCollapseButton"] button,
    [data-testid="stSidebarHeader"] button {
        background-color: #1f77b4 !important;
        color: #ffffff !important;
        border-radius: 8px !important;
        padding: 6px 12px !important;
        font-size: 16px !important;
        box-shadow: 0 2px 6px rgba(31,119,180,0.3) !important;
    }
    [data-testid="stSidebarCollapseButton"] button:hover,
    [data-testid="stSidebarHeader"] button:hover {
        background-color: #155a8a !important;
    }

    [data-testid="stSidebarCollapsedControl"] {
        display: none !important;
    }
}
