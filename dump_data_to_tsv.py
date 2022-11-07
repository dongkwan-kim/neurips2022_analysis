import pickle


with open("data/pp_authors.txt", "rb") as fp:  # Unpickling
    pp_authors = pickle.load(fp)

with open("data/pp_names.txt", "rb") as fp:  # Unpickling
    pp_names = pickle.load(fp)

author_and_aff_list_full = []
for pp, paper in zip(pp_authors, pp_names):
    author_and_aff_list_full += [
        (author[:author.find("(")].strip(),
         author[author.find("(") + 1: author.find("')")].lower())
        for author in pp
    ]
author_and_aff_list_full = set(author_and_aff_list_full)

title_and_author_list_full = []
title_and_aff_list_full = []
for pp, paper in zip(pp_authors, pp_names):
    title_and_author_list_full.append(
        tuple([paper] + [author[:author.find("(")].strip() for author in pp])
    )
    title_and_aff_list_full.append(
        tuple([paper] + [author[author.find("(") + 1: author.find("')")].lower() for author in pp])
    )

with open("data/neurips_2022_author_and_aff.tsv", "w") as fp:
    for line in author_and_aff_list_full:
        fp.write("\t".join(line) + "\n")

with open("data/neurips_2022_title_and_authors.tsv", "w") as fp:
    for line in title_and_author_list_full:
        fp.write("\t".join(line) + "\n")

with open("data/neurips_2022_title_and_aff.tsv", "w") as fp:
    for line in title_and_aff_list_full:
        fp.write("\t".join(line) + "\n")

