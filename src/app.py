class TextProducer:
    def produce_text(self):
        return 'Hello world!'


class App:
    def __init__(self) -> None:
        pass

    def run(self):
        text_producer = TextProducer()
        print(text_producer.produce_text())
