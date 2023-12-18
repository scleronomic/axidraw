from .device import Device, draw
from .drawing import Drawing
from .lindenmayer import LSystem
from .paths import (
    convex_hull,
    crop_path,
    crop_paths,
    join_paths,
    load_paths,
    path_length,
    paths_length,
    paths_to_shapely,
    quadratic_path,
    shapely_to_paths,
    simplify_path,
    simplify_paths,
    sort_paths,
)
from .planner import Planner
from .turtle import Turtle

from .hershey import text, Font
from .hershey_fonts import *

from .units import *

from .plotting import plotting

directory = "/Users/jote/Documents/art/axidraw"
