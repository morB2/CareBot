#include "pch.h"
#include <iostream>
#include <stdio.h>
#include <vector>
#include <string>
#include <locale>
#include <cwchar>
#include <codecvt>
#include <fstream>
#include <sstream>
#include <algorithm>
#include <unordered_map>

using namespace std;
wofstream logFile("log.txt");

// State class definition
class State {
public:
    State();
    State(int i, bool last, bool isDisease, const wstring& n);

    void addTransition(wchar_t value, int destId);
    unordered_map<wchar_t, int> getTransitions() const;
    int getId() const;
    bool getIsLast() const;
    bool getIsDisease() const;
    wstring getName() const;
    void setIsLast(bool last);
    void setIsDiseas(bool disease);
    void setName(const wstring& n);

private:
    int id;
    bool isLast;
    bool isDisease;
    wstring name;
    unordered_map<wchar_t, int> transitions;
};

// Function implementations for State class
void State::addTransition(wchar_t value, int destId) {
    transitions[value] = destId;
}

int State::getId() const {
    return id;
}

bool State::getIsLast() const {
    return isLast;
}

bool State::getIsDisease() const {
    return isDisease;
}

wstring State::getName() const {
    return name;
}

unordered_map<wchar_t, int> State::getTransitions() const {
    return transitions;
}

void State::setIsLast(bool last) {
    isLast = last;
}

void State::setIsDiseas(bool disease) {
    isDisease = disease;
}

void State::setName(const wstring& n) {
    name = n;
}

// Constructors for State class
State::State() : id(-1), isLast(false), isDisease(false) {}

State::State(int i, bool last, bool disease, const wstring& n)
    : id(i), isLast(last), isDisease(disease), name(n) {}

// DFA class definition
class DFA {
public:
    DFA();

    void insert(vector<wstring>& wordList);
    void init(const string& filePath);
    State search(const wstring& word);

private:
    int countOfStates;
    vector<State> states;
};

// Constructor for DFA class
DFA::DFA() : countOfStates(0) {}

// Function to insert words into DFA
void DFA::insert(vector<wstring>& wordList) {
    int indexVector = 0;
    int finalFirstState = 0;
    int prevIndex = 0;
    wstring_convert<codecvt_utf8<wchar_t>, wchar_t> converter;
    unordered_map<wchar_t, int> transitions;
    for (int i = 0; i < wordList.size(); i++) {
        wstring word = wordList.at(i);
        if (word[0] == L'\uFEFF') {
            word.erase(0, 1);
        }
        for (int j = 0; j < word.length(); j++) {
            wchar_t ch = word[j];
            if (indexVector < states.size()) {
                transitions = states.at(indexVector).getTransitions();
            }
            if (indexVector < states.size() && !transitions.empty() && transitions.find(ch) != transitions.end()) {
                indexVector = states.at(indexVector).getTransitions()[ch];
            } else {
                State s(countOfStates++, false, false, L"");
                states.push_back(s);
                prevIndex = indexVector;
                j == word.length() - 1 && i != 0 ? indexVector = finalFirstState : indexVector = states.size();
                states.at(prevIndex).addTransition(ch, indexVector);
            }
        }
        if (i == 0) {
            finalFirstState = indexVector;
            State s(countOfStates++, true, stoi(converter.to_bytes(wordList.at(1))), word);
            states.push_back(s);
            i++;
        }
        states.at(prevIndex).setIsLast(true);
        indexVector = 0;
        prevIndex = 0;
    }
}

// Function to initialize DFA from CSV file
void DFA::init(const string& filePath) {
    wifstream file(filePath);
    if (!file.is_open()) {
        return;
    }
    wstring line;
    wchar_t delimiter = L',';
    file.imbue(locale(locale(), new codecvt_utf8<wchar_t>));

    while (getline(file, line)) {
        wistringstream iss(line);
        vector<wstring> words;
        wstring word;
        while (getline(iss, word, delimiter)) {
            words.push_back(word);
        }
        insert(words);
    }
}

// Function to search a word in the DFA
State DFA::search(const wstring& word) {
    logFile.imbue(locale(locale(), new codecvt_utf8<wchar_t>));

    int currentStateIndex = 0;
    int i = 0;
    wchar_t ch;
    State state;
    unordered_map<wchar_t, int> transitions;
    for (; i < word.length(); i++) {
        ch = word[i];
        transitions = states.at(currentStateIndex).getTransitions();
        if (transitions.find(ch) == transitions.end()) {
            return state;
        }
        currentStateIndex = transitions[ch];
    }
    if (i < word.length() || !states[currentStateIndex].getIsLast()) {
        return state;
    }
    if (states[currentStateIndex].getIsLast() && states[currentStateIndex].getName() != L"") {
        return states[currentStateIndex];
    }
    return states.at(++currentStateIndex);
}

// Function to load phrases from CSV file
unordered_map<wstring, wstring> loadPhrases(const string& filename) {
    unordered_map<wstring, wstring> phrases;
    wifstream file(filename);
    if (!file.is_open()) {
        return phrases;
    }

    wstring line;
    wstring word;
    wstring secWord;
    wchar_t delimiter = L',';
    file.imbue(locale(locale(), new codecvt_utf8<wchar_t>));
    while (getline(file, line)) {
        wistringstream iss(line);
        getline(iss, word, delimiter);
        if (word[0] == L'\uFEFF') {
            word.erase(0, 1);
        }
        getline(iss, secWord, delimiter);
        phrases[word] = secWord;
    }
    return phrases;
}

// Function to hash states
vector<State> hashStates(const vector<State>& states) {
    logFile << states.size() << endl;

    vector<State> finalStates;
    unordered_map<wstring, wstring> phrases = loadPhrases("C:\\Users\\morb9\\Desktop\\סמסטר ב שנה ב פרויקטים\\פרויקט שנתי משרד החינוך\\server\\dfa2\\phrases.csv");

    for (size_t i = 0; i < states.size(); i++) {
        wstring name_1 = states[i].getName();
        wstring name_2 = (i + 1 < states.size()) ? states[i + 1].getName() : L"";
        wstring fullName = name_1 + L" " + name_2;
        if (phrases.count(fullName)) {
            int isDisease = states[i].getIsDisease() != states[i + 1].getIsDisease() ? 1 : states[i].getIsDisease();
            State newState(states[i + 1].getId(), true, isDisease, phrases[fullName]);
            finalStates.push_back(newState);
            i++;
        } else if (phrases[states[i].getName()] != L"-1") {
            State newState(states[i].getId(), true, states[i].getIsDisease(), phrases[states[i].getName()]);
            finalStates.push_back(newState);
        }
        if (phrases[states[i].getName()] != L"-1" && finalStates.at(finalStates.size() - 1).getIsDisease()) {
            State newState = finalStates.at(finalStates.size() - 1);
            finalStates.clear();
            finalStates.push_back(newState);
            return finalStates;
        }
    }
    return finalStates;
}

// Function to convert char** to vector<wstring>
vector<wstring> convertToWStringVector(char** inputWords, int size) {
    vector<wstring> wstringVector;
    wstring_convert<codecvt_utf8_utf16<wchar_t>> converter;

    for (int i = 0; i < size; ++i) {
        wstring wideString = converter.from_bytes(inputWords[i]);
        wstringVector.push_back(wideString);
    }

    return wstringVector;
}

// Structure to represent state in C-style
struct CState {
    int id;
    bool isLast;
    bool isDisease;
    wchar_t name[100];
};

// Function to recognize words and return states
extern "C" {
    __declspec(dllexport) void recognizeWords(char** inputWords, int wordCount, CState* outputStates) {
        try {
            vector<wstring> inputArray = convertToWStringVector(inputWords, wordCount);

            DFA dfa;
            wstring word;

            dfa.init("C:\\Users\\morb9\\Desktop\\סמסטר ב שנה ב פרויקטים\\פרויקט שנתי משרד החינוך\\server\\dfa2\\dfa_init.csv");

            vector<State> recognizedStates;
            for (wstring word : inputArray) {
                State state = dfa.search(word);
                if (state.getId() != -1) {
                    recognizedStates.push_back(state);
                }
            }

            vector<State> finalStates = hashStates(recognizedStates);

            for (size_t i = 0; i < finalStates.size(); ++i) {
                outputStates[i].id = finalStates[i].getId();
                outputStates[i].isLast = finalStates[i].getIsLast();
                outputStates[i].isDisease = finalStates[i].getIsDisease();
                wcsncpy_s(outputStates[i].name, finalStates[i].getName().c_str(), _TRUNCATE);
            }
        } catch (const exception& e) {
            logFile << "Exception caught: " << e.what() << endl;
        }
    }
}
