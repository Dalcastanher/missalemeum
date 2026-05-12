import re

from api.constants import common as constants
from api.constants.common import TRANSFORMATIONS_COMMON

PDF_LABELS = {
    "rank": "Ritus",
    "colors": "Color"
}

PDF_RANK_LABELS = {
    1: "Classis I",
    2: "Classis II",
    3: "Classis III",
    4: "Classis IV",
}

PDF_COLOR_LABELS = {
    "g": "Virides",
    "r": "Rubri",
    "w": "Albi",
    "v": "Violacei",
    "p": "Rosacei",
    "b": "Nigri",
}
