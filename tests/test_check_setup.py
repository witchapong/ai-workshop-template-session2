from check_setup import check_env, check_imports, check_python_version


def test_python_version_passes_on_supported_version():
    passed, message = check_python_version()
    assert passed is True
    assert "3.1" in message


def test_imports_pass_when_dependencies_installed():
    passed, message = check_imports()
    assert passed is True, message


def test_zai_key_alone_is_enough():
    ok, message = check_env({"ZAI_API_KEY": "zai-real-key"})
    assert ok
    assert "ZAI_API_KEY" in message


def test_placeholder_zai_key_is_not_a_key():
    ok, message = check_env({"ZAI_API_KEY": "paste-your-key-here"})
    assert not ok
    assert "placeholder" in message.lower()


def test_no_key_at_all_names_the_file_to_edit():
    ok, message = check_env({})
    assert not ok
    assert ".env" in message
