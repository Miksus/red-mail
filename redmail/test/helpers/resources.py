
from io import BytesIO

import pytest

def get_mpl_fig():
    pytest.importorskip("matplotlib")
    import matplotlib.pyplot as plt
    # Data for plotting
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3])

    buf = BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    bytes = buf.read()
    return fig, bytes

def get_pil_image():
    pytest.importorskip("PIL")
    from PIL import Image
    img = Image.new('RGB', (100, 30), color = (73, 109, 137))
    buf = BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    bytes = buf.read()
    return img, bytes