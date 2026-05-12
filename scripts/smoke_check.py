from __future__ import annotations

import sys
from pathlib import Path

from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.main import app


def main() -> None:
    client = TestClient(app)
    assert client.get("/").status_code == 200
    assert client.get("/queue").status_code == 200
    assert client.get("/playbooks").status_code == 200
    assert client.get("/api/dashboard/summary").status_code == 200
    assert client.get("/api/sample").status_code == 200
    print("smoke-ok")


if __name__ == "__main__":
    main()
