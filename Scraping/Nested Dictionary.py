book_dict = {}
for each book_id, story_id, word_dict in who_knows_what:
    if book_id not in book_dict:
        book_dict[book_id] = {}
    if story_id not in book_dict[book_id]:
        book_dict[book_id][story_id] = []
    book_dict[book_id][story_id].append( word_dict )