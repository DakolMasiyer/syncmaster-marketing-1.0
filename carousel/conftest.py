import sys
from pathlib import Path

# Allow `from generators...` and `import figma_publisher` from tests.
sys.path.insert(0, str(Path(__file__).resolve().parent))
