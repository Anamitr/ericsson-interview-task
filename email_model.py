from dataclasses import dataclass

@dataclass()
class EmailModel:
    target_email: str
    email_topic: str
    email_content: str
    attachment_list: list
