from src.app_factory import AppFactory


factory = AppFactory()
app = factory.create_app(testing=False, build_optimized=True)
