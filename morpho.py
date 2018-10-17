import random
import time
import sys


def create_database(text_file, num):
    with open(text_file, 'r') as f:
        words = f.read().splitlines()  # words:109581
    data = random.sample(words, int(num))
    data.sort()
    return data


def get_prefixes(sample):
    prefix_dict = {}
    # pair-wise comparison of prefixes
    for i, word1 in enumerate(sample):
        for word2 in sample[i+1:]:
            # check prefix
            if word1[0] == word2[0]:
                pre = word1[0]
                z = 1
                while word1[z] == word2[z]:
                    pre = pre + word1[z]
                    z += 1
                    # break the loop if you finish the word
                    if z == len(word1) or z == len(word2):
                        break
                    # add prefix to the list, but leave out those made of a single letter
                if pre not in prefix_dict and len(pre) > 1:
                    prefix_dict[pre] = 1
                elif pre in prefix_dict and len(pre) > 1:
                    prefix_dict[pre] += 1
            else:
                break
            # weight prefixes
    for prefix in prefix_dict:
        prefix_dict[prefix] *= (len(prefix)-1) ** 3
    pre_list = [(w,prefix_dict[w]) for w in sorted(prefix_dict, key=prefix_dict.get, reverse=True)]
    return pre_list[:20]


def get_suffixes(sample):
    suffix_dict = {}
    # pair-wise comparison of prefixes
    for i, word1 in enumerate(sample):
        for word2 in sample[i+1:]:
            # check suffix
            if word1[-1] == word2[-1]:
                suf = word1[-1]
                z = -2
                while word1[z] == word2[z]:
                    suf = word1[z] + suf
                    z -= 1
                    # break the loop if you finish the word
                    if abs(z) >= len(word1) or abs(z) >= len(word2):
                        break
                # add suffix to the list, but leave out those made of a single letter
                if suf not in suffix_dict and len(suf) > 1:
                    suffix_dict[suf] = 1
                elif suf in suffix_dict and len(suf) > 1:
                    suffix_dict[suf] += 1
    # weight prefixes
    for suffix in suffix_dict:
        suffix_dict[suffix] *= (len(suffix)-1) ** 2
        if suffix[-1] == 's':
            suffix_dict[suffix] /= 2
    suff_list = [(w, suffix_dict[w]) for w in sorted(suffix_dict, key=suffix_dict.get, reverse=True)]
    updated_suff_list = remove_noise_suffixes(suff_list[:100])
    return updated_suff_list[:20]


def remove_noise_suffixes(suff_list):
    # this takes just a list of suffix, frequency tuples
    # remove suffixes where there is a shorter suffix in the current one
    remove = set()
    for i, s1 in enumerate(suff_list):
        for s2 in suff_list[i+1:]:
            # check if suffix is either in the beginning or in the end (so you can check *ed---*ted but not *es--*ness)
            if s2[0].endswith(s1[0]) or s2[0].startswith(s1[0]):
                    remove.add(s2)
    remove = list(remove)
    for word in remove:
        suff_list.remove(word)
    return suff_list


def morpho(sample):

    # get a list containing the prefixes
    pre_list = get_prefixes(sample)
    prefixes = [tup[0] for tup in pre_list]

    # get a list containing the suffixes
    suf_list = get_suffixes(sample)
    suffixes = [tup[0] for tup in suf_list]


    # build a root list in which the prefixes are removed
    root_list_partial = []
    for word in sample:
        for pre in prefixes:
            if pre in word and pre[:2] == word[:2]:
                root = word[len(pre):]
                if root in sample:
                    root_list_partial.append(root)
                    
    # build a root list in which both the prefixes and the suffixes are removed
    root_list_final = []
    with open('wordsEn.txt', 'r') as f:
        words = f.read().splitlines()
    for word in root_list_partial:
        for suf in suffixes:
            if suf in word and suf[-2:] == word[-2:]:
                root = word[:(len(word)-len(suf))]
                # correct final -e
                if root in words:
                    root_list_final.append(root)
                if root + 'e' in words:
                    root_list_final.append(root + 'e')
                    
    # correct -i in -y
    word_to_correct = []
    corrected_word = []
    for word in root_list_final:
        if len(word) >= 1:
            if word[-1] == 'i':
                word_to_correct.append(word)
                corrected_word.append(word.replace(word[-1], 'y'))
    for word in corrected_word:
            root_list_final.append(word)
    for word in word_to_correct:
        root_list_final.remove(word)

    # create a dictionary of roots by frequency
    root_dictionary = {word:root_list_final.count(word) for word in root_list_final}
        
    # sort dictionary by frequency
    root_list = [(w, root_dictionary[w]) for w in sorted(root_dictionary, key=root_dictionary.get, reverse=True)]
        
    # print prefixes, suffixes and the beginning of the sample and the root list
    print('PREFIXES', '\n', pre_list, '\n', '\n', 'SUFFIXES', '\n', suf_list, '\n', '\n', 'ROOTS', '\n', root_list[:100])
    return pre_list, suf_list, root_list
                

if __name__ == '__main__':

    start_time = time.time()
    suffixes, prefixes, roots = morpho(create_database(sys.argv[1], sys.argv[2]))

    print("--- %s seconds ---" % (time.time() - start_time))
