"""Рисует assets/demo.gif: ввод команды, подсветка стоп-слов, правленый текст.
Запуск: python3 scripts/make_demo_gif.py (нужен Pillow и macOS-шрифт Menlo)."""
import pathlib
from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "demo.gif"
W, H = 1000, 420
S = 2  # рисуем в 2x, потом уменьшаем — сглаживание текста
FONT = "/System/Library/Fonts/Menlo.ttc"
f_body = ImageFont.truetype(FONT, 17 * S)
f_bold = ImageFont.truetype(FONT, 17 * S, index=1)
f_small = ImageFont.truetype(FONT, 14 * S)

BG, BAR = (26, 26, 26), (38, 38, 38)
FG, DIM, MUTED = (230, 230, 230), (110, 110, 110), (150, 150, 150)
CLAY, RED_BG, RED_FG = (217, 119, 87), (92, 38, 38), (255, 160, 150)
GREEN, BOX = (166, 227, 161), (70, 70, 70)
PAD, LH = 36 * S, 27 * S

CMD = "/make-it-short normal"
ORIG = ("Наша компания является динамично развивающимся лидером рынка в сфере оказания "
        "услуг по ремонту бытовой техники. Мы осуществляем качественный ремонт в кратчайшие "
        "сроки с применением современного оборудования. Команда высококвалифицированных "
        "профессионалов с многолетним опытом работы обеспечивает индивидуальный подход к "
        "каждому клиенту. Мы ценим ваше доверие!")
STOPS = [
    ("является динамично развивающимся лидером рынка", "штамп + канцелярит"),
    ("в сфере оказания услуг по ремонту", "канцелярит"),
    ("осуществляем", "канцелярит"),
    ("качественный", "оценка вместо факта"),
    ("в кратчайшие сроки", "неопределённость"),
    ("современного", "оценка вместо факта"),
    ("высококвалифицированных профессионалов с многолетним опытом работы", "оценка + неопределённость"),
    ("индивидуальный подход к каждому клиенту", "штамп"),
    ("Мы ценим ваше доверие!", "брехня"),
]
RESULT = ("Ремонтируем холодильники, стиральные машины и плиты с 2011 года. Мастер приезжает "
          "в день заявки, 80% поломок чинит на месте за час. Гарантия на ремонт — 12 месяцев. "
          "[факт: цена диагностики]")

ranges = []
for phrase, _ in STOPS:
    i = ORIG.index(phrase)
    ranges.append((i, i + len(phrase)))


def wrap(text, width, font):
    """Возвращает строки как список (start, end) индексов в text."""
    lines, start, last_space, i = [], 0, None, 0
    while i < len(text):
        if text[i] == " ":
            last_space = i
        if font.getlength(text[start:i + 1]) > width and last_space is not None and last_space > start:
            lines.append((start, last_space))
            start = last_space + 1
            last_space = None
        i += 1
    lines.append((start, len(text)))
    return lines


TEXT_W = W * S - 2 * PAD
orig_lines = wrap(ORIG, TEXT_W, f_body)
res_lines = wrap(RESULT, TEXT_W - 40 * S, f_body)


def hl_id(pos, upto):
    for k, (a, b) in enumerate(ranges[:upto]):
        if a <= pos < b:
            return k
    return None


def frame(cmd_chars=0, show_orig=False, hl=0, dim_orig=False, legend=None,
          res_chars=None, copied=False, cursor=True):
    im = Image.new("RGB", (W * S, H * S), BG)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W * S, 34 * S], fill=BAR)
    for k, c in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        x = 20 * S + k * 20 * S
        d.ellipse([x, 11 * S, x + 12 * S, 23 * S], fill=c)
    d.text((W * S // 2, 17 * S), "claude — make-it-short", font=f_small, fill=MUTED, anchor="mm")

    y = 56 * S
    d.text((PAD, y), ">", font=f_bold, fill=CLAY)
    typed = CMD[:cmd_chars]
    d.text((PAD + 22 * S, y), typed, font=f_body, fill=FG)
    if cursor and not show_orig:
        cx = PAD + 22 * S + f_body.getlength(typed)
        d.rectangle([cx + 2 * S, y + 2 * S, cx + 11 * S, y + 21 * S], fill=FG)
    y += LH + 8 * S

    if show_orig:
        base_col = DIM if dim_orig else FG
        for (a, b) in orig_lines:
            x = PAD
            j = a
            while j < b:
                k = hl_id(j, hl)
                e = j
                while e < b and hl_id(e, hl) == k:
                    e += 1
                seg = ORIG[j:e]
                wseg = f_body.getlength(seg)
                if k is not None:
                    col = (150, 90, 90) if dim_orig else RED_FG
                    if not dim_orig:
                        d.rectangle([x - 1 * S, y - 1 * S, x + wseg + 1 * S, y + 22 * S], fill=RED_BG)
                    d.text((x, y), seg, font=f_body, fill=col)
                    d.line([x, y + 12 * S, x + wseg, y + 12 * S], fill=col, width=2 * S)
                else:
                    d.text((x, y), seg, font=f_body, fill=base_col)
                x += wseg
                j = e
            y += LH
        y += 14 * S

    if legend:
        n, label = legend
        d.text((PAD, y), f"стоп-слова: {n}", font=f_small, fill=MUTED)
        d.text((PAD + 175 * S, y), label, font=f_small, fill=RED_FG)
        y += 34 * S

    if res_chars is not None:
        bx0, bx1 = PAD, W * S - PAD
        by0 = y
        by1 = by0 + 56 * S + LH * len(res_lines) + 12 * S
        d.rounded_rectangle([bx0, by0, bx1, by1], radius=12 * S, outline=BOX, width=2 * S)
        d.text((bx0 + 20 * S, by0 + 18 * S), "Правленый текст · normal · 43 → 29 слов",
               font=f_small, fill=MUTED)
        label = "Скопировано" if copied else "Копировать"
        lw = f_small.getlength(label)
        btn = [bx1 - 20 * S - lw - 28 * S, by0 + 10 * S, bx1 - 20 * S, by0 + 40 * S]
        d.rounded_rectangle(btn, radius=7 * S, outline=GREEN if copied else BOX, width=2 * S)
        d.text(((btn[0] + btn[2]) / 2, (btn[1] + btn[3]) / 2), label, font=f_small,
               fill=GREEN if copied else FG, anchor="mm")
        ty = by0 + 56 * S
        for (a, b) in res_lines:
            seg = RESULT[a:min(b, res_chars)] if res_chars > a else ""
            if seg:
                if "[факт" in seg:
                    pre, post = seg.split("[факт", 1)
                    d.text((bx0 + 20 * S, ty), pre, font=f_body, fill=GREEN)
                    d.text((bx0 + 20 * S + f_body.getlength(pre), ty), "[факт" + post,
                           font=f_body, fill=(240, 200, 120))
                else:
                    d.text((bx0 + 20 * S, ty), seg, font=f_body, fill=GREEN)
            ty += LH
    return im.resize((W, H), Image.LANCZOS)


frames, durs = [], []
def add(im, ms):
    frames.append(im)
    durs.append(ms)

add(frame(cursor=True), 500)
for i in range(1, len(CMD) + 1):
    add(frame(cmd_chars=i), 55)
add(frame(cmd_chars=len(CMD)), 400)
add(frame(cmd_chars=len(CMD), show_orig=True, cursor=False), 1600)
for k, (_, label) in enumerate(STOPS, start=1):
    add(frame(cmd_chars=len(CMD), show_orig=True, hl=k, legend=(k, label)), 650)
add(frame(cmd_chars=len(CMD), show_orig=True, hl=len(STOPS), legend=(len(STOPS), "убираем или меняем на факт")), 1400)
step = 6
for c in list(range(0, len(RESULT), step)) + [len(RESULT)]:
    add(frame(cmd_chars=len(CMD), show_orig=True, hl=len(STOPS), dim_orig=True, res_chars=c), 35)
add(frame(cmd_chars=len(CMD), show_orig=True, hl=len(STOPS), dim_orig=True, res_chars=len(RESULT)), 1500)
add(frame(cmd_chars=len(CMD), show_orig=True, hl=len(STOPS), dim_orig=True, res_chars=len(RESULT), copied=True), 3500)

sheet = Image.new("RGB", (W, H * 3))
for k, idx in enumerate([0, len(STOPS) + len(CMD) + 2, -1]):
    sheet.paste(frames[idx], (0, H * k))
master = sheet.quantize(colors=200, method=Image.Quantize.MEDIANCUT)
pal = [f.quantize(palette=master, dither=Image.Dither.NONE) for f in frames]
OUT.parent.mkdir(exist_ok=True)
pal[0].save(OUT, save_all=True, append_images=pal[1:], duration=durs, loop=0, optimize=True, disposal=1)
frames[-1].save(OUT.with_name("preview.png"))
print(OUT, len(frames), "кадров", OUT.stat().st_size // 1024, "КБ")
