#!/usr/bin/env python3
"""Generate Bienvenida Docentes PDF for Eligiendo Mi Camino."""

from fpdf import FPDF
import os

BASE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(BASE, "img")
FOTOS = os.path.join(BASE, "campus_fotos")

# EMC brand colors (RGB)
CREAM = (253, 227, 177)
YELLOW = (253, 208, 38)
ORANGE = (243, 147, 0)
DEEP_ORANGE = (247, 90, 0)
DARK = (36, 44, 50)
LIGHT_BG = (255, 251, 240)
WHITE = (255, 255, 255)
RED = (198, 40, 40)
GREEN = (46, 125, 50)
BLUE = (21, 101, 192)

PW = 210  # A4 width mm


class BienvenidaPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=20)

    def header_bar(self, title, subtitle="", color=ORANGE):
        self.set_fill_color(*color)
        self.set_text_color(*WHITE)
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 10, title, fill=True, align="C", new_x="LMARGIN", new_y="NEXT")
        if subtitle:
            r, g, b = color
            self.set_fill_color(min(r+30,255), min(g+30,255), min(b+30,255))
            self.set_font("Helvetica", "", 9)
            self.cell(0, 7, subtitle, fill=True, align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_text_color(*DARK)
        self.ln(4)

    def section_title(self, title):
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(*DEEP_ORANGE)
        self.cell(0, 8, title, new_x="LMARGIN", new_y="NEXT")
        y = self.get_y()
        self.set_draw_color(*ORANGE)
        self.set_line_width(0.8)
        self.line(self.l_margin, y, self.l_margin + 40, y)
        self.set_draw_color(0, 0, 0)
        self.set_line_width(0.2)
        self.ln(4)
        self.set_text_color(*DARK)

    def body_text(self, text, bold=False, size=10):
        self.set_font("Helvetica", "B" if bold else "", size)
        self.multi_cell(0, 5.5, text, new_x="LMARGIN", new_y="NEXT")

    def bullet(self, sym, text, sub=""):
        self.set_font("Helvetica", "B", 10)
        x0 = self.get_x()
        self.cell(8, 5.5, sym, new_x="END")
        self.set_font("Helvetica", "", 10)
        self.multi_cell(0, 5.5, text, new_x="LMARGIN", new_y="NEXT")
        if sub:
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(120, 120, 120)
            self.set_x(x0 + 8)
            self.multi_cell(0, 4.5, sub, new_x="LMARGIN", new_y="NEXT")
            self.set_text_color(*DARK)

    def colored_box(self, text, bg=LIGHT_BG, border_color=ORANGE):
        self.set_fill_color(*bg)
        self.set_draw_color(*border_color)
        self.set_line_width(0.5)
        x, y = self.get_x(), self.get_y()
        w = self.w - self.l_margin - self.r_margin
        self.set_font("Helvetica", "", 9)
        lines = self.multi_cell(w - 8, 5, text, dry_run=True, output="LINES")
        h = len(lines) * 5 + 8
        if y + h > self.h - self.b_margin:
            self.add_page()
            y = self.get_y()
        self.rect(x, y, w, h, style="DF")
        self.set_xy(x + 4, y + 4)
        self.multi_cell(w - 8, 5, text, new_x="LMARGIN", new_y="NEXT")
        self.set_y(y + h + 3)
        self.set_draw_color(0, 0, 0)
        self.set_line_width(0.2)

    def add_photo(self, path, caption="", max_w=90):
        if not os.path.exists(path):
            return
        if self.get_y() > self.h - 70:
            self.add_page()
        x = (self.w - max_w) / 2
        try:
            self.image(path, x=x, w=max_w)
        except Exception:
            return
        if caption:
            self.set_font("Helvetica", "I", 7)
            self.set_text_color(120, 120, 120)
            self.cell(0, 4, caption, align="C", new_x="LMARGIN", new_y="NEXT")
            self.set_text_color(*DARK)
        self.ln(3)

    def sched_row(self, cells, widths, bold=False, bg=None, text_color=DARK):
        if bg:
            self.set_fill_color(*bg)
        self.set_text_color(*text_color)
        self.set_font("Helvetica", "B" if bold else "", 8.5)
        old_margin = self.c_margin
        self.c_margin = 2  # more inner padding
        h = 7
        for i, (cell, w) in enumerate(zip(cells, widths)):
            self.cell(w, h, cell, border=1, fill=bg is not None,
                      align="C" if i == 0 else "L", new_x="END")
        self.ln(h)
        self.c_margin = old_margin
        self.set_text_color(*DARK)


def build_pdf():
    pdf = BienvenidaPDF()
    pdf.set_margins(15, 15, 15)
    usable_w = PW - 30  # 180mm

    # ===== PAGE 1: COVER =====
    pdf.add_page()

    # Orange header area
    pdf.set_fill_color(*ORANGE)
    pdf.rect(0, 0, PW, 100, style="F")
    pdf.set_fill_color(*DEEP_ORANGE)
    pdf.rect(0, 85, PW, 15, style="F")

    # Mascot
    mascot = os.path.join(IMG, "brand_p4_0.jpeg")
    if os.path.exists(mascot):
        pdf.image(mascot, x=80, y=8, w=50)

    pdf.set_y(62)
    pdf.set_text_color(*WHITE)
    pdf.set_font("Helvetica", "B", 8)
    pdf.cell(0, 5, "FORMACION DOCENTE 2026", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "B", 22)
    pdf.cell(0, 12, "Bienvenido/a", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 6, "Eligiendo Mi Camino", align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.set_text_color(*DARK)
    pdf.set_y(108)

    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(0, 5.5,
        "Un programa innovador de la DRELM y el Banco Mundial, implementado junto "
        "a la UPC, que busca fortalecer las capacidades de los docentes para guiar a "
        "los estudiantes de 5to de secundaria en sus decisiones vocacionales y mejorar "
        "su aprendizaje de matematicas con herramientas de inteligencia artificial.",
        align="C", new_x="LMARGIN", new_y="NEXT"
    )
    pdf.ln(5)

    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(*ORANGE)
    pdf.cell(0, 6, "DRELM  |  Banco Mundial  |  UPC  |  uDocz", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(*DARK)
    pdf.ln(3)

    # WB link
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(0, 5, "Mas informacion del programa:", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(*BLUE)
    pdf.set_font("Helvetica", "U", 9)
    wb_link = "https://www.bancomundial.org/es/country/peru/brief/eligiendo-mi-camino"
    pdf.cell(0, 5, wb_link, align="C", link=wb_link, new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(*DARK)
    pdf.ln(3)

    # Video link
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(0, 6, "Video de Bienvenida", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(0, 5, "Jaime Saavedra, Director de Desarrollo Humano para America Latina, Banco Mundial", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(*BLUE)
    pdf.set_font("Helvetica", "U", 8)
    vid_link = "https://drive.google.com/file/d/1epEU4vQEa4nxbwcHkuKG1mz8KBtSpIfe/view"
    pdf.cell(0, 5, "Ver video de bienvenida", align="C", link=vid_link, new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(*DARK)
    pdf.ln(6)

    # Welcome app link - prominent box (super communicator style)
    app_link = "https://ezequielmolina-lang.github.io/bienvenida-docentes/"
    pdf.set_fill_color(*CREAM)
    pdf.set_draw_color(*ORANGE)
    pdf.set_line_width(0.8)
    x, y = pdf.get_x(), pdf.get_y()
    w_box = pdf.w - pdf.l_margin - pdf.r_margin
    pdf.rect(x, y, w_box, 28, style="DF")
    pdf.set_xy(x + 4, y + 3)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(*DEEP_ORANGE)
    pdf.cell(w_box - 8, 6, "Guarda este link en tu celular", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_x(x + 4)
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(w_box - 8, 5, "Tu bienvenida digital con horarios, aulas, mapas y todo lo que necesitas.",
             align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_x(x + 4)
    pdf.set_font("Helvetica", "U", 9)
    pdf.set_text_color(*BLUE)
    pdf.cell(w_box - 8, 6, "Abrir mi paquete de bienvenida",
             align="C", link=app_link, new_x="LMARGIN", new_y="NEXT")
    pdf.set_y(y + 32)
    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(0.2)
    pdf.set_text_color(*DARK)
    pdf.ln(3)

    pdf.colored_box(
        "SEDE: UPC Campus Villa, Chorrillos, Lima\n"
        "Capacitacion presencial de 2 dias  |  Marzo 2026"
    )

    # ===== PAGE 2: UGEL TABLE =====
    pdf.add_page()
    pdf.section_title("Informacion por UGEL")
    pdf.body_text(
        "Busca tu UGEL en la tabla para conocer las fechas de tu capacitacion, "
        "el punto de encuentro del bus y tu grupo.",
        size=9
    )
    pdf.ln(3)

    # UGEL data - using a card-style layout instead of a cramped table
    ugels = [
        ("UGEL 01", "Grupo I", "Jueves 12 y Viernes 13 de marzo",
         "Sede UGEL 01 - San Juan de Miraflores", "Los s/n, Los Angeles, San Juan de Miraflores"),
        ("UGEL 02", "Grupo I", "Jueves 12 y Viernes 13 de marzo",
         "Sede UGEL 02 - Rimac", "Jr. Alfonso Bernal Montoya Mz B1, San Martin de Porres"),
        ("UGEL 03", "Grupo I", "Jueves 12 y Viernes 13 de marzo",
         "Sede UGEL 03 - Brena", "Av. Iquitos 918, La Victoria"),
        ("UGEL 04", "Grupo I", "Jueves 12 y Viernes 13 de marzo",
         "Sede UGEL 04 - Comas", "Av. Carabayllo 561, Comas"),
        ("UGEL 05", "Grupo II", "Fechas por confirmar",
         "Sede UGEL 05 - San Juan de Lurigancho", "Av. Peru s/n Urb, San Juan de Lurigancho"),
        ("UGEL 06", "Grupo II", "Fechas por confirmar",
         "Sede UGEL 06 - Ate", "Av. La Molina 905, La Molina"),
        ("UGEL 07", "Grupo II", "Fechas por confirmar",
         "Sede UGEL 07 - San Borja", "Ca. Jose Alvarez Calderon 492, San Borja"),
    ]

    for i, (ugel, grupo, fechas, bus, addr) in enumerate(ugels):
        if pdf.get_y() > 245:
            pdf.add_page()
        is_g1 = grupo == "Grupo I"
        # UGEL name bar
        color = ORANGE if is_g1 else (160, 160, 160)
        pdf.set_fill_color(*color)
        pdf.set_text_color(*WHITE)
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(35, 7, ugel, fill=True, new_x="END")
        pdf.set_fill_color(*(LIGHT_BG if is_g1 else (240, 240, 240)))
        pdf.set_text_color(*DARK)
        pdf.set_font("Helvetica", "B", 9)
        pdf.cell(25, 7, "  " + grupo, fill=True, new_x="END")
        pdf.set_font("Helvetica", "", 9)
        pdf.cell(0, 7, "  " + fechas, fill=True, new_x="LMARGIN", new_y="NEXT")
        # Bus + address
        pdf.set_font("Helvetica", "", 8)
        pdf.set_text_color(80, 80, 80)
        pdf.cell(0, 5, "    Bus: " + bus + "  |  " + addr, new_x="LMARGIN", new_y="NEXT")
        pdf.set_text_color(*DARK)
        pdf.ln(2)

    pdf.ln(3)
    pdf.colored_box(
        "IMPORTANTE: El bus sale puntual a las 7:00 AM desde la sede de tu UGEL. "
        "El viaje dura entre 45 y 90 minutos dependiendo de tu ubicacion. "
        "Ten tu DNI listo para ingresar al campus."
    )

    # ===== PAGE 3: YOUR DAY STEP BY STEP =====
    pdf.add_page()
    pdf.section_title("Tu Dia en la UPC - Paso a Paso")

    steps = [
        ("7:00 AM", "Salida del bus desde tu UGEL",
         "El bus sale puntual a las 7:00 AM desde la sede de tu UGEL."),
        ("~8:00 AM", "Llegada a UPC Campus Villa",
         "Al llegar, el personal de seguridad verificara tu DNI. Ten tu documento listo."),
        ("8:00 AM", "Registro y bienvenida",
         "En la mesa de registro recibiras tu gafete de color, un mini mapa del campus y tu bolsa de bienvenida."),
        ("8:00 - 8:45", "Desayuno",
         "Sube a la cafeteria del 2do piso para el desayuno de bienvenida. Servicio tipo buffet."),
        ("8:45 AM", "Traslado a tu aula",
         "Sigue la senalizacion de tu color desde la cafeteria hasta tu aula."),
        ("9:00 AM", "Inicio de la capacitacion",
         "En tu puesto encontraras la guia impresa de tu curso. Las sesiones comienzan a las 9:00 AM."),
        ("Almuerzo", "Almuerzo escalonado",
         "PIP/Tutoria: 12:00-1:00 PM  |  Matematica: 1:00-2:00 PM. Cafeteria 2do piso."),
        ("Dia 2 - 5:30", "Clausura",
         "Palabras finales y foto grupal en el auditorio. Bus de regreso a tu UGEL (~6:10 PM)."),
    ]

    for idx, (time, title, desc) in enumerate(steps):
        if pdf.get_y() > 255:
            pdf.add_page()
        pdf.set_fill_color(*ORANGE)
        pdf.set_text_color(*WHITE)
        pdf.set_font("Helvetica", "B", 10)
        x0 = pdf.get_x()
        pdf.cell(8, 6, str(idx + 1), fill=True, align="C", new_x="END")
        pdf.set_text_color(*DEEP_ORANGE)
        pdf.set_font("Helvetica", "B", 9)
        pdf.cell(30, 6, "  " + time, new_x="END")
        pdf.set_text_color(*DARK)
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(0, 6, title, new_x="LMARGIN", new_y="NEXT")
        pdf.set_x(x0 + 8)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(80, 80, 80)
        pdf.multi_cell(0, 4.5, desc, new_x="LMARGIN", new_y="NEXT")
        pdf.set_text_color(*DARK)
        pdf.ln(3)

    # Photos right after steps - check space
    pdf.ln(2)
    # Two small photos side by side
    photo_w = 85
    gap = 10
    x_left = 15
    x_right = x_left + photo_w + gap

    # Check if we have ~75mm for photos
    if pdf.get_y() > 190:
        pdf.add_page()

    y_photos = pdf.get_y()
    entrada = os.path.join(FOTOS, "entrada_upc.jpeg")
    cafe = os.path.join(FOTOS, "cafeteria_2do_piso.jpeg")

    if os.path.exists(entrada):
        pdf.image(entrada, x=x_left, y=y_photos, w=photo_w)
    if os.path.exists(cafe):
        pdf.image(cafe, x=x_right, y=y_photos, w=photo_w)

    # Move below photos (estimate ~55mm for photos)
    pdf.set_y(y_photos + 55)
    pdf.set_font("Helvetica", "I", 7)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(photo_w, 4, "Entrada UPC Campus Villa", align="C", new_x="END")
    pdf.cell(gap, 4, "", new_x="END")
    pdf.cell(photo_w, 4, "Cafeteria 2do piso", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(*DARK)

    # ===== TEACHER TYPE SECTIONS =====

    # ---------- MATEMATICA ----------
    pdf.add_page()
    pdf.header_bar("DOCENTES DE MATEMATICA", "Gafete ROJO", color=RED)

    pdf.section_title("Tu Aula")
    pdf.body_text("Laboratorios de PC (Lab PC 1, Lab PC 2 o Lab PC 3)", bold=True)
    pdf.body_text("Area de laboratorios de computo", size=9)
    pdf.ln(2)
    pdf.bullet("-", "Ubicacion: Area de laboratorios de computo")
    pdf.bullet("-", "Capacidad: ~35 personas por laboratorio (3 labs en total)")
    pdf.bullet("-", "Como llegar: Desde la cafeteria, sigue las flechas ROJAS hacia los labs")
    pdf.ln(3)

    # Two photos side by side (both landscape)
    y_p = pdf.get_y()
    tunel = os.path.join(FOTOS, "tunel_edificio_h.png")
    labs = os.path.join(FOTOS, "aulas_h315_h316.png")
    if os.path.exists(tunel):
        pdf.image(tunel, x=x_left, y=y_p, w=photo_w)
    if os.path.exists(labs):
        pdf.image(labs, x=x_right, y=y_p, w=photo_w)
    pdf.set_y(y_p + 50)
    pdf.set_font("Helvetica", "I", 7)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(photo_w, 4, "Tunel hacia los laboratorios", align="C", new_x="END")
    pdf.cell(gap, 4, "", new_x="END")
    pdf.cell(photo_w, 4, "Labs de PC - tu aula", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(*DARK)
    pdf.ln(4)

    # Math schedule
    pdf.section_title("Tu Horario")
    sw = [28, 150]
    sched_math = [
        ("8:00", "Llegada, registro y bolsa de bienvenida"),
        ("8:00 - 8:45", "Desayuno de bienvenida"),
        ("8:45", "Traslado a aulas (flechas ROJAS)"),
        ("9:00", "Inicio de sesiones de la manana"),
        ("1:00 - 2:00", "ALMUERZO"),
        ("2:00", "Sesiones de la tarde"),
        ("4:00 - 4:30", "RECESO"),
        ("4:30 - 5:30", "Continuacion de sesiones"),
        ("5:30 (Dia 2)", "Clausura en auditorio + foto grupal"),
        ("~6:10", "Bus de regreso a tu UGEL"),
    ]
    pdf.sched_row(["Hora", "Actividad"], sw, bold=True, bg=RED, text_color=WHITE)
    for i, (hora, act) in enumerate(sched_math):
        bg = LIGHT_BG if i % 2 == 0 else WHITE
        if "ALMUERZO" in act: bg = (255, 235, 238)
        elif "RECESO" in act: bg = (255, 243, 224)
        pdf.sched_row([hora, act], sw, bg=bg)
    pdf.ln(3)
    pdf.body_text("Material en tu puesto:", bold=True, size=9)
    pdf.bullet("-", "Guia docente de matematica (material impreso)")

    # ---------- TUTORIA ----------
    pdf.add_page()
    pdf.header_bar("DOCENTES DE TUTORIA / OV", "Gafete VERDE", color=GREEN)

    pdf.section_title("Tu Aula")
    pdf.body_text("Mac Lab 2 + Salas A y B", bold=True)
    pdf.body_text("Biblioteca, 2do piso", size=9)
    pdf.ln(2)
    pdf.bullet("-", "Ubicacion: Biblioteca, 2do piso (cerca de la cafeteria)")
    pdf.bullet("-", "Capacidad: Mac Lab 2 (~35) + Sala A (~20) + Sala B (~20)")
    pdf.bullet("-", "Como llegar: Desde la cafeteria, sigue las flechas VERDES hacia la biblioteca")
    pdf.ln(3)

    # Two photos side by side
    y_p = pdf.get_y()
    ruta = os.path.join(FOTOS, "ruta_salas_tutoria.png")
    mac = os.path.join(FOTOS, "mac_labs.png")
    if os.path.exists(ruta):
        pdf.image(ruta, x=x_left, y=y_p, w=photo_w)
    if os.path.exists(mac):
        pdf.image(mac, x=x_right, y=y_p, w=photo_w)
    pdf.set_y(y_p + 55)
    pdf.set_font("Helvetica", "I", 7)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(photo_w, 4, "Ruta a salas de tutoria", align="C", new_x="END")
    pdf.cell(gap, 4, "", new_x="END")
    pdf.cell(photo_w, 4, "Mac Lab", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(*DARK)
    pdf.ln(4)

    # Tutoria schedule
    pdf.section_title("Tu Horario")
    sched_tut = [
        ("8:00", "Llegada, registro y bolsa de bienvenida"),
        ("8:00 - 8:45", "Desayuno de bienvenida"),
        ("8:45", "Traslado a aulas (flechas VERDES)"),
        ("9:00", "Inicio de sesiones de la manana"),
        ("12:00 - 1:00", "ALMUERZO"),
        ("1:00", "Sesiones de la tarde"),
        ("3:00 - 3:30", "RECESO"),
        ("3:30 - 5:30", "Continuacion de sesiones"),
        ("5:30 (Dia 2)", "Clausura en auditorio + foto grupal"),
        ("~6:10", "Bus de regreso a tu UGEL"),
    ]
    pdf.sched_row(["Hora", "Actividad"], sw, bold=True, bg=GREEN, text_color=WHITE)
    for i, (hora, act) in enumerate(sched_tut):
        bg = LIGHT_BG if i % 2 == 0 else WHITE
        if "ALMUERZO" in act: bg = (232, 245, 233)
        elif "RECESO" in act: bg = (255, 243, 224)
        pdf.sched_row([hora, act], sw, bg=bg)
    pdf.ln(3)
    pdf.body_text("Material en tu puesto:", bold=True, size=9)
    pdf.bullet("-", "Guia de tutoria (material impreso)")

    # ---------- PIP ----------
    pdf.add_page()
    pdf.header_bar("DOCENTES DE INNOVACION (PIP)", "Gafete AZUL", color=BLUE)

    pdf.section_title("Tu Aula")
    pdf.body_text("Sala de Computadoras - Biblioteca", bold=True)
    pdf.body_text("Biblioteca, 3er piso", size=9)
    pdf.ln(2)
    pdf.bullet("-", "Ubicacion: Biblioteca, 3er piso")
    pdf.bullet("-", "Capacidad: ~50 personas")
    pdf.bullet("-", "Como llegar: Desde la cafeteria, sigue las flechas AZULES hacia la biblioteca, sube al 3er piso")
    pdf.ln(3)

    pdf.add_photo(os.path.join(FOTOS, "biblioteca_3er_piso.png"),
                  "3er piso - Sala de Computadoras (tu aula de innovacion)", max_w=100)

    # PIP schedule
    if pdf.get_y() > 170:
        pdf.add_page()
    pdf.section_title("Tu Horario")
    sched_pip = [
        ("8:00", "Llegada, registro y bolsa de bienvenida"),
        ("8:00 - 8:45", "Desayuno de bienvenida"),
        ("8:45", "Traslado a aulas (flechas AZULES)"),
        ("9:00", "Inicio de sesiones de la manana"),
        ("12:00 - 1:00", "ALMUERZO"),
        ("1:00", "Sesiones de la tarde"),
        ("3:00 - 3:30", "RECESO"),
        ("3:30 - 5:30", "Continuacion de sesiones"),
        ("5:30 (Dia 2)", "Clausura en auditorio + foto grupal"),
        ("~6:10", "Bus de regreso a tu UGEL"),
    ]
    pdf.sched_row(["Hora", "Actividad"], sw, bold=True, bg=BLUE, text_color=WHITE)
    for i, (hora, act) in enumerate(sched_pip):
        bg = LIGHT_BG if i % 2 == 0 else WHITE
        if "ALMUERZO" in act: bg = (227, 242, 253)
        elif "RECESO" in act: bg = (255, 243, 224)
        pdf.sched_row([hora, act], sw, bg=bg)
    pdf.ln(3)
    pdf.body_text("Material en tu puesto:", bold=True, size=9)
    pdf.bullet("-", "Los 5 Compromisos + Afiches (material impreso)")

    # ===== WHAT YOU RECEIVE & BRING =====
    pdf.add_page()
    pdf.section_title("Que Recibiras")
    pdf.body_text("Todo el material necesario te sera entregado.", size=9)
    pdf.ln(3)

    pdf.body_text("Bolsa de bienvenida (en el registro):", bold=True, size=10)
    pdf.ln(2)
    for item in ["Bolsa del programa", "Llavero", "Plancha de stickers",
                 "Tomatodo", "Cuaderno", "Lapiceros"]:
        pdf.bullet("*", item)
    pdf.ln(4)

    pdf.body_text("En tu puesto (dentro del aula):", bold=True, size=10)
    pdf.ln(2)
    pdf.bullet("*", "Guia impresa de tu curso (segun tu tipo de docente)")
    pdf.bullet("*", "Computadora con los materiales digitales")
    pdf.ln(5)

    pdf.section_title("Que Necesitas Traer")
    pdf.ln(2)

    # DNI box
    pdf.set_fill_color(255, 235, 238)
    pdf.set_draw_color(*RED)
    pdf.set_line_width(0.8)
    x, y = pdf.get_x(), pdf.get_y()
    w_box = usable_w
    pdf.rect(x, y, w_box, 18, style="DF")
    pdf.set_xy(x + 4, y + 3)
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(*RED)
    pdf.cell(0, 6, "DNI (OBLIGATORIO)", new_x="LMARGIN", new_y="NEXT")
    pdf.set_x(x + 4)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 5, "Sin DNI no podras ingresar al campus de la UPC.", new_x="LMARGIN", new_y="NEXT")
    pdf.set_y(y + 22)
    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(0.2)
    pdf.set_text_color(*DARK)

    pdf.ln(3)
    pdf.bullet("*", "Ropa comoda (dos dias de actividades practicas)")
    pdf.ln(4)

    pdf.colored_box(
        "TODO LO DEMAS LO PROPORCIONAMOS NOSOTROS\n"
        "Desayuno, almuerzo, receso, materiales de trabajo, cuaderno, "
        "lapiceros y el transporte de ida y vuelta estan incluidos."
    )

    # ===== CERTIFICATION =====
    pdf.ln(5)
    pdf.section_title("Certificacion")

    # Cert box - green themed
    pdf.set_fill_color(232, 245, 233)
    pdf.set_draw_color(*GREEN)
    pdf.set_line_width(0.8)
    x, y = pdf.get_x(), pdf.get_y()
    w_box = pdf.w - pdf.l_margin - pdf.r_margin
    pdf.rect(x, y, w_box, 30, style="DF")
    pdf.set_xy(x + 4, y + 3)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(*GREEN)
    pdf.cell(w_box - 8, 6, "Certificado oficial de la DRELM y la UPC", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_x(x + 4)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*DARK)
    pdf.multi_cell(w_box - 8, 5,
        "Al completar los dos dias de capacitacion recibiras un certificado "
        "emitido por la DRELM y la UPC, valido para tu escalafon docente.",
        align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_y(y + 34)
    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(0.2)

    pdf.ln(2)
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 5, "* La asistencia a AMBOS dias es obligatoria para recibir el certificado.",
             new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(*DARK)

    # ===== CAMPUS PHOTOS =====
    pdf.add_page()
    pdf.section_title("Conoce el Campus - UPC Campus Villa")
    pdf.ln(2)

    # Big entrance photo
    pdf.add_photo(os.path.join(FOTOS, "entrada_upc.jpeg"),
                  "Entrada principal - UPC Campus Villa, Chorrillos", max_w=160)

    # Two smaller photos side by side
    y_p = pdf.get_y()
    if y_p > 190:
        pdf.add_page()
        y_p = pdf.get_y()

    cafe_path = os.path.join(FOTOS, "cafeteria_2do_piso.jpeg")
    lounge_path = os.path.join(FOTOS, "zona_lounge.jpeg")
    if os.path.exists(cafe_path):
        pdf.image(cafe_path, x=x_left, y=y_p, w=photo_w)
    if os.path.exists(lounge_path):
        pdf.image(lounge_path, x=x_right, y=y_p, w=photo_w)
    pdf.set_y(y_p + 55)
    pdf.set_font("Helvetica", "I", 7)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(photo_w, 4, "Cafeteria 2do piso", align="C", new_x="END")
    pdf.cell(gap, 4, "", new_x="END")
    pdf.cell(photo_w, 4, "Zona lounge", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(*DARK)
    pdf.ln(4)

    # Two more photos side by side
    y_p = pdf.get_y()
    if y_p > 190:
        pdf.add_page()
        y_p = pdf.get_y()

    mac_path = os.path.join(FOTOS, "mac_labs.png")
    labs_path = os.path.join(FOTOS, "aulas_h315_h316.png")
    if os.path.exists(mac_path):
        pdf.image(mac_path, x=x_left, y=y_p, w=photo_w)
    if os.path.exists(labs_path):
        pdf.image(labs_path, x=x_right, y=y_p, w=photo_w)
    pdf.set_y(y_p + 55)
    pdf.set_font("Helvetica", "I", 7)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(photo_w, 4, "Mac Labs", align="C", new_x="END")
    pdf.cell(gap, 4, "", new_x="END")
    pdf.cell(photo_w, 4, "Labs de PC", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(*DARK)

    # ===== FOOTER =====
    pdf.ln(8)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(*ORANGE)
    pdf.cell(0, 6, "Eligiendo Mi Camino", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*DARK)
    pdf.cell(0, 5, "DRELM  |  Banco Mundial  |  UPC  |  uDocz", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 5, "Capacitacion Docente  |  Marzo 2026", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    pdf.set_text_color(*BLUE)
    pdf.set_font("Helvetica", "U", 8)
    pdf.cell(0, 5, "Mas informacion: " + wb_link, align="C", link=wb_link, new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(*DARK)

    # Output
    out_path = os.path.join(BASE, "Bienvenida_Docentes_EMC.pdf")
    pdf.output(out_path)
    print(f"PDF generado: {out_path}")
    print(f"Paginas: {pdf.pages_count}")


if __name__ == "__main__":
    build_pdf()
