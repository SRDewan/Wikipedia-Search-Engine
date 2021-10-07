# Wikipedia-Search-Engine
Search engine for wikipedia data dump.

# To Do
1. Fix references parsing for reflist.
2. Try creating own list of stop words using a program.
3. Try Porter stemmer and lemitization.
4. For index format, could try 1 line per field per word instead of per doc per word.
5. Try multiprocessing and/or threading to speed up.
6. Remove other field data from body to reduce mem and speed up.

# How To Run The Code

Run the following commands:
```
pip install -r requirements.txt
bash index.sh <path_to_wiki_dump> <path_to_inverted_index> invertedindex_stat.txt
bash search.sh <path_to_inverted_index> <path_to_queries_file>
```

Note that for the query strings, it has been assumed that there will be no spaces before and after the ':' for field queries. Any such cases will be treated as regular (non field) queries.
The search results are stored in a file 'queries_op.txt' along with the time it took to run the search for each query.
