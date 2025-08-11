def comma_tokenizer(text):
    return [token.strip().lower() for token in text.split(',') if token.strip()]
