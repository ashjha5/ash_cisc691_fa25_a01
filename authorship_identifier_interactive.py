#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Interactive Authorship Identification System
User provides data on the fly, trains the model, and makes predictions interactively.
"""

import string
import json
from datetime import datetime


class AuthorshipIdentifier:
    """Interactive authorship identification system with on-the-fly training."""

    def __init__(self):
        self.author_texts = {}
        self.signatures = {}
        self.weights = [11, 33, 50, 0.4, 4, 100, 10]
        self.is_trained = False

    def clean_word(self, word):
        word = word.lower().strip()
        word = word.strip(string.punctuation)
        return word

    def split_string(self, text, separators):
        words = []
        word = ''
        for char in text:
            if char in separators:
                word = word.strip()
                if word:
                    words.append(word)
                word = ''
            else:
                word += char
        word = word.strip()
        if word:
            words.append(word)
        return words

    def get_sentences(self, text):
        return self.split_string(text, '.?!')

    def get_phrases(self, sentence):
        return self.split_string(sentence, ',;:')

    def average_word_length(self, text):
        words = text.split()
        total = 0
        count = 0
        for word in words:
            word = self.clean_word(word)
            if word:
                total += len(word)
                count += 1
        return total / count if count > 0 else 0

    def different_to_total(self, text):
        words = text.split()
        total = 0
        unique = set()
        for word in words:
            word = self.clean_word(word)
            if word:
                total += 1
                unique.add(word)
        return len(unique) / total if total > 0 else 0

    def exactly_once_to_total(self, text):
        words = text.split()
        total = 0
        unique = set()
        once = set()
        for word in words:
            word = self.clean_word(word)
            if word:
                total += 1
                if word in unique:
                    once.discard(word)
                else:
                    unique.add(word)
                    once.add(word)
        return len(once) / total if total > 0 else 0

    def average_sentence_length(self, text):
        sentences = self.get_sentences(text)
        if not sentences:
            return 0
        word_counts = [len(sentence.split()) for sentence in sentences]
        total_words = sum(word_counts)
        return total_words / len(sentences)

    def average_sentence_complexity(self, text):
        sentences = self.get_sentences(text)
        if not sentences:
            return 0
        total = 0
        for sentence in sentences:
            phrases = self.get_phrases(sentence)
            total += len(phrases)
        return total / len(sentences)

    def punctuation_density(self, text):
        if len(text) == 0:
            return 0
        punct_count = sum(1 for char in text if char in string.punctuation)
        return punct_count / len(text)

    def average_word_frequency(self, text):
        words = text.split()
        word_counts = {}
        total = 0

        for word in words:
            word = self.clean_word(word)
            if word:
                total += 1
                word_counts[word] = word_counts.get(word, 0) + 1

        if len(word_counts) == 0:
            return 0

        total_frequency = sum(word_counts.values())
        return total_frequency / len(word_counts)

    def make_signature(self, text):
        return [
            self.average_word_length(text),
            self.different_to_total(text),
            self.exactly_once_to_total(text),
            self.average_sentence_length(text),
            self.average_sentence_complexity(text),
            self.punctuation_density(text),
            self.average_word_frequency(text)
        ]

    def add_author(self, author_name, text):
        if not author_name or not text:
            return False, "Author name and text cannot be empty"

        self.author_texts[author_name] = text
        self.is_trained = False
        return True, f"Added author '{author_name}' with {len(text)} characters of text"

    def train(self):
        if not self.author_texts:
            return False, "No authors added yet. Add at least one author first."

        self.signatures = {}
        for author, text in self.author_texts.items():
            try:
                self.signatures[author] = self.make_signature(text)
            except Exception as e:
                return False, f"Error processing {author}: {str(e)}"

        self.is_trained = True
        return True, f"Model trained successfully with {len(self.signatures)} authors"

    def get_score(self, sig1, sig2):
        score = 0
        for i in range(len(sig1)):
            score += abs(sig1[i] - sig2[i]) * self.weights[i]
        return score

    def predict(self, mystery_text):
        if not self.is_trained:
            return None, "Model not trained yet. Please train the model first."

        if not mystery_text:
            return None, "Mystery text cannot be empty"

        try:
            mystery_sig = self.make_signature(mystery_text)
        except Exception as e:
            return None, f"Error processing mystery text: {str(e)}"

        best_author = None
        best_score = None
        all_scores = {}

        for author, signature in self.signatures.items():
            score = self.get_score(signature, mystery_sig)
            all_scores[author] = score

            if best_score is None or score < best_score:
                best_score = score
                best_author = author

        return best_author, all_scores

    def get_status(self):
        return {
            'authors_count': len(self.author_texts),
            'authors': list(self.author_texts.keys()),
            'is_trained': self.is_trained
        }

    def save_model(self, filename):
        if not self.is_trained:
            return False, "Model not trained yet"

        data = {
            'author_texts': self.author_texts,
            'signatures': self.signatures,
            'weights': self.weights,
            'timestamp': datetime.now().isoformat()
        }

        try:
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            return True, f"Model saved to {filename}"
        except Exception as e:
            return False, f"Error saving model: {str(e)}"

    def load_model(self, filename):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)

            self.author_texts = data['author_texts']
            self.signatures = data['signatures']
            self.weights = data.get('weights', self.weights)
            self.is_trained = True

            return True, f"Model loaded from {filename}"
        except Exception as e:
            return False, f"Error loading model: {str(e)}"

    def remove_author(self, author_name):
        if author_name in self.author_texts:
            del self.author_texts[author_name]
            if author_name in self.signatures:
                del self.signatures[author_name]
            self.is_trained = False
            return True, f"Removed author '{author_name}'"
        return False, f"Author '{author_name}' not found"

    def list_authors(self):
        if not self.author_texts:
            return "No authors added yet."

        result = "\n=== Authors in System ===\n"
        for i, (author, text) in enumerate(self.author_texts.items(), 1):
            word_count = len(text.split())
            result += f"{i}. {author} ({word_count} words)\n"
        return result


def print_menu():
    print("\n" + "=" * 60)
    print("    INTERACTIVE AUTHORSHIP IDENTIFICATION SYSTEM")
    print("=" * 60)
    print("\n[1] Add Author")
    print("[2] Train Model")
    print("[3] Predict Author of Mystery Text")
    print("[4] View Authors")
    print("[5] Remove Author")
    print("[6] Save Model")
    print("[7] Load Model")
    print("[8] System Status")
    print("[9] Exit")
    print("-" * 60)


def add_author_interactive(system):
    print("\n" + "=" * 60)
    print("ADD AUTHOR")
    print("=" * 60)

    author_name = input("\nEnter author name: ").strip()
    if not author_name:
        print("❌ Author name cannot be empty!")
        return

    print("\nEnter the author's text (paste it below).")
    print("When done, type '---END---' on a new line and press Enter:\n")

    lines = []
    while True:
        line = input()
        if line.strip() == '---END---':
            break
        lines.append(line)

    text = '\n'.join(lines)

    success, message = system.add_author(author_name, text)
    if success:
        print(f"\n✅ {message}")
    else:
        print(f"\n❌ {message}")

        def train_model_interactive(system):
            print("\n" + "=" * 60)
            print("TRAIN MODEL")
            print("=" * 60)

            success, message = system.train()
            if success:
                print(f"\n✅ {message}")
            else:
                print(f"\n❌ {message}")

        def predict_interactive(system):
            print("\n" + "=" * 60)
            print("PREDICT AUTHORSHIP")
            print("=" * 60)

            if not system.is_trained:
                print("\n❌ Model not trained yet! Please train the model first.")
                return

            print("\nEnter the mystery text (paste it below).")
            print("When done, type '---END---' on a new line and press Enter:\n")

            lines = []
            while True:
                line = input()
                if line.strip() == '---END---':
                    break
                lines.append(line)

            mystery_text = '\n'.join(lines)

            author, scores = system.predict(mystery_text)

            if author is None:
                print(f"\n❌ {scores}")
                return

            print("\n" + "=" * 60)
            print("PREDICTION RESULTS")
            print("=" * 60)
            print(f"\n🎯 PREDICTED AUTHOR: {author}")
            print("\nConfidence Scores (lower is better):")
            print("-" * 40)

            sorted_scores = sorted(scores.items(), key=lambda x: x[1])
            for auth, score in sorted_scores:
                indicator = "👉" if auth == author else "  "
                print(f"{indicator} {auth}: {score:.2f}")

        def view_authors_interactive(system):
            print("\n" + system.list_authors())

        def remove_author_interactive(system):
            print("\n" + "=" * 60)
            print("REMOVE AUTHOR")
            print("=" * 60)

            view_authors_interactive(system)

            author_name = input("\nEnter author name to remove: ").strip()
            if not author_name:
                print("❌ Author name cannot be empty!")
                return

            success, message = system.remove_author(author_name)
            if success:
                print(f"\n✅ {message}")
            else:
                print(f"\n❌ {message}")

        def save_model_interactive(system):
            print("\n" + "=" * 60)
            print("SAVE MODEL")
            print("=" * 60)

            filename = input("\nEnter filename (default: model.json): ").strip()
            if not filename:
                filename = "model.json"

            success, message = system.save_model(filename)
            if success:
                print(f"\n✅ {message}")
            else:
                print(f"\n❌ {message}")

        def load_model_interactive(system):
            print("\n" + "=" * 60)
            print("LOAD MODEL")
            print("=" * 60)

            filename = input("\nEnter filename (default: model.json): ").strip()
            if not filename:
                filename = "model.json"

            success, message = system.load_model(filename)
            if success:
                print(f"\n✅ {message}")
            else:
                print(f"\n❌ {message}")

        def show_status_interactive(system):
            print("\n" + "=" * 60)
            print("SYSTEM STATUS")
            print("=" * 60)

            status = system.get_status()
            print(f"\nAuthors Count: {status['authors_count']}")
            print(f"Trained: {'Yes ✅' if status['is_trained'] else 'No ❌'}")

            if status['authors']:
                print(f"\nAuthors: {', '.join(status['authors'])}")

        def run_demo_mode(system):
            print("\n🎬 Loading demo data...")

            demo_texts = {
                'Agatha Christie': """
                The Murder at the Vicarage is a work of detective fiction by Agatha Christie. 
                It features Miss Marple, one of Christie's most beloved characters. 
                The story unfolds in the quaint village of St. Mary Mead.
                A murder occurs, and Miss Marple uses her keen observation skills to solve it.
                The narrative is filled with red herrings and clever plot twists.
                """,

                'Arthur Conan Doyle': """
                The Hound of the Baskervilles is perhaps the most famous Sherlock Holmes tale. 
                Holmes investigates a supernatural legend on the eerie moors of Devonshire. 
                Watson accompanies him, documenting every detail of the investigation.
                The atmosphere is thick with fog and mystery.
                Holmes uses his powers of deduction to unravel the truth.
                """,

                'Jane Austen': """
                Pride and Prejudice remains a beloved classic of English literature.
                Elizabeth Bennet is a spirited and intelligent protagonist.
                The novel explores themes of love, class, and social expectations.
                Mr. Darcy initially appears proud and disagreeable.
                Through misunderstandings and revelations, their relationship develops beautifully.
                """
            }

            for author, text in demo_texts.items():
                system.add_author(author, text)

            system.train()
            print("✅ Demo data loaded and model trained!")

        def main():
            system = AuthorshipIdentifier()

            print("\n" + "=" * 60)
            print("  Welcome to Interactive Authorship Identification!")
            print("=" * 60)

            demo = input("\nLoad demo data? (y/n): ").strip().lower()
            if demo == 'y':
                run_demo_mode(system)

            while True:
                print_menu()
                choice = input("Enter your choice (1-9): ").strip()

                if choice == '1':
                    add_author_interactive(system)
                elif choice == '2':
                    train_model_interactive(system)
                elif choice == '3':
                    predict_interactive(system)
                elif choice == '4':
                    view_authors_interactive(system)
                elif choice == '5':
                    remove_author_interactive(system)
                elif choice == '6':
                    save_model_interactive(system)
                elif choice == '7':
                    load_model_interactive(system)
                elif choice == '8':
                    show_status_interactive(system)
                elif choice == '9':
                    print("\n👋 Thanks for using the system! Goodbye!\n")
                    break
                else:
                    print("\n❌ Invalid choice. Please enter 1-9.")

                input("\nPress Enter to continue...")

        if __name__ == "__main__":
            main()