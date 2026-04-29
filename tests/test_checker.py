import requests
from pytest_mock import MockerFixture


from simple_http_checker.checker import check_urls


def test_check_urls_success(mocker: MockerFixture):

    # mock_requests_get = mocker.patch("simple_http_checker.checker.requests.get")
    mock_get = mocker.patch("simple_http_checker.checker.requests.get")

    # Fake Response 1 → 200
    response_200 = mocker.MagicMock()
    response_200.status_code = 200
    response_200.reason = "OK"
    response_200.ok = True

    # Fake Response 2 → 404
    response_404 = mocker.MagicMock()
    response_404.status_code = 404
    response_404.reason = "Not Found"
    response_404.ok = False

    # Timeout Exception
    timeout_error = requests.exceptions.Timeout()
    connection_error = requests.exceptions.ConnectionError()
    request_error = requests.exceptions.RequestException()

    # Reihenfolge der Antworten
    # mock_get.side_effect = [response_200, response_404, timeout_error]
    mock_get.side_effect = [
        response_200,
        response_404,
        timeout_error,
        connection_error,
        request_error,
    ]

    urls = [
        "http://example.com",
        "http://example.org",
        "http://timeout.com",
        "http://connection-error.com",
        "http://request-error.com",
    ]

    results = check_urls(urls)

    assert results[urls[0]] == "200 OK"
    assert results[urls[1]] == "404 Not Found"
    assert "Timeout" in results[urls[2]]
    assert "Connection Error" in results[urls[3]]
    assert "RequestException" in results[urls[4]]


def test_check_urls_empty_list():
    urls = []
    results = check_urls(urls)
    assert results == {}


def test_check_urls_customer_timeout(mocker: MockerFixture):
    mock_get = mocker.patch("simple_http_checker.checker.requests.get")
    response_200 = mocker.MagicMock()
    response_200.status_code = 200
    response_200.reason = "OK"
    response_200.ok = True
    mock_get.return_value = response_200
    # timeout_error = requests.exceptions.Timeout()
    # mock_get.side_effect = timeout_error

    urls = ["http://example.com"]
    custom_timeout = 10
    results = check_urls(urls, timeout=custom_timeout)

    assert results[urls[0]] == "200 OK"
