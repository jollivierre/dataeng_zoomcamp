import sys
import pandas as pd

print('all args entered at runtime:', sys.argv)

day = sys.argv[1]


# some fancy stuff with pandas

ver = pd.__version__

print('pandas version:', ver)
print('job finished successfully for day = ', day)