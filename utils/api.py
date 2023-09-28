import openai
from typing import Literal
import time
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

Role = Literal["system", "user", "assistant"]
Model = Literal["gpt-3.5-turbo", "gpt-4"]


class Message:
    def __init__(self, role: Role, content: str, is_example: bool = False) -> None:
        self.role = role
        self.name: str | None = None
        self.content = content
        if is_example:
            self.role = "system"
            self.name = f"example_{role}"

    def to_dict(self) -> dict:
        ret = {
            "role": self.role,
            "content": self.content,
        }
        if self.name is not None:
            ret["name"] = self.name
        return ret


class Response:
    def __init__(self, model: str = "", content: str = "") -> None:
        self.model = model
        self.content = content

    def __str__(self) -> str:
        return f"Responsed by {self.model}:\n\n{self.content}"


def request_step(messages: list[Message], model: Model) -> Response:
    response = openai.ChatCompletion.create(
        model=model,
        messages=[message.to_dict() for message in messages],
        temperature=0,
    )
    return Response(
        response["model"],
        response["choices"][0]["message"]["content"],
    )


def request(messages: list[Message], model: Model) -> Response:
    time.sleep(2)
    try:
        return request_step(messages, model)
    except:
        print("Error!", end="")
        time.sleep(2)
        try:
            return request_step(messages, model)
        except:
            print("Error!", end="")
            return Response()
