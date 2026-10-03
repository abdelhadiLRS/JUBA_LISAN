import os
import subprocess
import sys


def test_alembic_metadata_in_clean_process_has_billing_and_quota_tables():
    code = "import app.models; from app.core.database import Base; required={'billing_intents','feature_usage','feature_reservations'}; assert required <= set(Base.metadata.tables), required-set(Base.metadata.tables)"
    result = subprocess.run([sys.executable,"-c",code],cwd=os.getcwd(),env=os.environ.copy(),capture_output=True,text=True,timeout=30)
    assert result.returncode == 0, result.stderr
