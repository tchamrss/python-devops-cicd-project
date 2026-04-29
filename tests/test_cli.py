from click.testing import CliRunner
from simple_http_checker.cli import main
from pytest_mock import MockerFixture


def test_no_urls_provided():
    runner = CliRunner()
    result = runner.invoke(main, [])
    assert result.exit_code == 0
    assert "usage: check-urls" in result.output


def test_main_single_url(mocker: MockerFixture):
    url = "https://example.com"
    mock_check_urls = mocker.patch(
        "simple_http_checker.cli.check_urls", return_value={url: "200 OK"}
    )
    runner = CliRunner()
    result = runner.invoke(main, [url])
    assert result.exit_code == 0
    mock_check_urls.assert_called_once_with((url,), 5)
    assert url in result.output
    assert "200 OK" in result.output


def test_main_timeout_option(mocker: MockerFixture):
    url = "https://example.com"
    timeout = 10
    mock_check_urls = mocker.patch(
        "simple_http_checker.cli.check_urls", return_value={url: "TIMEOUT"}
    )
    runner = CliRunner()
    result = runner.invoke(main, [url, "--timeout", str(timeout)])
    assert result.exit_code == 0
    mock_check_urls.assert_called_once_with((url,), timeout)
    assert url in result.output
    assert "TIMEOUT" in result.output
