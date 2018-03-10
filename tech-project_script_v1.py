from bs4 import BeautifulSoup
import hfst
import random
import sys


# Parse word list XML file with BeautifulSoup
print("Parsing XML file...")
with open('kotus_sanalista/kotus-sanalista_v1.xml') as fp:
    soup = BeautifulSoup(fp, 'lxml')

# Read all word entries directly into a variable; the resulting
# bs4.element.ResultSet object can be manipulated like a list
print("Listing word entries...")
word_entries = soup.find_all('st')

print("Picking words with desired inflection paradigms...")
random_entries = []
for entry in word_entries:
    if entry.t is not None and int(entry.t.tn.string) == 1:
        random_entries.append(entry)

# Pick 100 word entries at random
random_entries = random.choices(random_entries, k=50)


nouns = {}
verbs = {}
other = {}

print("Composing word entries...")

for word_entry in random_entries:
    word = word_entry.s.string.replace(' ', '_')
    infl_paradigm = ''
    grad_paradigm = ''
    if word_entry.t is not None and int(word_entry.t.tn.string) < 52:
        infl_paradigm = word_entry.t.tn.string
        if word_entry.av is not None:
            grad_paradigm = word_entry.av.string
        nouns[word] = (infl_paradigm, grad_paradigm)
    # elif word_entry.t is not None and int(word_entry.t.tn.string) < 77:
    #     infl_paradigm = word_entry.t.tn.string
    #     if word_entry.av is not None:
    #         grad_paradigm = word_entry.av.string
    #     verbs[word] = (infl_paradigm, grad_paradigm)
    # else:
    #     other[word] = (infl_paradigm, grad_paradigm)

multichar_symbols = ''
multichar_set = ['+Nom', '+Gen', '+Part',
                 '+Ine', '+Ela', '+Ill',
                 '+Ade', '+Abl', '+All',
                 '+Ess', '+Tra']

for item in multichar_set:
    multichar_symbols += item + '\n\t'

continuation_lexica = []

print("Writing lexc file...")
fp = open('temp.lexc', 'w')

fp.write('Multichar_Symbols\n\t{}\n'.format(multichar_symbols))
fp.write('\nLEXICON Root\n\tNouns ;\n\tVerbs ;\n\tOther ;')
fp.write('\n\nLEXICON Nouns\n\n')
for word in nouns.items():
    next_lexicon = 'N{}{}'.format(word[1][0], word[1][1])
    if next_lexicon not in continuation_lexica:
        continuation_lexica.append(next_lexicon)
    fp.write('{}\t\t\t{} ;'.format(str(word[0]), next_lexicon))
    fp.write('\n')

# fp.write('\n\nLEXICON Verbs\n\n')
# for word in verbs.items():
#     next_lexicon = 'V{}{}'.format(word[1][0], word[1][1])
#     if next_lexicon not in continuation_lexica:
#         continuation_lexica.append(next_lexicon)
#     fp.write('{}\t\t\t{} ;'.format(str(word[0]), next_lexicon))
#     fp.write('\n')

# fp.write('\n\nLEXICON Other\n\n')
# for word in other.items():
#     fp.write('{}\t\t\tN ;'.format(str(word[0])))
#     fp.write('\n')

sorted_lexica = sorted(continuation_lexica)

fp.write('\n\n')
for item in sorted_lexica:
    fp.write('\nLEXICON {}\n'.format(item))
    fp.write('\t\tCase ;')
    fp.write('\n')

fp.write('\n\n')
fp.write('\nLEXICON Case\n')
fp.write('\n+Nom:0\t\t # ;')
fp.write('\n+Gen:n\t\t # ;')
fp.write('\n+Part:A')
fp.write('\t\t# ;')

# fp.write('\n\nEND')
fp.close()

# Set default FST type to FOMA
# hfst.set_default_fst_type(hfst.ImplementationType.FOMA_TYPE)

print("Compiling transducer from lexc file...")
# Compile transducer from lexc file
tr = hfst.compile_lexc_file('temp.lexc', output=sys.stderr)
tr.invert()
# tr.convert(hfst.ImplementationType.HFST_OL_TYPE)

paths = tr.input_project()
for item in paths:
    print(item)

# for inputs, outputs in paths.items():
#     print('{}:'.format(inputs))
#     for output in outputs:
#         print('\t{}'.format(output[0]))
