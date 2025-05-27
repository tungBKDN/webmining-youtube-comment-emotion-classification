import re
import nltk
from nltk.tokenize import word_tokenize
import underthesea

class Preprocessor:
	def __init__(self):
		self.stop_words_path = "./artifacts/vietnamese-stopwords.txt"
		self.stop_words = self.load_stop_words(self.stop_words_path)

	def load_stop_words(self, file_path: str):
		"""
		Load stop words from a file and return them as a set.

		:param file_path: Path to the stop words file.
		:return: A set of stop words.
		"""
		print("Loading stop words...")
		try:
			with open(file_path, 'r', encoding='utf-8') as file:
				stop_words : set = set(file.read().splitlines())
			return stop_words
		except Exception as e:
			print(f"Error loading stop words: {e}")
			return set()

	def remove_html_tags(self, text: str) -> str:
		"""
		Remove HTML tags from a given text.

		:param text: The input text from which to remove HTML tags.
		:return: The text with HTML tags removed.
		"""
		if not isinstance(text, str):
			return text
		return re.sub(r'<[^>]+>', '', text)

	def remove_punctuation_and_numbers(self, text: str) -> str:
		"""
		Remove punctuation and numbers from a given text.

		:param text: The input text from which to remove punctuation and numbers.
		:return: The text with punctuation and numbers removed.
		"""
		if not isinstance(text, str):
			return text
		# Remove all kinds of punctuation and numbers
		removed_punctuation = re.sub(r'[^\w\s]', ' ', text)
		removed_numbers = re.sub(r'\d+', ' ', removed_punctuation)
		# Remove extra whitespace
		cleaned_text = re.sub(r'\s+', ' ', removed_numbers).strip()
		# Return the lowercased text
		return cleaned_text.lower()


	def remove_stopwords(self, text: str, stop_words: set):
		"""
		Remove stop words from a given text, prioritizing longer stop words first.

		:param text: The input text from which to remove stop words.
		:param stop_words: A set or list of stop words to remove.
		:return: The text with stop words removed.
		"""
		if not isinstance(text, str):
			return text

		# Sort stopwords by length descending
		sorted_stops = sorted(stop_words, key=lambda w: -len(w))

		# Build regex pattern (whole words, word boundaries)
		pattern = r'\b(?:' + '|'.join(re.escape(w) for w in sorted_stops) + r')\b'

		# Replace matched stopwords with empty string
		cleaned = re.sub(pattern, '', text)

		# Remove extra whitespace
		cleaned = re.sub(r'\s+', ' ', cleaned).strip()

		# If the cleaned text is empty, return the original text
		return cleaned if cleaned else text

	def tokenize(self, text: str) -> str:
		result = underthesea.word_tokenize(text, format="text")
		if isinstance(result, list):
			return ' '.join(result)
		return str(result)

# Test
# if __name__ == "__main__":
	# preprocessor = Preprocessor()
	# test_text = "Đây là một ví dụ về việc loại bỏ từ dừng."
	# test_text = preprocessor.remove_html_tags(test_text)
	# test_text = preprocessor.remove_punctuation_and_numbers(test_text)
	# cleaned_text = preprocessor.remove_stopwords(test_text, preprocessor.stop_words)
	# tokenized_text = preprocessor.tokenize(cleaned_text)
	# print(f"Cleaned Text: {cleaned_text}")
	# print(f"Tokenized Text: {tokenized_text}")