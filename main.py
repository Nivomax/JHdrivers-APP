from gui.dashboard import open_dashboard
from gui.login_view import open_login


def main():
    open_login(on_success=lambda administrator: open_dashboard())


if __name__ == "__main__":
    main()
