from dataclasses import dataclass

@dataclass()
class EmailModel:
    target_email: str
    email_topic: str
    email_content: str
    attachment_list: list

    def get_file_write_string(self):
        result = ""
        result += "Target email:\t" + self.target_email + "\n"
        result += "Topic:\t" + self.email_topic + "\n\n"
        result += self.email_content
        return result
