from dotenv import load_dotenv

from src.i2global_backend.application import app

from src.i2global_backend.hypercorn_app import HypercornApplication


def main() -> None:
    load_dotenv(".env.developent")
    hypercorn_app = HypercornApplication(app)
    hypercorn_app.run()


if __name__ == "__main__":
    main()
