# Genera test/resumen-ejemplo.pdf: resumen de tarjeta FICTICIO para probar el lector de PDF.
# Uso: python -I make_pdf.py
import pathlib

LINES = [
    "BANCO EJEMPLO S.A. - RESUMEN DE CUENTA TARJETA VISA",
    "TITULAR: CLIENTE DE PRUEBA",
    "CIERRE ACTUAL 28/11/2026   VENCIMIENTO 10/12/2026",
    "SALDO ACTUAL $ 452.380,55",
    "PAGO MINIMO $ 185.200,00",
    "T.N.A. 98,50 %   T.E.M. 8,21 %",
    "FECHA       DETALLE                                   PESOS",
    "12.08.26  MERCADOLIBRE*CELULAR      C.04/12        45.000,00",
    "03.10.26  FRAVEGA HELADERA          C.02/18        38.250,50",
    "15.09.26  DESPEGAR PASAJES   CUOTA 03 DE 06        52.100,00",
    "20.11.26  SUPERMERCADO DIA                         15.300,00",
    "22.11.26  NETFLIX                                   8.999,00",
    "05.11.26  ZAPATILLAS DEPORTE        C.01/03        21.000,00",
]


def pdf(lines):
    text = ["BT", "/F1 10 Tf", "40 800 Td", "14 TL"]
    for ln in lines:
        safe = ln.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
        text.append(f"({safe}) '")
    text.append("ET")
    stream = "\n".join(text).encode("latin-1")
    objs = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Courier >>",
        b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n" + stream + b"\nendstream",
    ]
    out = bytearray(b"%PDF-1.4\n")
    offs = []
    for i, o in enumerate(objs, 1):
        offs.append(len(out))
        out += f"{i} 0 obj\n".encode() + o + b"\nendobj\n"
    xref = len(out)
    out += f"xref\n0 {len(objs) + 1}\n0000000000 65535 f \n".encode()
    for o in offs:
        out += f"{o:010d} 00000 n \n".encode()
    out += f"trailer\n<< /Size {len(objs) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode()
    return bytes(out)


dest = pathlib.Path(__file__).with_name("resumen-ejemplo.pdf")
dest.write_bytes(pdf(LINES))
print("ok", dest)
