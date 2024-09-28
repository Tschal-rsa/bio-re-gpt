from utils import Message, request
from config import Sample, Eval, evaluate, Const, Config


class Baseline:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.system_message = Message("system", Const.system_text(config.ner))
        self.example_messages = [
            message
            for example in Const.task_examples[config.dataset]
            for message in (
                self.wrap_question(example, True),
                self.wrap_answer(example, True),
            )
        ]

    def __call__(self, sample: Sample) -> Eval:
        question_message = self.wrap_question(sample)
        request_messages = [
            self.system_message,
            *self.example_messages,
            question_message,
        ]
        response = request(request_messages, self.config.model)
        return evaluate(response.content, sample.result)

    def wrap_question(self, sample: Sample, is_example: bool = False) -> Message:
        question = sample.text + " " + Const.question_text(self.config.dataset, self.config.ner)
        return Message("user", question, is_example)

    def wrap_answer(self, sample: Sample, is_example: bool = False) -> Message:
        answer = Const.answer_text(self.config.dataset, sample.result)
        return Message("assistant", answer, is_example)
