


class StringMatchHelper:

    @staticmethod
    def split_string(string: str) -> str:

        ret: list[str] = []
        current_word: str = ''

        for char in string:

            if char in {' ', '_', '(', ')'}:
                if current_word:
                    ret.append(current_word)
                    current_word = ''

            elif char in {'.', '\'', '"', '-'}:
                pass
            
            else: current_word += char

        if current_word: ret.append(current_word)

        return ret

    @staticmethod
    def string_match(string_to_match: str, target_string: str) -> bool:
        
        if target_string == '': return True

        for target in StringMatchHelper.split_string(target_string):

            if target.lower().startswith(string_to_match.lower()):
                return True
        
        return False
    


