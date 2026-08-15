import pyautogui
import keyboard
import customtkinter as ctk

# ---------------------------------
# Mouse Coordinate + RGB Finder
# Uses: pyautogui, keyboard, customtkinter
# ---------------------------------

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Mouse RGB & Location")
app.geometry("620x380")
app.resizable(False, False)

locked = False
last_x, last_y = 0, 0
last_rgb = (0, 0, 0)


def copy_value(value):
    app.clipboard_clear()
    app.clipboard_append(str(value))
    app.update()


def copy_location():
    copy_value(f"{last_x}, {last_y}")


def copy_rgb():
    r, g, b = last_rgb
    copy_value(f"{r}, {g}, {b}")


def toggle_lock():
    global locked
    locked = not locked
    update_lock_text()


def update_lock_text():
    if locked:
        lock_label.configure(text="LOCKED  •  Press SPACE to unlock")
    else:
        lock_label.configure(text="LIVE  •  Press SPACE to lock")


def check_keyboard():
    # keyboard module detects SPACE even when the app isn't focused.
    if keyboard.is_pressed("space"):
        # Prevent repeated toggles while the key is held.
        if not getattr(check_keyboard, "space_was_down", False):
            toggle_lock()
            check_keyboard.space_was_down = True
    else:
        check_keyboard.space_was_down = False

    app.after(30, check_keyboard)


def update_values():
    global last_x, last_y, last_rgb

    if not locked:
        last_x, last_y = pyautogui.position()

        try:
            last_rgb = pyautogui.pixel(last_x, last_y)
        except Exception:
            last_rgb = (0, 0, 0)

        location_button.configure(
            text=f"X: {last_x}    Y: {last_y}"
        )

        r, g, b = last_rgb
        rgb_button.configure(
            text=f"R: {r}    G: {g}    B: {b}"
        )

    app.after(30, update_values)


# Main box
box = ctk.CTkFrame(
    app,
    corner_radius=12,
    fg_color="white",
    border_width=2,
    border_color="#333333"
)
box.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.82)

title = ctk.CTkLabel(
    box,
    text="MOUSE COORDINATES & RGB",
    font=("Arial", 20, "bold"),
    text_color="black"
)
title.pack(pady=(20, 12))


location_button = ctk.CTkButton(
    box,
    text="X: 0    Y: 0",
    font=("Arial", 20, "bold"),
    height=65,
    fg_color="black",
    hover_color="#222222",
    text_color="white",
    command=copy_location
)
location_button.pack(fill="x", padx=45, pady=8)


rgb_button = ctk.CTkButton(
    box,
    text="R: 0    G: 0    B: 0",
    font=("Arial", 20, "bold"),
    height=65,
    fg_color="black",
    hover_color="#222222",
    text_color="white",
    command=copy_rgb
)
rgb_button.pack(fill="x", padx=45, pady=8)


lock_label = ctk.CTkLabel(
    box,
    text="LIVE  •  Press SPACE to lock",
    font=("Arial", 12),
    text_color="#555555"
)
lock_label.pack(pady=8)


exit_button = ctk.CTkButton(
    box,
    text="EXIT",
    width=110,
    height=35,
    fg_color="#222222",
    hover_color="#444444",
    command=app.destroy
)
exit_button.pack(pady=3)


update_values()
check_keyboard()
app.mainloop()
