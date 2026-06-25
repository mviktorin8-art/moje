"""
Simple Calculator App
----------------------
A basic desktop calculator built with Python's built-in Tkinter library.
No external dependencies needed — just run it with Python 3.

Usage:
    python calculator.py
"""

import tkinter as tk

# ---------------------------------------------------------------------------
# App window setup
# ---------------------------------------------------------------------------
window = tk.Tk()
window.title("Calculator")
window.resizable(False, False)
window.configure(bg="#2b2b3d")

# Colors (basic, flat design)
COLOR_DISPLAY_BG = "#1e1e2e"
COLOR_DISPLAY_FG = "#ffffff"
COLOR_NUM_BTN = "#3a3d52"
COLOR_NUM_BTN_FG = "#ffffff"
COLOR_OP_BTN = "#ff9f43"
COLOR_OP_BTN_FG = "#1e1e2e"
COLOR_EQUALS_BTN = "#4cd137"
COLOR_EQUALS_BTN_FG = "#1e1e2e"
COLOR_CLEAR_BTN = "#e74c3c"
COLOR_CLEAR_BTN_FG = "#ffffff"

FONT_DISPLAY = ("Consolas", 28)
FONT_BTN = ("Helvetica", 16, "bold")

# ---------------------------------------------------------------------------
# Display
# ---------------------------------------------------------------------------
display_var = tk.StringVar(value="0")

display = tk.Label(
    window,
    textvariable=display_var,
    anchor="e",
    bg=COLOR_DISPLAY_BG,
    fg=COLOR_DISPLAY_FG,
    font=FONT_DISPLAY,
    padx=15,
    pady=25,
)
display.grid(row=0, column=0, columnspan=4, sticky="nsew")

# ---------------------------------------------------------------------------
# Calculator logic
# ---------------------------------------------------------------------------
ALLOWED_CHARS = set("0123456789.+-*/() ")


def is_expression_safe(expression: str) -> bool:
    """Only allow digits, decimal points, parentheses, and basic operators."""
    return all(ch in ALLOWED_CHARS for ch in expression)


def update_display(text: str) -> None:
    display_var.set(text if text else "0")


def on_digit(value: str) -> None:
    current = display_var.get()
    current = "" if current == "0" else current
    update_display(current + value)


def on_operator(op: str) -> None:
    current = display_var.get()
    if current and current[-1] in "+-*/":
        current = current[:-1]  # replace trailing operator instead of stacking
    update_display(current + op)


def on_clear() -> None:
    update_display("0")


def on_backspace() -> None:
    update_display(display_var.get()[:-1])


def on_equals() -> None:
    expression = display_var.get()
    if not is_expression_safe(expression):
        update_display("Error")
        return
    try:
        result = eval(expression)  # safe here: input is pre-filtered above
        update_display(str(result))
    except ZeroDivisionError:
        update_display("Error: ÷0")
    except Exception:
        update_display("Error")


def on_percent() -> None:
    expression = display_var.get()
    if not is_expression_safe(expression):
        update_display("Error")
        return
    try:
        result = eval(expression) / 100
        update_display(str(result))
    except Exception:
        update_display("Error")


def on_sign_toggle() -> None:
    current = display_var.get()
    try:
        value = eval(current) if is_expression_safe(current) else 0
        update_display(str(value * -1))
    except Exception:
        update_display("Error")


# ---------------------------------------------------------------------------
# Buttons layout: (label, row, column, handler, color set)
# ---------------------------------------------------------------------------
buttons = [
    ("C", 1, 0, on_clear, COLOR_CLEAR_BTN, COLOR_CLEAR_BTN_FG),
    ("⌫", 1, 1, on_backspace, COLOR_CLEAR_BTN, COLOR_CLEAR_BTN_FG),
    ("%", 1, 2, on_percent, COLOR_OP_BTN, COLOR_OP_BTN_FG),
    ("/", 1, 3, lambda: on_operator("/"), COLOR_OP_BTN, COLOR_OP_BTN_FG),

    ("7", 2, 0, lambda: on_digit("7"), COLOR_NUM_BTN, COLOR_NUM_BTN_FG),
    ("8", 2, 1, lambda: on_digit("8"), COLOR_NUM_BTN, COLOR_NUM_BTN_FG),
    ("9", 2, 2, lambda: on_digit("9"), COLOR_NUM_BTN, COLOR_NUM_BTN_FG),
    ("*", 2, 3, lambda: on_operator("*"), COLOR_OP_BTN, COLOR_OP_BTN_FG),

    ("4", 3, 0, lambda: on_digit("4"), COLOR_NUM_BTN, COLOR_NUM_BTN_FG),
    ("5", 3, 1, lambda: on_digit("5"), COLOR_NUM_BTN, COLOR_NUM_BTN_FG),
    ("6", 3, 2, lambda: on_digit("6"), COLOR_NUM_BTN, COLOR_NUM_BTN_FG),
    ("-", 3, 3, lambda: on_operator("-"), COLOR_OP_BTN, COLOR_OP_BTN_FG),

    ("1", 4, 0, lambda: on_digit("1"), COLOR_NUM_BTN, COLOR_NUM_BTN_FG),
    ("2", 4, 1, lambda: on_digit("2"), COLOR_NUM_BTN, COLOR_NUM_BTN_FG),
    ("3", 4, 2, lambda: on_digit("3"), COLOR_NUM_BTN, COLOR_NUM_BTN_FG),
    ("+", 4, 3, lambda: on_operator("+"), COLOR_OP_BTN, COLOR_OP_BTN_FG),

    ("±", 5, 0, on_sign_toggle, COLOR_NUM_BTN, COLOR_NUM_BTN_FG),
    ("0", 5, 1, lambda: on_digit("0"), COLOR_NUM_BTN, COLOR_NUM_BTN_FG),
    (".", 5, 2, lambda: on_digit("."), COLOR_NUM_BTN, COLOR_NUM_BTN_FG),
    ("=", 5, 3, on_equals, COLOR_EQUALS_BTN, COLOR_EQUALS_BTN_FG),
]

for (label, row, col, handler, bg_color, fg_color) in buttons:
    btn = tk.Button(
        window,
        text=label,
        command=handler,
        font=FONT_BTN,
        bg=bg_color,
        fg=fg_color,
        activebackground=bg_color,
        relief="flat",
        width=5,
        height=2,
        bd=0,
    )
    btn.grid(row=row, column=col, padx=4, pady=4)

# ---------------------------------------------------------------------------
# Keyboard support
# ---------------------------------------------------------------------------
def on_key_press(event: tk.Event) -> None:
    char = event.char
    if char.isdigit() or char == ".":
        on_digit(char)
    elif char in "+-*/":
        on_operator(char)
    elif event.keysym == "Return":
        on_equals()
    elif event.keysym == "BackSpace":
        on_backspace()
    elif event.keysym.lower() == "escape":
        on_clear()


window.bind("<Key>", on_key_press)

# ---------------------------------------------------------------------------
# Run the app
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    window.mainloop()
