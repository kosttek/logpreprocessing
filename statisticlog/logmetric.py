__author__ = 'kosttek'


'''Zwraca procentowo slowa na tym samym miejscu w zdaniu'''
class SequenceMatcher():
    def __init__(self,a,b):
        self.count = 0
        self.max_word_count = None
        self.different_words = set()

        self.init_compute_match(a,b)

    def init_compute_match(self,a,b):
        word_list_a = a.split(" ")
        word_list_b = b.split(" ")
        min_index = min(len(word_list_a),len(word_list_b))

        for i in range(0,min_index):
            if word_list_a[i] == word_list_b[i]:
                self.count+=1
            else :
                self.different_words.add(i)
        self.max_word_count = max(len(word_list_a),len(word_list_b))

    def ratio(self):
        return float(self.count)/self.max_word_count
