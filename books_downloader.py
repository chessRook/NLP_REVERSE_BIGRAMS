import urllib.request

web_url = r'http://www.gutenberg.org/files/'
books_amount = 10
start_from = 567
skip = 3
file_path = r'.\texts\check_that_runs.txt'


def main_downloader():
    for idx in range(1, skip * books_amount, skip):
        book_url = get_book_url(start_from, idx)
        book_text = books_downloader(book_url)
        pure_text = remove_non_book_parts(book_text)
        with open(file_path, 'a') as file:
            file.write(pure_text)


def remove_non_book_parts(book_text):
    splitter = 'project gutenberg'
    start_two_times_splitters = ['chapter i', 'part i']
    book_text = split_on_text_by_middle(book_text, splitter)
    for splitter_2 in start_two_times_splitters:
        book_text = start_two_times_splitter(book_text, splitter_2)
    book_text = book_text.strip()
    try:
        index = book_text.rindex('end of')
        if index > len(book_text) * 0.95:
            book_text = book_text[:index]
    except:
        pass
    book_text = ''.join([single_char if single_char.isalpha() else ' '
                         for single_char in book_text])
    print('*' * 30)
    print(book_text)
    return book_text


def start_two_times_splitter(text, splitter):
    for _ in range(2):
        if splitter not in text:
            return text
        index = text.index(splitter)
        if index > len(text) / 2 or text[index + len(splitter)].isalpha():
            return text
        text = text[index + len(splitter):]
    return text


def split_on_text_by_middle(text, splitter):
    splitter_len = len(splitter)
    while splitter in text:
        index = text.index(splitter)
        length = len(text)
        if index < length / 2:
            text = text[index + splitter_len:]
        else:
            text = text[:index]
    return text


def books_downloader(book_url):
    try:
        with urllib.request.urlopen(book_url) as f:
            try:
                text = f.read().decode('utf-8', errors='ignore').lower()
            except:
                pass
    except:
        return ''
    return text


def get_book_url(start_from, idx):
    book_number = start_from + idx
    book_page_url = f'{web_url}/{book_number}/{book_number}.txt'
    return book_page_url


if __name__ == '__main__':
    main_downloader()
