/* v1.9: PULSANTI "APRI" / "CHIUDI" AL POSTO DELLE FRECCE */

[data-testid="stSidebarCollapsedControl"] button::before {
    content: "APRI";
    font-size: 12px;
    font-weight: 700;
    color: #1f77b4;
    letter-spacing: 0.5px;
}
[data-testid="stSidebarCollapsedControl"] button svg {
    display: none !important;
}
[data-testid="stSidebarCollapsedControl"] button {
    background-color: #e8f4fd !important;
    border: 1px solid #1f77b4 !important;
    border-radius: 8px !important;
    padding: 8px 14px !important;
}

[data-testid="stSidebarCollapseButton"] button::before,
[data-testid="stSidebarHeader"] button::before {
    content: "CHIUDI";
    font-size: 12px;
    font-weight: 700;
    color: #ffffff;
}
[data-testid="stSidebarCollapseButton"] button svg,
[data-testid="stSidebarHeader"] button svg {
    display: none !important;
}
[data-testid="stSidebarCollapseButton"] button,
[data-testid="stSidebarHeader"] button {
    background-color: #1f77b4 !important;
    border-radius: 8px !important;
    padding: 8px 14px !important;
}
