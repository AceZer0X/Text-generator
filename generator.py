#coding: utf-8
from random import choice


# Вспомогательная функция возвращает список самых вероятных слов, которые могут идти после данных
def wordSuggestion(inputText, bigramCount, trigramCount):
    # Запоминаем два последних слова входной строки
    text = inputText.lower().split()
    givenBigram = (text[-2], text[-1])
    givenBigramCount = bigramCount[givenBigram]

    # Для каждого слова, которое может идти после двух входных слов находим вероятность его выпадения
    probabilities = {}
    for trigram, count in trigramCount.items():
        if (trigram[0], trigram[1]) == givenBigram and trigram[2] not in probabilities.keys():
            # P(слово) = P(данная двуграмма + слово) / P(данная двуграмма)
            probabilities[trigram[2]] = count / givenBigramCount

    return sorted(probabilities.items(), key=lambda x: x[1], reverse=True)[:3]


# Основная функция возвращает готовый сгенерированный текст данной длины
def textGenerate(filename, textLength=100):
    # Загружаем текст из файла, переводя все его элементы в нижний регистр,
    # чтобы избежать одних и тех же слов в разных регистрах
    file = open(filename)
    text = file.read().lower().split()

    # Находим все существующие в тексте двуграммы и триграммы и количество каждой их них
    bigramCount = {}
    trigramCount = {}
    for i in range(len(text)-2):
        currentBigram = (text[i], text[i + 1])
        if currentBigram in bigramCount.keys():
            bigramCount[currentBigram] += 1
        else:
            bigramCount[currentBigram] = 1

        currentTrigram = (text[i], text[i+1], text[i+2])
        if currentTrigram in trigramCount.keys():
            trigramCount[currentTrigram] += 1
        else:
            trigramCount[currentTrigram] = 1

    # Случайно выбираем два первых слова из текста
    chosenBigram = choice(list(bigramCount.keys()))
    outputText = chosenBigram[0] + ' ' + chosenBigram[1]

    # Генерируем одно слово за раз
    for i in range(textLength-2):
        outputText = outputText + ' ' + choice(wordSuggestion(outputText, bigramCount, trigramCount))[0]

    return outputText


print(textGenerate('text.txt', 100))