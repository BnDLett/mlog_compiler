class Block:
    enabled: bool
    processor_id: int

    def __init__(self, processor_id):
        self.processor_id = processor_id


class MessageBlock(Block):
    content: str

    def __init__(self, processor_id: int, content: str):
        super().__init__(processor_id)

        self.content = content

    def get_processor_representation(self) -> str:
        return f"print {self.content}\nprintflush message{self.processor_id}"
