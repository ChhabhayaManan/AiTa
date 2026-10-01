from app.core.config import settings


def test_execution_defaults():
    assert settings.EXECUTION_PROVIDER == "sidecar"
    assert settings.EXEC_WALL_SECONDS == 2.0
    assert settings.EXEC_MEMORY_MB == 256
    assert settings.EXEC_OUTPUT_KB == 64


def test_pipeline_and_generation_defaults():
    assert settings.EVAL_PIPELINE in ("v1", "v2")
    assert settings.TEST_CASES_MIN == 3
    assert settings.TEST_CASES_TARGET == 8
    assert settings.REFERENCE_MAX_ATTEMPTS == 3


def test_llm_defaults():
    assert settings.LLM_MAX_OUTPUT_TOKENS == 8192
    assert settings.NVIDIA_MODEL
    assert settings.NVIDIA_CODEGEN_MODEL
