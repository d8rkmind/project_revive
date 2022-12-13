from prompt_toolkit.validation import Validator, ValidationError


class InputValidaton(Validator):
    def validate(self, document) -> None:
        text = document.text
        k = len(text)
        text = text.strip()
        if text.startswith("options"):
            if len(text) > 7 and not text.startswith('set', 8) and not text.startswith('load', 8):
                raise ValidationError(
                    message="options require any of these two sub commands <set|load|unset> \
[OPTIONS RESPECTIVELY]", cursor_position=k)
            elif text.startswith('set', 8) and len(text) == 11:
                raise ValidationError(
                    message="set command requires you to set key-value pairs by using KEY=VALUE \
you can set multiple values at ones by seperating it with commas < key1=value1,key2=value2 >",
                    cursor_position=k)
            elif text.startswith('load', 8) and len(text) == 12:
                raise ValidationError(
                    message="load command requires a plugin name press tab to auto complete",
                    cursor_position=k)
            elif text[-1] == "=":
                raise ValidationError(
                    message="You need to set a value", cursor_position=k)
            elif text.count(',') != 0 and text.count('=') != text.count(',') + 1:
                raise ValidationError(
                    message="Missing options after last ',' ", cursor_position=k)
        elif text.startswith("result"):
            if len(text) > 6 and not text.removeprefix("result ").isdigit():
                raise ValidationError(
                    message="Index value should be an integer",
                    cursor_position=k
                )
