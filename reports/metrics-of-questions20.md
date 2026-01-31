## Набор данных
Использован файл `test/questions20.yaml`

## Использованная метрика и модель
- DeepEval
  - ContextualPrecisionMetric
  - LLMTestCase

- LLM для оценки 
  - gemma3 (через Ollama)

## Результаты
| Показатель                   | Значение          |
| ---------------------------- |-------------------|
| Количество вопросов          | 20                |
| Средний Contextual Precision | **≈ 0.975**       |
| Минимальный score            | **0.81**          |
| Максимальный score           | **1.00**          |
| Вопросы с score = 1.0        | **16 / 20 (80%)** |

## Анализ
Высокий средний `Contextual Precision` `(≈ 0.96)` свидетельствует о хорошем качестве источников данных

Снижение `score` в отдельных вопросах обусловлено тематическим пересечением нормативных документов и избыточной информацией в отдельных чанках.

## Возникшие трудности
При использовании deepeval интеграции с haystack наблюдались таймауты (RetryError). Предполагается, что это из-за попытки параллельного обращения к Ollama.

Проблема была решена за счет отключения async-режима и последовательной обработки вопросов путем использования DeepEval напрямую (`LLMTestCase`).

## Полный вывод программы:
```
Evaluating question 1/20

✅ Score: 1.000
🧠 Reason: The score is 1.00 because all retrieval contexts are ranked appropriately, with the most relevant nodes – such as the first node stating 'document, удостоверяющий личность и гражданство' and 'document об образовании' – consistently receiving 'yes' judgments. The ranking ensures that the crucial information about required documents is prioritized, effectively addressing the input question.

Evaluating question 2/20

✅ Score: 0.854
🧠 Reason: The score is 0.85 because the top retrieval contexts (nodes 1, 2, 4, and 6) consistently provide relevant information about admission deadlines and schedules for the Financial University, directly addressing the input question. While node 3 and node 5 are marked as 'no', their explanations highlight irrelevant aspects of the university's programs and procedures, which explains why they are ranked lower. The contextual precision is high because the most pertinent nodes are prioritized, ensuring the system effectively retrieves the desired information about the specific deadlines.

Evaluating question 3/20
✅ Score: 1.000
🧠 Reason: The score is 1.00 because the first and second retrieval contexts nodes provide relevant information directly answering the question, while the third node, a retrieval context node, offers irrelevant details about the application process. The ranking of the relevant nodes ensures high contextual precision.


Evaluating question 4/20
✅ Score: 0.917
🧠 Reason: The score is 0.92 because the top three retrieval contexts – nodes 1, 2, and 4 – successfully identify relevant information about entrance tests, including ЕГЭ results and potential additional tests, while the lower-ranked nodes (nodes 5 and 6) contain irrelevant information about general admission processes and Einstein's Nobel Prize, preventing a higher score.


Evaluating question 5/20

✅ Score: 1.000
🧠 Reason: The score is 1.00 because the first two retrieval contexts nodes, ranked 1 and 2, both provide direct answers to the input question, specifically stating the minimum passing scores for each subject. The third node, ranked 3, is irrelevant as it discusses admissions to the Financial University and does not contain the requested information about passing scores.

Evaluating question 6/20

✅ Score: 1.000
🧠 Reason: The score is 1.00 because the retrieval contexts successfully rank the relevant nodes higher than the irrelevant nodes. Specifically, the first node, which states: 'Целевое обучение может быть предусмотрено.', and the second node, which details the step-by-step process for obtaining target training, are ranked highest and provide direct answers to the input question. The third node reinforces this information. The fourth and fifth nodes, which discuss the 'Работа в России' platform and the specifics of the program, are ranked lower and provide tangential details, ensuring the most pertinent information is prioritized.

Evaluating question 7/20

✅ Score: 1.000
🧠 Reason: The score is 1.00 because the retrieval contexts successfully rank the relevant nodes higher. Specifically, the first node, which states 'Количество бюджетных мест на бакалавриат (очная форма обучения, г. Москва) За счет средств федерального бюджета - 117. По договорам об образовании - 83.', directly answers the input question, and the second node confirms this information. The third node, stating 'специалитета); на места в пределах отдельной квоты (по программам бакалавриата и программам специалитета); на основные бюджетные места', is irrelevant to the specific question about the number of budget places.

Evaluating question 8/20

✅ Score: 1.000
🧠 Reason: The score is 1.00 because the first two retrieval contexts nodes ('The text states...' and 'The text confirms...') provide highly relevant information about the cost of education and discounts, while the third node ('The provided context...') offers irrelevant details about the admission process. This prioritization ensures that the most pertinent nodes are ranked highest.

Evaluating question 9/20
✅ Score: 1.000
🧠 Reason: The score is 1.00 because the first three retrieval contexts, ranked highest, all accurately address the input question about online document submission, providing direct instructions and methods. The remaining nodes, ranked lower, contain irrelevant information about enrollment quotas, internal exams, and foreign student requirements, which explains why they are not ranked higher and contribute to the high contextual precision score.


Evaluating question 10/20
✅ Score: 1.000
🧠 Reason: The score is 1.00 because all retrieval contexts are highly relevant. The first node directly answers the question, the second provides a timeframe, the third directs the user to find precise dates, and the fourth node acknowledges the absence of specific dates while still offering helpful guidance. This demonstrates a perfect alignment of relevant nodes with the input query.


Evaluating question 11/20

✅ Score: 1.000
🧠 Reason: The score is 1.00 because the retrieval contexts successfully rank relevant nodes higher than irrelevant ones. Specifically, the first node, which states "Подготовительные курсы могут быть организованы вузом.", is correctly identified as relevant, and the subsequent nodes, despite containing related information about admissions, are ranked lower due to the 'no' verdicts and their focus on unrelated aspects like admissions procedures and scholarship criteria. The text clearly provides information about preparatory courses, and the ranking of the relevant nodes ensures precision.

Evaluating question 12/20

✅ Score: 1.000
🧠 Reason: The score is 1.00 because all relevant nodes in the retrieval contexts – nodes 1, 2, and 3 – provide affirmative answers to the question about hostel availability for foreign students. Specifically, nodes 1 and 2 directly confirm hostel provision, while node 3 details the process for applying. The final node, ranked lower, discusses admission documents and doesn't address the core query about hostel access.

Evaluating question 13/20

✅ Score: 0.917
🧠 Reason: The score is 0.92 because the top nodes (1, 2, and 3) consistently provide highly relevant information about benefits and rights for students, including details on Olympiads, disability status, and legal regulations. While nodes 4, 5, and 6 are irrelevant, they are ranked lower than the key nodes, preventing a higher score. The inclusion of the university's admission rules website as a reference in node 5 is a helpful detail, but it doesn't fully address the core question about specific benefits and rights.

Evaluating question 14/20

✅ Score: 0.810
🧠 Reason: The score is 0.81 because the first three retrieval contexts, containing nodes with 'yes' verdicts, accurately address the core question about transferring from paid to budget education. These nodes provide relevant information about the possibility of transfer and the conditions required. However, the remaining nodes, ranked lower, contain irrelevant information such as acceptance withdrawal procedures or admission quotas, which detract from the precision of the retrieval context. Specifically, nodes 3, 4, 5, and 10 contain statements that are not directly related to the transfer process, thus lowering the score.

Evaluating question 15/20

✅ Score: 1.000
🧠 Reason: The score is 1.00 because the first and second retrieval contexts, containing nodes with 'yes' responses, are ranked higher than the third node with a 'no' response. The first node states, "Наличие заочной или очно‑заочной формы обучения зависит от направления подготовки.", and the second node provides information about remote/part-time study options, effectively addressing the input question. The third node, while relevant to the broader topic of admissions, does not directly answer the question about studying remotely/part-time.

Evaluating question 16/20

✅ Score: 1.000
🧠 Reason: The score is 1.00 because the first node provides a direct answer to the user's question about program durations, while the second node elaborates on this information with specific timeframes for each program type, and the third node discusses irrelevant admission details. The ranking of the relevant nodes ensures high contextual precision.

Evaluating question 17/20

✅ Score: 1.000
🧠 Reason: The score is 1.00 because the first node, stating "Наличие военной кафедры зависит от вуза…", directly answers the question and confirms the existence of a military department, while the subsequent nodes provide irrelevant details about university admissions and the 'Работа в России' platform. The ranking of the relevant node is appropriately high, ensuring accurate retrieval.

Evaluating question 18/20
✅ Score: 1.000
🧠 Reason: The score is 1.00 because all the retrieval contexts are ranked correctly, with the relevant nodes (nodes 1, 2, 3, and 6) consistently receiving 'yes' judgments. The irrelevant nodes (nodes 4, 5, 7, and 8) contain information about university regulations, program details, and enrollment numbers, which are clearly not related to the input question about internship and employment opportunities, ensuring a high level of precision.


Evaluating question 19/20
✅ Score: 1.000
🧠 Reason: The score is 1.00 because all retrieval contexts are highly relevant and ranked appropriately. Each node, including node 1, provides direct and affirmative answers to the question, stating that changes to the chosen direction are possible after submitting the application, as evidenced by the phrases 'можно внести изменения' and 'поменять направления' within the nodes' reasons.


Evaluating question 20/20

✅ Score: 1.000
🧠 Reason: The contextual precision score is 1.00 because the first three retrieval contexts (ranked 1, 2, and 3) all correctly identify relevant nodes – providing information about where to find academic plans and entrance exam programs. The remaining nodes, while present in the context, offer irrelevant details about admissions procedures, document translation, verification processes, or student file creation, thus ensuring that the most pertinent information is ranked highest.

================================================================================
FINAL RESULTS
================================================================================
──────────────────────────────────────────────────
Question: Какие документы необходимы для подачи заявления на поступление?
Result: {'question': 'Какие документы необходимы для подачи заявления на поступление?', 'score': 1.0, 'reason': "The score is 1.00 because all retrieval contexts are ranked appropriately, with the most relevant nodes – such as the first node stating 'document, удостоверяющий личность и гражданство' and 'document об образовании' – consistently receiving 'yes' judgments. The ranking ensures that the crucial information about required documents is prioritized, effectively addressing the input question."}
──────────────────────────────────────────────────
Question: Каковы сроки приёма документов в этом году?
Result: {'question': 'Каковы сроки приёма документов в этом году?', 'score': 0.8541666666666666, 'reason': "The score is 0.85 because the top retrieval contexts (nodes 1, 2, 4, and 6) consistently provide relevant information about admission deadlines and schedules for the Financial University, directly addressing the input question. While node 3 and node 5 are marked as 'no', their explanations highlight irrelevant aspects of the university's programs and procedures, which explains why they are ranked lower. The contextual precision is high because the most pertinent nodes are prioritized, ensuring the system effectively retrieves the desired information about the specific deadlines."}
──────────────────────────────────────────────────
Question: Сколько направлений (специальностей) можно выбрать при подаче заявления?
Result: {'question': 'Сколько направлений (специальностей) можно выбрать при подаче заявления?', 'score': 1.0, 'reason': 'The score is 1.00 because the first and second retrieval contexts nodes provide relevant information directly answering the question, while the third node, a retrieval context node, offers irrelevant details about the application process. The ranking of the relevant nodes ensures high contextual precision.'}
──────────────────────────────────────────────────
Question: Какие вступительные испытания нужно пройти (ЕГЭ, дополнительные экзамены)?
Result: {'question': 'Какие вступительные испытания нужно пройти (ЕГЭ, дополнительные экзамены)?', 'score': 0.9166666666666666, 'reason': "The score is 0.92 because the top three retrieval contexts – nodes 1, 2, and 4 – successfully identify relevant information about entrance tests, including ЕГЭ results and potential additional tests, while the lower-ranked nodes (nodes 5 and 6) contain irrelevant information about general admission processes and Einstein's Nobel Prize, preventing a higher score."}
──────────────────────────────────────────────────
Question: Каков минимальный проходной балл по каждому предмету?
Result: {'question': 'Каков минимальный проходной балл по каждому предмету?', 'score': 1.0, 'reason': 'The score is 1.00 because the first two retrieval contexts nodes, ranked 1 and 2, both provide direct answers to the input question, specifically stating the minimum passing scores for each subject. The third node, ranked 3, is irrelevant as it discusses admissions to the Financial University and does not contain the requested information about passing scores.'}
──────────────────────────────────────────────────
Question: Есть ли в университете целевое обучение и как его получить?
Result: {'question': 'Есть ли в университете целевое обучение и как его получить?', 'score': 1.0, 'reason': "The score is 1.00 because the retrieval contexts successfully rank the relevant nodes higher than the irrelevant nodes. Specifically, the first node, which states: 'Целевое обучение может быть предусмотрено.', and the second node, which details the step-by-step process for obtaining target training, are ranked highest and provide direct answers to the input question. The third node reinforces this information. The fourth and fifth nodes, which discuss the 'Работа в России' platform and the specifics of the program, are ranked lower and provide tangential details, ensuring the most pertinent information is prioritized."}
──────────────────────────────────────────────────
Question: Сколько бюджетных мест выделено на направлении Прикладное машинное обучение?
Result: {'question': 'Сколько бюджетных мест выделено на направлении Прикладное машинное обучение?', 'score': 1.0, 'reason': "The score is 1.00 because the retrieval contexts successfully rank the relevant nodes higher. Specifically, the first node, which states 'Количество бюджетных мест на бакалавриат (очная форма обучения, г. Москва) За счет средств федерального бюджета - 117. По договорам об образовании - 83.', directly answers the input question, and the second node confirms this information. The third node, stating 'специалитета); на места в пределах отдельной квоты (по программам бакалавриата и программам специалитета); на основные бюджетные места', is irrelevant to the specific question about the number of budget places."}
──────────────────────────────────────────────────
Question: Какова стоимость обучения и есть ли скидки?
Result: {'question': 'Какова стоимость обучения и есть ли скидки?', 'score': 1.0, 'reason': "The score is 1.00 because the first two retrieval contexts nodes ('The text states...' and 'The text confirms...') provide highly relevant information about the cost of education and discounts, while the third node ('The provided context...') offers irrelevant details about the admission process. This prioritization ensures that the most pertinent nodes are ranked highest."}
──────────────────────────────────────────────────
Question: Можно ли подать документы онлайн, и как это сделать?
Result: {'question': 'Можно ли подать документы онлайн, и как это сделать?', 'score': 1.0, 'reason': 'The score is 1.00 because the first three retrieval contexts, ranked highest, all accurately address the input question about online document submission, providing direct instructions and methods. The remaining nodes, ranked lower, contain irrelevant information about enrollment quotas, internal exams, and foreign student requirements, which explains why they are not ranked higher and contribute to the high contextual precision score.'}
──────────────────────────────────────────────────
Question: Когда будут опубликованы конкурсные списки и приказы о зачислении?
Result: {'question': 'Когда будут опубликованы конкурсные списки и приказы о зачислении?', 'score': 1.0, 'reason': 'The score is 1.00 because all retrieval contexts are highly relevant. The first node directly answers the question, the second provides a timeframe, the third directs the user to find precise dates, and the fourth node acknowledges the absence of specific dates while still offering helpful guidance. This demonstrates a perfect alignment of relevant nodes with the input query.'}
──────────────────────────────────────────────────
Question: Есть ли подготовительные курсы для абитуриентов и сколько они стоят?
Result: {'question': 'Есть ли подготовительные курсы для абитуриентов и сколько они стоят?', 'score': 1.0, 'reason': 'The score is 1.00 because the retrieval contexts successfully rank relevant nodes higher than irrelevant ones. Specifically, the first node, which states "Подготовительные курсы могут быть организованы вузом.", is correctly identified as relevant, and the subsequent nodes, despite containing related information about admissions, are ranked lower due to the \'no\' verdicts and their focus on unrelated aspects like admissions procedures and scholarship criteria. The text clearly provides information about preparatory courses, and the ranking of the relevant nodes ensures precision.'}
──────────────────────────────────────────────────
Question: Предоставляется ли общежитие иногородним студентам?
Result: {'question': 'Предоставляется ли общежитие иногородним студентам?', 'score': 1.0, 'reason': "The score is 1.00 because all relevant nodes in the retrieval contexts – nodes 1, 2, and 3 – provide affirmative answers to the question about hostel availability for foreign students. Specifically, nodes 1 and 2 directly confirm hostel provision, while node 3 details the process for applying. The final node, ranked lower, discusses admission documents and doesn't address the core query about hostel access."}
──────────────────────────────────────────────────
Question: Какие льготы и особые права при поступлении предусмотрены (олимпиады, инвалидность и т. д.)?
Result: {'question': 'Какие льготы и особые права при поступлении предусмотрены (олимпиады, инвалидность и т.\xa0д.)?', 'score': 0.9166666666666666, 'reason': "The score is 0.92 because the top nodes (1, 2, and 3) consistently provide highly relevant information about benefits and rights for students, including details on Olympiads, disability status, and legal regulations. While nodes 4, 5, and 6 are irrelevant, they are ranked lower than the key nodes, preventing a higher score. The inclusion of the university's admission rules website as a reference in node 5 is a helpful detail, but it doesn't fully address the core question about specific benefits and rights."}
──────────────────────────────────────────────────
Question: Можно ли перевестись с платного обучения на бюджетное?
Result: {'question': 'Можно ли перевестись с платного обучения на бюджетное?', 'score': 0.8095238095238094, 'reason': "The score is 0.81 because the first three retrieval contexts, containing nodes with 'yes' verdicts, accurately address the core question about transferring from paid to budget education. These nodes provide relevant information about the possibility of transfer and the conditions required. However, the remaining nodes, ranked lower, contain irrelevant information such as acceptance withdrawal procedures or admission quotas, which detract from the precision of the retrieval context. Specifically, nodes 3, 4, 5, and 10 contain statements that are not directly related to the transfer process, thus lowering the score."}
──────────────────────────────────────────────────
Question: Есть ли возможность учиться заочно/очно‑заочно на выбранной специальности?
Result: {'question': 'Есть ли возможность учиться заочно/очно‑заочно на выбранной специальности?', 'score': 1.0, 'reason': 'The score is 1.00 because the first and second retrieval contexts, containing nodes with \'yes\' responses, are ranked higher than the third node with a \'no\' response. The first node states, "Наличие заочной или очно‑заочной формы обучения зависит от направления подготовки.", and the second node provides information about remote/part-time study options, effectively addressing the input question. The third node, while relevant to the broader topic of admissions, does not directly answer the question about studying remotely/part-time.'}
──────────────────────────────────────────────────
Question: Какова продолжительность обучения по моей программе (бакалавриат/специалитет/магистратура)?
Result: {'question': 'Какова продолжительность обучения по моей программе (бакалавриат/специалитет/магистратура)?', 'score': 1.0, 'reason': "The score is 1.00 because the first node provides a direct answer to the user's question about program durations, while the second node elaborates on this information with specific timeframes for each program type, and the third node discusses irrelevant admission details. The ranking of the relevant nodes ensures high contextual precision."}
──────────────────────────────────────────────────
Question: Есть ли военная кафедра в университете?
Result: {'question': 'Есть ли военная кафедра в университете?', 'score': 1.0, 'reason': 'The score is 1.00 because the first node, stating "Наличие военной кафедры зависит от вуза…", directly answers the question and confirms the existence of a military department, while the subsequent nodes provide irrelevant details about university admissions and the \'Работа в России\' platform. The ranking of the relevant node is appropriately high, ensuring accurate retrieval.'}
──────────────────────────────────────────────────
Question: Какие возможности стажировок и трудоустройства предлагает вуз?
Result: {'question': 'Какие возможности стажировок и трудоустройства предлагает вуз?', 'score': 1.0, 'reason': "The score is 1.00 because all the retrieval contexts are ranked correctly, with the relevant nodes (nodes 1, 2, 3, and 6) consistently receiving 'yes' judgments. The irrelevant nodes (nodes 4, 5, 7, and 8) contain information about university regulations, program details, and enrollment numbers, which are clearly not related to the input question about internship and employment opportunities, ensuring a high level of precision."}
──────────────────────────────────────────────────
Question: Можно ли поменять выбранное направление после подачи заявления?
Result: {'question': 'Можно ли поменять выбранное направление после подачи заявления?', 'score': 1.0, 'reason': "The score is 1.00 because all retrieval contexts are highly relevant and ranked appropriately. Each node, including node 1, provides direct and affirmative answers to the question, stating that changes to the chosen direction are possible after submitting the application, as evidenced by the phrases 'можно внести изменения' and 'поменять направления' within the nodes' reasons."}
──────────────────────────────────────────────────
Question: Где можно ознакомиться с учебными планами и программами вступительных испытаний?
Result: {'question': 'Где можно ознакомиться с учебными планами и программами вступительных испытаний?', 'score': 1.0, 'reason': 'The contextual precision score is 1.00 because the first three retrieval contexts (ranked 1, 2, and 3) all correctly identify relevant nodes – providing information about where to find academic plans and entrance exam programs. The remaining nodes, while present in the context, offer irrelevant details about admissions procedures, document translation, verification processes, or student file creation, thus ensuring that the most pertinent information is ranked highest.'}

================================================================================
SUMMARY STATISTICS
================================================================================
Total questions: 20
Successfully evaluated: 20
Average Contextual Precision: 0.975
Min score: 0.810
Max score: 1.000
Count(score == 1): 16 (80.0%)
================================================================================

Process finished with exit code 0
```