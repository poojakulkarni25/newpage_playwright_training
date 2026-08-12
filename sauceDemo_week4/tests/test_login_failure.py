from pages.login_page import LoginPage


def test_failed_login_shows_error(page, random_invalid_credentials):
    login_page = LoginPage(page)
    login_page.load()

    login_page.login(
        random_invalid_credentials["username"],
        random_invalid_credentials["password"],
    )

    error_message = login_page.get_error_message()
    assert "username and password do not match" in error_message.lower(), (
        "Expected an error message for invalid SauceDemo credentials"
    )
