
import tkinter as tk
from tkinter import font as tkfont
import random
import os
import math

# ═══════════════════════════════════════════════════════════════════
# CONSTANTES
# ═══════════════════════════════════════════════════════════════════

ROWS, COLS = 6, 5
TILE_SIZE  = 64
TILE_GAP   = 6
WIN_W      = 460

C = {
    "bg":        "#07090d",
    "surface":   "#0d1117",
    "panel":     "#0f1822",
    "border":    "#1a2a3a",
    "border_hi": "#2a4060",
    "correct":   "#00e87a",
    "present":   "#f5c518",
    "absent_bg": "#2a3a4a",
    "absent_br": "#3a5068",
    "text":      "#d8eaf8",
    "dim":       "#3d5a7a",
    "accent":    "#00aaff",
    "accent2":   "#005588",
    "win":       "#00e87a",
    "lose":      "#ff3d5a",
    "key_bg":    "#111e2a",
    "key_bor":   "#1e3045",
}

KEYBOARD_ROWS = [
    list("QWERTYUIOP"),
    list("ASDFGHJKL"),
    ["ENT"] + list("ZXCVBNM") + ["DEL"],
]

STATE_FILL    = {"correct": "#00e87a", "present": "#f5c518", "absent": "#2a3a4a"}
STATE_OUTLINE = {"correct": "#00ff88", "present": "#ffd700", "absent": "#3a5068"}
STATE_TEXT    = {"correct": "#07090d", "present": "#07090d", "absent": "#d8eaf8"}
STATE_PRIO    = {"correct": 3, "present": 2, "absent": 1}

WIN_MESSAGES  = ["Incrível!! 🔥", "Excelente! ✨", "Muito bem! 👏",
                 "Boa! 😎", "Ufa... 😅", "Na última! 😤"]

# ═══════════════════════════════════════════════════════════════════
# CARREGAR PALAVRAS
# ═══════════════════════════════════════════════════════════════════

FALLBACK = [
    "CAMPO","TEMPO","CARRO","PORTA","MUNDO","TERRA","FORTE","BRAVO","CERTO","FUNDO",
    "GENTE","HEROI","JUNTO","LARGO","NOBRE","ORDEM","PERTO","RAPAZ","SALVO","TARDE",
    "VERDE","PRAIA","LIVRO","AMIGO","BOLSA","CARTA","DENTE","FESTA","GRAVE","HUMOR",
    "PEDRA","SABIO","TIGRE","VALOR","CHAVE","DUPLO","HOTEL","JOGAR","MARTE","NEVOA",
    "PAGAR","QUERO","SUAVE","TOUCA","VIRAR","ABRIR","BRISA","CALMA","DENSO","FALSO",
    "GORDO","ISCAR","JURAR","LENTO","OLHAR","PARAR","QUASE","RASGO","SORTE","CLARO",
    "RISCO","PLANO","CRIME","DISCO","CORAL","CORDA","CORES","CORPO","CORTE","COSTA",
]

def carregar_palavras() -> list[str]:
    try:
        caminho = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lista_palavras.txt")
        with open(caminho, "r", encoding="utf-8") as f:
            palavras = [p.strip().upper() for p in f if len(p.strip()) == 5 and p.strip().isalpha()]
        return palavras if palavras else FALLBACK
    except FileNotFoundError:
        return FALLBACK

# ═══════════════════════════════════════════════════════════════════
# APLICAÇÃO PRINCIPAL
# ═══════════════════════════════════════════════════════════════════

class Termo(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Termo")
        self.resizable(False, False)
        self.configure(bg=C["bg"])

        self.palavras = carregar_palavras()

        # Estado do jogo
        self.resposta:  str       = ""
        self.row:       int       = 0
        self.col:       int       = 0
        self.entrada:   list[str] = []
        self.jogando:   bool      = False
        self.key_state: dict      = {}   # letra → "correct" | "present" | "absent"

        # Referências de widgets
        self.tiles:     list[list[dict]] = []
        self.key_items: dict             = {}   # letra → {canvas, rect, txt}

        self._setup_fonts()
        self._build_ui()
        self._centralizar()
        self._iniciar_pulse()

    # ── Fontes ───────────────────────────────────────────────────────────────

    def _setup_fonts(self):
        self.f_title  = tkfont.Font(family="Courier", size=26, weight="bold")
        self.f_tile   = tkfont.Font(family="Courier", size=22, weight="bold")
        self.f_key    = tkfont.Font(family="Courier", size=10, weight="bold")
        self.f_status = tkfont.Font(family="Courier", size=10)
        self.f_sub    = tkfont.Font(family="Courier", size=8)
        self.f_btn    = tkfont.Font(family="Courier", size=12, weight="bold")

    # ── Construção da UI ─────────────────────────────────────────────────────

    def _build_ui(self):
        self._build_header()
        self._build_grid()
        self._build_status()
        self._build_attempts_bar()
        self._build_key_hint()
        self._build_button()

    def _build_header(self):
        self.hdr = tk.Canvas(self, bg=C["bg"], highlightthickness=0,
                             width=WIN_W, height=82)
        self.hdr.pack()

        # Linha de topo colorida
        self.hdr.create_rectangle(WIN_W//2 - 60, 2, WIN_W//2 + 60, 4,
                                   fill=C["accent"], outline="")
        self.hdr.create_line(0, 6, WIN_W, 6, fill=C["border_hi"], width=1)

        # Scanlines decorativas
        for y in range(8, 82, 4):
            self.hdr.create_line(0, y, WIN_W, y, fill="#0a1520", width=1)

        # Cantos
        for x, anc in ((14, "w"), (WIN_W - 14, "e")):
            self.hdr.create_text(x, 40, text="◈",
                                 fill=C["border_hi"], font=self.f_sub, anchor=anc)

        # Título SEM pontos
        self.hdr_title = self.hdr.create_text(
            WIN_W // 2, 38,
            text="TERMO",
            fill=C["accent"],
            font=self.f_title,
        )

        # Subtítulo
        self.hdr.create_text(
            WIN_W // 2, 62,
            text="adivinhe a palavra de 5 letras",
            fill=C["dim"],
            font=self.f_sub,
        )

        # Linha de rodapé do header
        self.hdr.create_line(0, 78, WIN_W, 78, fill=C["border_hi"], width=1)

    def _build_grid(self):
        gw = COLS * TILE_SIZE + (COLS - 1) * TILE_GAP
        gh = ROWS * TILE_SIZE + (ROWS - 1) * TILE_GAP

        self.gc = tk.Canvas(self, width=gw, height=gh,
                             bg=C["bg"], highlightthickness=0)
        self.gc.pack(pady=14)

        self.tiles = []
        for r in range(ROWS):
            row_tiles = []
            for c in range(COLS):
                x = c * (TILE_SIZE + TILE_GAP)
                y = r * (TILE_SIZE + TILE_GAP)

                rect = self.gc.create_rectangle(
                    x, y, x + TILE_SIZE, y + TILE_SIZE,
                    fill=C["surface"], outline=C["border"], width=2
                )
                # Cantos decorativos
                tl = self.gc.create_line(x, y, x + 10, y,
                                          fill=C["border_hi"], width=1)
                lt = self.gc.create_line(x, y, x, y + 10,
                                          fill=C["border_hi"], width=1)
                txt = self.gc.create_text(
                    x + TILE_SIZE // 2, y + TILE_SIZE // 2,
                    text="", fill=C["text"], font=self.f_tile
                )
                row_tiles.append({"rect": rect, "tl": tl, "lt": lt,
                                   "txt": txt, "x": x, "y": y})
            self.tiles.append(row_tiles)

    def _build_status(self):
        self.lbl_status = tk.Label(
            self, text="pressione iniciar",
            bg=C["bg"], fg=C["dim"], font=self.f_status
        )
        self.lbl_status.pack(pady=(0, 6))

    def _build_attempts_bar(self):
        self.bar = tk.Canvas(self, width=WIN_W, height=28,
                              bg=C["bg"], highlightthickness=0)
        self.bar.pack(pady=(0, 4))
        self._draw_bar(0)

    def _draw_bar(self, used: int):
        self.bar.delete("all")
        seg_w = 42
        total = ROWS * seg_w + (ROWS - 1) * 6
        sx    = (WIN_W - total) // 2
        self.bar.create_text(WIN_W // 2, 6,
                              text=f"tentativas: {used} / {ROWS}",
                              fill=C["dim"], font=self.f_sub)
        for i in range(ROWS):
            x    = sx + i * (seg_w + 6)
            fill = C["accent"] if i < used else C["border"]
            self.bar.create_rectangle(x, 14, x + seg_w, 24,
                                       fill=fill, outline="")

    def _build_key_hint(self):
        self.key_items = {}
        self.lbl_hint = tk.Label(
            self,
            text="⌨  use o teclado  ·  Enter para confirmar  ·  Delete/Backspace para apagar",
            bg=C["bg"], fg=C["dim"], font=self.f_sub
        )
        self.lbl_hint.pack(pady=(0, 8))

    def _build_button(self):
        self.btn_cv = tk.Canvas(self, width=230, height=48,
                                bg=C["bg"], highlightthickness=0, cursor="hand2")
        self.btn_cv.pack(pady=(4, 22))
        self._draw_btn("▶   INICIAR JOGO", hover=False)
        self.btn_cv.bind("<Button-1>", lambda e: self._iniciar())
        self.btn_cv.bind("<Enter>",    lambda e: self._draw_btn(self._btn_label(), hover=True))
        self.btn_cv.bind("<Leave>",    lambda e: self._draw_btn(self._btn_label(), hover=False))

    def _draw_btn(self, label: str, hover: bool = False):
        self.btn_cv.delete("all")
        fill = C["accent2"] if hover else C["panel"]
        self.btn_cv.create_rectangle(1, 1, 229, 47,
                                      fill=fill, outline=C["accent"], width=2)
        self.btn_cv.create_line(8,  4,  8,  44, fill=C["accent2"], width=1)
        self.btn_cv.create_line(222, 4, 222, 44, fill=C["accent2"], width=1)
        self.btn_cv.create_text(115, 24, text=label,
                                 fill=C["accent"], font=self.f_btn)

    def _btn_label(self) -> str:
        return "↺   REINICIAR" if (self.jogando or self.row > 0) else "▶   INICIAR JOGO"

    def _key_outline(self, k: str) -> str:
        return STATE_OUTLINE.get(self.key_state.get(k, ""), C["key_bor"])

    # ═══════════════════════════════════════════════════════════════
    # LÓGICA DO JOGO
    # ═══════════════════════════════════════════════════════════════

    def _iniciar(self):
        self.resposta  = random.choice(self.palavras)
        self.row       = 0
        self.col       = 0
        self.entrada   = []
        self.jogando   = True
        self.key_state = {}

        # Reset tiles
        for row_tiles in self.tiles:
            for t in row_tiles:
                self.gc.itemconfig(t["rect"], fill=C["surface"],
                                    outline=C["border"], width=2)
                self.gc.itemconfig(t["txt"],  text="", fill=C["text"])
                self.gc.coords(t["rect"],
                               t["x"], t["y"],
                               t["x"] + TILE_SIZE, t["y"] + TILE_SIZE)
                self.gc.coords(t["txt"],
                               t["x"] + TILE_SIZE // 2,
                               t["y"] + TILE_SIZE // 2)

        # Reset teclado
        for k, d in self.key_items.items():
            d["canvas"].itemconfig(d["rect"], fill=C["key_bg"], outline=C["key_bor"])
            d["canvas"].itemconfig(d["txt"],  fill=C["text"])

        self._draw_bar(0)
        self._set_status("tentativa 1 de 6", C["dim"])
        self._draw_btn("↺   REINICIAR")
        self._highlight_row(0)

        self.focus_set()
        self.bind("<Key>", self._on_key)
        self.bind("<Button-1>", lambda e: self.focus_set())

    def _on_key(self, event):
        if not self.jogando:
            return
        sym = event.keysym
        if sym == "Return":
            self._press("ENT")
        elif sym in ("BackSpace", "Delete"):
            self._press("DEL")
        elif len(sym) == 1 and sym.isalpha():
            self._press(sym.upper())

    def _press(self, k: str):
        if not self.jogando:
            return
        if k == "DEL":
            self._apagar()
        elif k == "ENT":
            self._confirmar()
        elif k.isalpha() and self.col < COLS:
            self._digitar(k)

    def _digitar(self, letra: str):
        t = self.tiles[self.row][self.col]
        self.gc.itemconfig(t["rect"], outline=C["accent2"], width=2)
        self.gc.itemconfig(t["txt"],  text=letra, fill=C["text"])
        self._anim_pop(t)
        self.entrada.append(letra)
        self.col += 1

    def _apagar(self):
        if self.col == 0:
            return
        self.col     -= 1
        self.entrada.pop()
        t = self.tiles[self.row][self.col]
        self.gc.itemconfig(t["txt"],  text="")
        self.gc.itemconfig(t["rect"], outline=C["border_hi"], width=2)

    def _confirmar(self):
        if len(self.entrada) != COLS:
            self._anim_shake(self.row)
            self._set_status("⚠  digite 5 letras!", C["present"])
            self.after(1400, lambda: self._set_status(
                f"tentativa {self.row + 1} de {ROWS}", C["dim"]))
            return

        palavra = "".join(self.entrada)
        cores   = self._avaliar(palavra)
        self._revelar(self.row, palavra, cores)

    def _avaliar(self, palavra: str) -> list[str]:
        resultado = ["absent"] * COLS
        resp_list = list(self.resposta)

        for i in range(COLS):
            if palavra[i] == resp_list[i]:
                resultado[i]  = "correct"
                resp_list[i]  = None

        for i in range(COLS):
            if resultado[i] == "correct":
                continue
            if palavra[i] in resp_list:
                resultado[i] = "present"
                resp_list[resp_list.index(palavra[i])] = None

        return resultado

    # ═══════════════════════════════════════════════════════════════
    # ANIMAÇÕES
    # ═══════════════════════════════════════════════════════════════

    def _revelar(self, row: int, palavra: str, cores: list[str]):
        """Flip sequencial coluna a coluna."""
        STEPS = 8

        def flip_col(c: int):
            if c >= COLS:
                self._pos_reveal(row, palavra, cores)
                return

            t   = self.tiles[row][c]
            est = cores[c]
            x, y = t["x"], t["y"]

            def squish(i: int = 0):
                prog = i / STEPS
                mid  = y + TILE_SIZE // 2

                if prog <= 0.5:
                    frac = max(0.02, 1 - prog * 2)
                    nh   = int(TILE_SIZE * frac)
                    ny   = mid - nh // 2
                    self.gc.coords(t["rect"], x, ny, x + TILE_SIZE, ny + nh)
                    self.gc.itemconfig(t["txt"], state="hidden")
                else:
                    frac = (prog - 0.5) * 2
                    nh   = int(TILE_SIZE * frac)
                    ny   = mid - nh // 2
                    self.gc.coords(t["rect"], x, ny, x + TILE_SIZE, ny + nh)
                    self.gc.itemconfig(t["rect"],
                                       fill=STATE_FILL[est],
                                       outline=STATE_OUTLINE[est])
                    self.gc.itemconfig(t["txt"],
                                       state="normal",
                                       fill=STATE_TEXT[est])

                if i < STEPS:
                    self.after(24, lambda: squish(i + 1))
                else:
                    self.gc.coords(t["rect"], x, y, x + TILE_SIZE, y + TILE_SIZE)
                    self.gc.coords(t["txt"],  x + TILE_SIZE // 2, y + TILE_SIZE // 2)
                    self.gc.itemconfig(t["txt"], state="normal", fill=STATE_TEXT[est])
                    self.after(55, lambda: flip_col(c + 1))

            squish()

        flip_col(0)

    def _pos_reveal(self, row: int, palavra: str, cores: list[str]):
        """Chamado após animação: atualiza teclado e verifica fim de jogo."""
        for i, (letra, estado) in enumerate(zip(palavra, cores)):
            prio_nova   = STATE_PRIO[estado]
            prio_atual  = STATE_PRIO.get(self.key_state.get(letra, ""), 0)
            if prio_nova > prio_atual:
                self.key_state[letra] = estado
                d = self.key_items.get(letra)
                if d:
                    d["canvas"].itemconfig(d["rect"],
                                           fill=STATE_FILL[estado],
                                           outline=STATE_OUTLINE[estado])
                    d["canvas"].itemconfig(d["txt"], fill=STATE_TEXT[estado])

        self.row    += 1
        self.col     = 0
        self.entrada = []
        self._draw_bar(self.row)

        if palavra == self.resposta:
            self.jogando = False
            self.unbind("<Key>")
            msg = WIN_MESSAGES[self.row - 1]
            self._set_status(f"{msg}  —  {self.row}/6", C["win"])
            self._anim_celebrate(self.row - 1)
            self._draw_btn("↺   JOGAR NOVAMENTE")
            return

        if self.row == ROWS:
            self.jogando = False
            self.unbind("<Key>")
            self._set_status(f"fim de jogo  ·  era:  {self.resposta}", C["lose"])
            self._draw_btn("↺   REINICIAR")
            return

        self._set_status(f"tentativa {self.row + 1} de {ROWS}", C["dim"])
        self._highlight_row(self.row)

    def _anim_pop(self, t: dict):
        """Tile expande levemente ao digitar."""
        x, y = t["x"], t["y"]
        seq  = [3, 4, 3, 1, 0]

        def step(i: int = 0):
            d = seq[i]
            self.gc.coords(t["rect"],
                           x - d, y - d,
                           x + TILE_SIZE + d, y + TILE_SIZE + d)
            if i < len(seq) - 1:
                self.after(18, lambda: step(i + 1))
            else:
                self.gc.coords(t["rect"], x, y, x + TILE_SIZE, y + TILE_SIZE)

        step()

    def _anim_shake(self, row: int):
        """Linha inteira treme horizontalmente."""
        offsets = [-10, 10, -8, 8, -5, 5, -2, 0]

        def move_row(dx: int):
            for c in range(COLS):
                t = self.tiles[row][c]
                self.gc.move(t["rect"], dx, 0)
                self.gc.move(t["txt"],  dx, 0)

        def step(i: int = 0):
            if i > 0:
                move_row(-offsets[i - 1])
            if i < len(offsets):
                move_row(offsets[i])
                self.after(40, lambda: step(i + 1))

        step()

    def _anim_celebrate(self, row: int):
        """Tiles da linha vencedora saltam em cascata."""
        for c in range(COLS):
            def bounce(c: int = c):
                t    = self.tiles[row][c]
                x, y = t["x"], t["y"]
                seq  = [(0, 0), (-10, 30), (-16, 30), (-10, 30),
                        (0, 30), (4, 20), (0, 20)]
                total = 0
                for dy, pause in seq:
                    def frame(dy=dy, elapsed=total):
                        self.after(elapsed, lambda: (
                            self.gc.coords(t["rect"],
                                           x, y + dy,
                                           x + TILE_SIZE, y + TILE_SIZE + dy),
                            self.gc.coords(t["txt"],
                                           x + TILE_SIZE // 2,
                                           y + TILE_SIZE // 2 + dy)
                        ))
                    frame()
                    total += pause
                # Restaurar posição
                self.after(total + 60, lambda: (
                    self.gc.coords(t["rect"], x, y, x + TILE_SIZE, y + TILE_SIZE),
                    self.gc.coords(t["txt"],  x + TILE_SIZE // 2, y + TILE_SIZE // 2)
                ))
            self.after(c * 85, bounce)

    # ═══════════════════════════════════════════════════════════════
    # UTILITÁRIOS
    # ═══════════════════════════════════════════════════════════════

    def _highlight_row(self, row: int):
        for c in range(COLS):
            self.gc.itemconfig(self.tiles[row][c]["rect"],
                               outline=C["border_hi"], width=2)

    def _set_status(self, msg: str, color: str):
        self.lbl_status.config(text=msg, fg=color)

    def _centralizar(self):
        self.update_idletasks()
        w  = self.winfo_width()
        h  = self.winfo_height()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        self.geometry(f"+{(sw - w) // 2}+{(sh - h) // 2}")

    def _iniciar_pulse(self):
        """Título pulsa suavemente entre azul ciano e branco