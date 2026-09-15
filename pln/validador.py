from typing import Optional

from pydantic import BaseModel, Field


FORMAS_VALIDAS = {
    "triangulo",
    "copo",
    "cantor",
    "helecho"
}


class RepresentacionFractal(BaseModel):

    forma: str

    repeticiones: Optional[int] = Field(
        default=None,
        ge=0
    )

    angulo: Optional[float] = None

    color: Optional[str] = None


def validar_representacion(datos):

    representacion = (
        RepresentacionFractal(
            **datos
        )
    )

    if (
        representacion.forma
        not in FORMAS_VALIDAS
    ):
        raise ValueError(
            "Forma no válida para FractalESP: "
            f"{representacion.forma}"
        )

    return representacion