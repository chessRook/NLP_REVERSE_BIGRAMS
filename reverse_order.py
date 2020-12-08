# import string
from matplotlib import pyplot as plt
from pathlib import Path
import datetime

debug = False
results_path = Path(r'.\NLP_backward_bigrams_Results')


def runner():
    dir_name = 'debug' if debug else 'many_text_files'
    text_dir_path = Path(r'.\texts') / dir_name
    forward_dict = dict()
    backward_dict = dict()
    for idx, file_path in enumerate(text_dir_path.iterdir()):
        print(f'{idx}: {file_path}')
        main(file_path, forward_dict, backward_dict)
    make_distributions(forward_dict, backward_dict)
    return 0


def make_distributions(forward_dict, backward_dict):
    forward_masses = calculate_mass_distribution(forward_dict)
    backward_masses = calculate_mass_distribution(backward_dict)
    display_masses(forward_masses, backward_masses)


def display_masses(forward_masses, backward_masses):
    now_results_dir = results_path / f'{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}'
    Path.mkdir(now_results_dir)
    """plt.hist(forward_masses, bins=graph_resolution, color='y')
    plt.title('Forward Mass Distribution')
    plt.show()
    plt.hist(backward_masses, bins=graph_resolution, color='r')
    plt.title('Backward Mass Distribution difference')
    plt.show()
    difference = [backward - forward for forward, backward in zip(forward_masses, backward_masses)]
    plt.hist(difference, bins=graph_resolution, color='m')
    plt.title('Mass Distribution difference')
    plt.show()"""
    difference = [backward / forward for forward, backward in zip(forward_masses, backward_masses)]
    plt.hist(difference, bins=graph_resolution, color='b')
    plt.title('Mass Distribution Ratio')
    plt.savefig(now_results_dir / 'difference.png')
    plt.show()
    print(len(forward_masses))
    print(len(backward_masses))


def main(file_path, forward_dict, backward_dict):
    # r'C:\numerical_checks\texts\debug.txt'
    # file_path = r'.\texts\check_that_runs.txt'
    with open(file_path, encoding='utf8') as text_file:
        text: str = text_file.read()
    # text = text.replace('\n', ' ').replace('\r', '').replace(',', '').replace('.', '').lower()
    # text = text.replace('?', '').replace('!', '')
    # delete_chars = {'\'', '"', '\\', '%', '$', '@'}
    # wanted_chars = list(string.ascii_lowercase)
    # for i in range(10):
    #    delete_chars.add(str(i))
    # for char in delete_chars:
    #    text = text.replace(char, '')
    text = text.lower()
    text = ''.join([single_char if single_char.isalpha() else ' ' for single_char in text])
    while '  ' in text:
        text = text.replace('  ', ' ')
    words = text.strip().split(' ')
    for i in range(1, len(words) - 1):
        add_to_dict(forward_dict, words[i], words[i + 1])
        add_to_dict(backward_dict, words[i], words[i - 1])


counter_key = 'All_appearances_ooooooo'

graph_resolution = 60

number_of_words = 4
no_mass = -9999


def kl_divergence_from_uniform():
    pass


def word_mass(word_dict: dict):
    total = word_dict[counter_key]
    # The distribution of rare words say nothing
    if total < 30:
        return no_mass
    word_dict.pop(counter_key)
    total_keys = len(word_dict.keys())
    frequencies_list = word_dict.values()
    frequencies_list = sorted(frequencies_list, reverse=True)
    effective_word_number = min(total_keys, number_of_words)
    accumulated_mass = sum(frequencies_list[0:effective_word_number]) / total
    return accumulated_mass


def calculate_mass_distribution(bigrams_dict):
    mass_vector = [word_mass(bigrams_dict[word]) for word in bigrams_dict]
    mass_vector = [el for el in mass_vector if el != no_mass]
    sorted_masses = sorted(mass_vector, reverse=True)
    return sorted_masses


def add_to_dict(dict_of_bigs, word_1, word_2):
    if word_1 not in dict_of_bigs:
        dict_of_bigs[word_1] = dict()
        dict_of_bigs[word_1][counter_key] = 0
    if word_2 not in dict_of_bigs[word_1]:
        dict_of_bigs[word_1][word_2] = 0
    dict_of_bigs[word_1][word_2] += 1
    dict_of_bigs[word_1][counter_key] += 1


if __name__ == '__main__':
    runner()
