# css.py
# Module to define custom CSS styles for the solar system simulation web app
# v.1.1 - Tweaked CSS for better appearance and consistency
# author: kuranez

CUSTOM_SELECT_CSS = """
:host {
    --bg: #2B3036;
    --text: #f5f5f5;
    --active-bg: #ff9800;
    --active-text: #422C71;
}

/* Main select box */
select {
    background-color: var(--bg);
    color: var(--text);
    border: 1px solid #555;
    border-radius: 6px;
    font-size: 16px;
    text-align: right;
    padding: 6px 30px 6px 6px; /* top, right, bottom, left */
    -webkit-appearance: none;
    -moz-appearance: none;
    appearance: none;
}
}

/* When clicked/focused */
select:focus {
    background-color: var(--active-bg);
    color: var(--active-text);
    outline: none;
    border-color: var(--active-bg);
}

/* Dropdown options */
option {
    background-color: var(--bg);
    color: var(--text);
}

/* Selected option */
option:checked {
    background-color: var(--active-bg);
    color: var(--active-text);
}

/* Hovered option */
option:hover {
    background-color: #444;
    color: white;
}
"""