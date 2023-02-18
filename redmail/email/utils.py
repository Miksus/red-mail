
from typing import TYPE_CHECKING
from redmail.utils import import_from_string

if TYPE_CHECKING:
    import matplotlib.pyplot as plt_lib
    import PIL as PIL_lib
    import pandas as pandas_lib
    import css_inline as css_inline_lib

plt: 'plt_lib' = import_from_string("matplotlib.pyplot", if_missing="ignore")
PIL: 'PIL_lib' = import_from_string("PIL", if_missing="ignore")
pd: 'pandas_lib' = import_from_string("pandas", if_missing="ignore")
css_inline: 'css_inline_lib' = import_from_string("css_inline", if_missing="ignore")