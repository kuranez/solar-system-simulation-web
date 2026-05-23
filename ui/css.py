""" ui/css.py

    # Contains global CSS styles for the Panel app, 
    # including color palette, typography, and 
    # custom component styles

"""

GLOBAL_THEME_CSS = """
:root {
    /* 1. YOUR CUSTOM COLOR PALETTE */
    --app-primary-color: #422C71;      /* Your main brand color */
    --app-secondary-color: #ff9800;    /* An accent color */
    --app-surface-color: #2B3036;      /* Background for elements */
    --app-on-primary-color: #ffffff;   /* Text color on primary background */
    --app-on-secondary-color: #000000; /* Text color on secondary background */
    --app-on-surface-color: #f5f5f5;   /* Default text color */

    /* 2. MAP YOUR PALETTE TO FAST THEME VARIABLES */
    --accent-color: var(--app-primary-color);
    --neutral-color: #7f7f7f; /* A neutral gray for the FAST system to build on */

    /* 3. TYPOGRAPHY */
    --body-font: "Montserrat", "Helvetica Neue", "Arial", sans-serif;
    --type-ramp-base-font-size: 1.25rem; /* 20px */

    /* 4. SHAPE */
    --control-corner-radius: 6px; 
}

/* NEW: Add this class for custom button styling */
.big-button {
    /* Increase vertical and horizontal padding */
    padding: 5px 5px;
    
    /* Set a consistent height */
    height: auto;

    /* Set a specific font size for the button text */
    font-size: 1.25rem;
}

"""


CUSTOM_SELECT_CSS = """
:host {
    /* --- Style for the main select box --- */
    --neutral-fill-input-rest: var(--app-surface-color);
    --neutral-foreground-rest: var(--app-on-surface-color);

    /* --- Style for the dropdown menu and its options --- */
    --accent-fill-rest: var(--app-secondary-color);
    --foreground-on-accent-rest: var(--app-on-secondary-color);
}
"""

CUSTOM_SLIDER_CSS = """
:host {
    /* Overriding the accent color just for this slider */
    --accent-color: var(--app-secondary-color);

    /* Color of the slider's thumb/handle */
    --neutral-foreground-rest: var(--app-secondary-color);

    /* Color of the inactive (background) part of the slider track */
    --neutral-fill-stealth-rest: #1E2226; /* A slightly darker grey */
}
"""
