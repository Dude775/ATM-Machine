# ============================================================
#  STYLES — Dark Premium Banking Theme
# ============================================================

COLORS = {
    # רקעים
    "bg":           "#0f0f0f",    # שחור עמוק
    "bg_light":     "#1a1a1a",    # כרטיסים
    "bg_card":      "#141414",    # פאנל פנימי
    "bg_input":     "#222222",    # שדות קלט
    "bg_hover":     "#2a2a2a",    # hover על שורות

    # טקסט
    "white":        "#f0ece3",    # לבן חם (לא קר)
    "text_light":   "#a09880",    # אפור זהבי — labels
    "text_muted":   "#5a5550",    # טקסט משני

    # אקסנט — זהב
    "gold":         "#c9a84c",    # זהב ראשי
    "gold_dark":    "#a07a2e",    # hover זהב
    "gold_glow":    "#e8c96a",    # highlight בהיר

    # ירוק — הצלחה
    "green":        "#2ecc71",
    "green_dark":   "#27ae60",

    # אדום — שגיאה / מחיקה
    "red":          "#e74c3c",
    "red_dark":     "#c0392b",

    # כחול — היסטוריה / מידע
    "blue":         "#3498db",
    "blue_dark":    "#2980b9",

    # כתום — Pending
    "orange":       "#e67e22",
    "orange_dark":  "#d35400",

    # גבולות
    "border":       "#2c2c2c",
    "border_gold":  "#3d3020",

    # סטטוסים
    "status_active":  "#2ecc71",
    "status_blocked": "#e74c3c",
    "status_pending": "#e67e22",
}

# פונטים
FONT_TITLE      = ("Segoe UI",     22, "bold")
FONT_SUBTITLE   = ("Segoe UI",     13, "normal")
FONT_LABEL      = ("Segoe UI",     10, "normal")
FONT_ENTRY      = ("Consolas",     12, "normal")
FONT_BUTTON     = ("Segoe UI",     10, "bold")
FONT_BUTTON_SM  = ("Segoe UI",      9, "normal")
FONT_MONO       = ("Consolas",     11, "normal")
FONT_SMALL      = ("Segoe UI",      8, "normal")
FONT_TEXT       = ("Segoe UI",     10, "normal")

# עזר לכפתורים
def btn_style(bg, fg=None, font=None):
    return {
        "bg": bg,
        "fg": fg or COLORS["white"],
        "font": font or FONT_BUTTON,
        "relief": "flat",
        "cursor": "hand2",
        "bd": 0,
    }