""" ui/css.py

    # Contains global CSS styles for the Panel app, 
    # including color palette, typography, and 
    # custom component styles

"""

GLOBAL_THEME_CSS = """
:root {
    /* 1. YOUR CUSTOM COLOR PALETTE */
    --app-primary-color: #1E293B;      /* Main dark slate */
    --app-secondary-color: #0F172A;    /* Deep accent tone */
    --app-surface-color: #111827;      /* App surface */
    --app-panel-color: #0B1220;        /* Main background */
    --app-button-color: #1F2937;       /* Dark button base */
    --app-button-hover-color: #334155; /* Darker hover state */
    --app-on-primary-color: #ffffff;   /* Text color on primary background */
    --app-on-secondary-color: #000000; /* Text color on secondary background */
    --app-on-surface-color: #f59e0b;   /* Default text color */

    /* 2. MAP YOUR PALETTE TO FAST THEME VARIABLES */
    --accent-color: var(--app-primary-color);
    --neutral-color: #7f7f7f; /* A neutral gray for the FAST system to build on */

    /* 3. TYPOGRAPHY */
    --body-font: "Montserrat", "Helvetica Neue", "Arial", sans-serif;
    --type-ramp-base-font-size: 1.25rem; /* 20px */

    /* 4. SHAPE */
    --control-corner-radius: 3px; 
}

"""

BUTTON_CSS = """
:host {
}

button,
:host button,
:host(.big-button) button {
    background: var(--app-button-color) !important;
    border: none !important;
    border-radius: 3px !important;
    color: var(--app-on-surface-color) !important;
    box-shadow: none !important;
}

button:hover,
:host button:hover,
:host(.big-button) button:hover {
    background: var(--app-button-hover-color) !important;
    border: none !important;
}
"""

APP_LAYOUT_CSS = """
html, body {
    width: 100%;
    height: 100%;
    margin: 0;
    overflow: hidden;
    background: radial-gradient(circle at top, #111827 0%, #060B15 55%, #02040A 100%);
}

.bk-root {
    width: 100%;
    height: 100%;
}

.app-shell {
    width: 100vw;
    height: 100vh;
    margin: 0;
    padding: 0;
    gap: 0;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    background: transparent;
}

.app-shell > .bk {
    flex: 1 1 auto;
    min-height: 0;
}

.app-controls {
    width: 100%;
    height: auto;
    flex: 0 0 auto;
    padding: 16px 24px 16px 24px;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 24px;
    color: var(--app-on-surface-color);
}

.app-controls > .bk {
    flex: 0 0 auto;
    min-width: 0;
}

.app-viewer {
    width: 100%;
    height: 100%;
    flex: 1 1 auto;
    min-height: 0;
    min-width: 0;
    padding: 10px 16px 16px 16px;
    background: linear-gradient(180deg, rgba(17, 24, 39, 0.92), rgba(8, 12, 22, 0.96));
    border: none;
    border-radius: 18px;
    overflow: hidden;
}
"""


CUSTOM_SELECT_CSS = """
:host {
}

:host .bk-input,
:host .bk-input-group,
:host select,
:host input {
    background: var(--app-button-color) !important;
    color: var(--app-on-surface-color) !important;
    border: none !important;
    border-radius: 3px !important;
    box-shadow: none !important;
}

:host .bk-input:hover,
:host .bk-input-group:hover,
:host select:hover,
:host input:hover {
    background: var(--app-button-hover-color) !important;
    border: none !important;
}

:host .bk-input::placeholder,
:host input::placeholder {
    color: rgba(245, 158, 11, 0.7) !important;
}

:host .bk-menu,
:host .bk-listbox,
:host .bk-popover,
:host .bk-tooltip {
    background: var(--app-surface-color) !important;
    color: var(--app-on-surface-color) !important;
    border: none !important;
    border-radius: 3px !important;
}

:host .bk-input-group label,
:host .bk-widget-label,
:host label,
:host .bk-input-group > div,
:host .bk-input-group .bk-input-group-text {
    color: var(--app-on-surface-color) !important;
}
"""

CUSTOM_SLIDER_CSS = """
:host {
}

:host .bk-slider,
:host .noUi-target,
:host .noUi-base,
:host .noUi-connects,
:host .noUi-connect,
:host .noUi-origin,
:host .noUi-handle {
    border: none !important;
    box-shadow: none !important;
}

:host .bk-slider,
:host .noUi-target {
    background: var(--app-button-color) !important;
    border-radius: 3px !important;
}

:host .noUi-connect {
    background: var(--app-button-hover-color) !important;
}

:host .noUi-handle {
    background: var(--app-on-surface-color) !important;
    border-radius: 3px !important;
}

:host .bk-input,
:host input {
    color: var(--app-on-surface-color) !important;
}

:host .bk-input-group label,
:host .bk-widget-label,
:host label,
:host .bk-slider-title,
:host .bk-slider-value {
    color: var(--app-on-surface-color) !important;
}
"""
