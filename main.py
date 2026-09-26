"""Conexión entre Python y Prolog usando pyswip (SWI-Prolog)."""

import os
import sys
from pathlib import Path

# pyswip no reconoce la estructura de SWI-Prolog 10 en macOS, así que le
# indicamos las rutas (solo si no están ya definidas y la app existe).
SWI_APP = Path("/Applications/SWI-Prolog.app/Contents")
if sys.platform == "darwin" and SWI_APP.exists():
    frameworks = str(SWI_APP / "Frameworks")
    os.environ.setdefault("LIBSWIPL_PATH", os.path.join(frameworks, "libswipl.dylib"))
    os.environ.setdefault("SWI_HOME_DIR", str(SWI_APP / "Resources" / "swipl"))
    # libswipl depende de libgmp/libz vía @rpath. macOS solo lee
    # DYLD_FALLBACK_LIBRARY_PATH al arrancar, así que relanzamos el script una vez.
    if os.environ.get("DYLD_FALLBACK_LIBRARY_PATH") != frameworks:
        os.environ["DYLD_FALLBACK_LIBRARY_PATH"] = frameworks
        os.execv(sys.executable, [sys.executable] + sys.argv)

from pyswip import Prolog  # noqa: E402  (debe importarse tras configurar el entorno)

ARCHIVO_PL = Path(__file__).parent / "familia.pl"


def main():
    prolog = Prolog()
    prolog.consult(str(ARCHIVO_PL))
    print(f"Base de conocimiento cargada: {ARCHIVO_PL.name}\n")

    # 1. Consulta verdadero/falso
    es_padre = bool(list(prolog.query("padre(juan, maria)")))
    print(f"¿juan es padre de maria? {es_padre}")

    # 2. Consulta con una variable
    hijos = [r["H"] for r in prolog.query("progenitor(juan, H)")]
    print(f"Hijos de juan: {hijos}")

    # 3. Consulta con varias variables
    print("Parejas abuelo -> nieto:")
    for r in prolog.query("abuelo(A, N)"):
        print(f"  {r['A']} -> {r['N']}")

    # 4. Recursividad: ancestros
    ancestros = sorted({r["X"] for r in prolog.query("ancestro(X, lucia)")})
    print(f"Ancestros de lucia: {ancestros}")

    # 5. Hermanos (sin duplicados)
    hermanos = sorted({r["Y"] for r in prolog.query("hermano(maria, Y)")})
    print(f"Hermanos de maria: {hermanos}")

    # 6. Aritmética en Prolog
    resultado = next(prolog.query("factorial(5, F)"))
    print(f"factorial(5) = {resultado['F']}")

    # 7. Agregar un hecho desde Python y consultarlo
    prolog.assertz("progenitor(carlos, diego)")
    prolog.assertz("hombre(diego)")
    prolog.assertz("mujer(andrea)")
    prolog.assertz("hombre(andres)")
    prolog.assertz("progenitor(andres,andrea)")
    #aqui pongo un comentario 
    nietos_maria = [r["N"] for r in prolog.query("abuelo(maria, N)")]
    print(f"Nietos de maria (tras agregar a diego): {nietos_maria}")


if __name__ == "__main__":
    main()
