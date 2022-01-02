
from redmail.utils import import_from_string

plt = import_from_string("matplotlib.pyplot", if_missing="ignore")
PIL = import_from_string("PIL", if_missing="ignore")
pd = import_from_string("pandas", if_missing="ignore")