// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>

#include <stdio.h>
#include <string.h>
#include <strings.h>
#include <stdlib.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 28;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    unsigned int index = hash(word);
    node *current = table[index];
    
    while (current != NULL) {
        if (strcasecmp(word, current->word) == 0) {
            return true;
        }
        current = current->next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // Hash word to a number
    unsigned int hash = 0;
    for (int i = 0; word[i] != '\0'; i++) {
        hash += toupper(word[i]) - 'A';
    }
    hash = hash % N;
    return hash;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO
    FILE *fp = fopen(dictionary, "r");
    if (fp == NULL) {
        return false;
    }
    for (int i = 0; i < N; i++) {
        table[i] = 0;
    }
    while (!feof(fp)) {
        char word[LENGTH + 1];
        fscanf(fp, "%s", word);
        if (check(word)) {
            continue;
        }
        node *new_node = malloc(sizeof(node));
        strcpy(new_node->word, word);
        new_node->next = table[hash(word)];
        table[hash(word)] = new_node;
    }
    fclose(fp);
    return true;
    
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    unsigned int size = 0;
    for (int i = 0; i < N; i++) {
        node *current = table[i];
        while (current != 0) {
            size++;
            current = current->next;
        }
    }
    return size;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    for (int i = 0; i < N; i++) {
        node *current = table[i];
        while (current != 0) {
            node *next = current->next;
            free(current);
            current = next;
        }
    }
    return true;
}
