#!/usr/bin/env python3
"""Detecta (y opcionalmente repara) mojibake cp1252/latin-1 -> UTF-8 en un repo.

El mojibake es texto que se decodifico con la codificacion equivocada y se
re-guardo como UTF-8. "más" acaba en disco como "mÃ¡s"; el emoji "🛡️" como
"ðŸ›¡ï¸". Es drift de codificacion: nadie lo escribio asi, se degrado solo.

POR QUE ESTE SCRIPT Y NO grep
-----------------------------
Detectar mojibake con `grep 'Ã'` NO funciona de forma fiable: el patron no-ASCII
viaja por el shell/terminal y puede llegar corrupto, con lo que acabas buscando
los BYTES del texto SANO y "encontrando" coincidencias en ficheros correctos
(falso positivo masivo). Aqui la deteccion es programatica, por round-trip, sin
que ningun patron cruce el shell.

POR QUE 'SLOPPY' cp1252
-----------------------
cp1252 deja 5 bytes sin definir: 0x81 0x8D 0x8F 0x90 0x9D. Los emoji los llevan
a menudo (p.ej. el selector VS16 U+FE0F -> EF B8 8F). Quien corrompio el fichero
los trato como latin-1, asi que para deshacerlo hay que encodear igual: cp1252
donde este definido y latin-1 en esos 5 huecos. Con cp1252 PURO esas lineas
lanzan UnicodeEncodeError y se quedan sin reparar EN SILENCIO: el fichero parece
arreglado (el texto acentuado se corrige) pero los emoji siguen rotos.

Uso:
    python mojibake_probe.py [ruta]            # informe (solo lectura)
    python mojibake_probe.py [ruta] --fix      # repara in situ
    python mojibake_probe.py [ruta] --show     # muestra antes/despues escapado
"""
import argparse
import pathlib
import sys

EXTS = {'.md', '.json', '.html', '.py', '.yml', '.yaml', '.jsonc', '.toml',
        '.txt', '.css', '.js', '.ts', '.rst', '.csv', '.xml'}
SKIP_DIRS = {'.git', 'node_modules', '.venv', 'venv', '__pycache__', 'dist',
             'build', 'target', '.mypy_cache', '.pytest_cache'}

# --- Tabla sloppy-cp1252: byte -> char (huecos de cp1252 resueltos como latin-1)
_DEC = {}
for _b in range(256):
    try:
        _DEC[_b] = bytes([_b]).decode('cp1252')
    except UnicodeDecodeError:
        _DEC[_b] = chr(_b)          # 0x81, 0x8D, 0x8F, 0x90, 0x9D
_ENC = {c: b for b, c in _DEC.items()}


def repair_line(line):
    """Devuelve la linea reparada, o None si esta sana / no es reparable.

    Una linea SANA casi nunca sobrevive el round-trip: al re-encodearla los bytes
    no forman UTF-8 valido -> UnicodeDecodeError -> None -> se deja intacta.
    """
    try:
        fixed = bytes(_ENC[c] for c in line).decode('utf-8')
    except (KeyError, UnicodeDecodeError):
        return None
    return fixed if fixed != line else None


def repair_text(text, max_passes=5):
    """Repara linea a linea hasta punto fijo (puede haber doble capa de mojibake)."""
    total = 0
    for _ in range(max_passes):
        out, touched = [], 0
        for line in text.split('\n'):
            r = repair_line(line)
            if r is not None:
                touched += 1
                out.append(r)
            else:
                out.append(line)
        text = '\n'.join(out)
        total += touched
        if touched == 0:
            break
    return text, total


def iter_files(root):
    for p in sorted(pathlib.Path(root).rglob('*')):
        if any(d in SKIP_DIRS for d in p.parts):
            continue
        if p.is_file() and p.suffix.lower() in EXTS:
            yield p


def esc(s):
    """Escapa a ASCII puro: imprimir unicode crudo puede mentir si stdout es cp1252."""
    return s.encode('unicode_escape').decode('ascii')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('root', nargs='?', default='.')
    ap.add_argument('--fix', action='store_true', help='repara in situ')
    ap.add_argument('--show', action='store_true', help='muestra antes/despues escapado')
    args = ap.parse_args()

    rows, scanned, non_utf8 = [], 0, []
    for p in iter_files(args.root):
        try:
            original = p.read_bytes().decode('utf-8')
        except UnicodeDecodeError:
            non_utf8.append(p)        # no es UTF-8: otro problema, se reporta aparte
            continue
        scanned += 1
        fixed, touched = repair_text(original)
        if not touched:
            continue
        # Invariante: reparar NO cambia la estructura del fichero
        assert fixed.count('\n') == original.count('\n'), f'{p}: cambio el conteo de lineas'
        rows.append((touched, p, original, fixed))
        if args.show:
            shown = 0
            for a, b in zip(original.split('\n'), fixed.split('\n')):
                if a != b and shown < 3:
                    print(f'  {p}')
                    print(f'    ANTES  : {esc(a)[:100]}')
                    print(f'    DESPUES: {esc(b)[:100]}')
                    shown += 1
        if args.fix:
            with open(p, 'w', encoding='utf-8', newline='') as fh:
                fh.write(fixed)

    print(f'Archivos escaneados : {scanned}')
    print(f'Con mojibake        : {len(rows)}')
    for touched, p, _, _ in sorted(rows, reverse=True, key=lambda r: r[0]):
        mark = 'REPARADO' if args.fix else 'DETECTADO'
        print(f'  [{mark}] {touched:5} lineas  {p}')
    for p in non_utf8:
        print(f'  [NO-UTF8] {p}  <- no decodifica como UTF-8; revisar aparte')

    if args.fix and rows:
        # Prueba de fuego: tras reparar no debe quedar residual
        residual = sum(repair_text(p.read_bytes().decode('utf-8'))[1] for _, p, _, _ in rows)
        print(f'\nResidual tras reparar: {residual} (debe ser 0)')
        return 1 if residual else 0
    if not rows and not non_utf8:
        print('  -> LIMPIO')
    return 1 if rows else 0


if __name__ == '__main__':
    sys.exit(main())
