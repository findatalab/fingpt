## Данные
Всего протестировано: 20 вопросов из файла `questions20.yaml`. В качестве контекста был
использован файл `answers20.yaml`, который имеет такую же структуру как `questions20.yaml`, но без вопросов
Для каждого FAQ-документа задан стабильный faq_id, который используется как gold-идентификатор для retrieval-оценки.
В Document.content хранится готовый ответ, что позволяет напрямую использовать retrieved documents в генерации.

## Использованная модель
- Gemma3 (через Ollama)

## Использованные метрики
- LLM-as-judge-метрики
  - Contextual Precision - насколько извлечённые документы действительно полезны для ответа.
  - Contextual Recall - насколько retriever покрыл всё нужное для ответа.


- IR-метрики (Information retrieval)
  - `Hit@k` - Есть ли хотя бы один релевантный документ среди топ-k результатов retriever-а.
  - `MRR = 1 / rank_first_relevant` - Насколько рано появляется первый релевантный документ.
  - `Precision@k = (# релевантных документов среди top-k) / k` - Сколько из top-k найденных элементов действительно релевантны?

Так как для каждого вопроса существует ровно один релевантный FAQ-документ, Precision@3 по определению ограничен значением 1/3 ≈ 0.33, даже при идеальном retrieval.



## Результаты
### IR-метрики
- Hit@3: ≈ 1.0 → правильный FAQ-документ почти всегда находится в топ-3.
- Hit@1: в большинстве случаев 1.0, но есть отдельные случаи, где релевантный документ находится на позиции 2.
- MRR: близок к 1.0 → первый релевантный документ почти всегда стоит на первой позиции.
- Precision@3: стабильно ≈ 0.33 → это ожидаемо и корректно, так как в топ-3 содержится ровно один релевантный документ.

### LLM-as-a-judge метрики
- Contextual Precision: в среднем высокая (≈ 0.7–1.0)
  - снижается, когда вместе с правильным FAQ-ответом в retrieval попадают дополнительные нерелевантные документы.

- Contextual Recall: сильно варьируется (≈ 0.1 – 1.0)
  - часто занижена, потому что: 
    - ответ в FAQ может быть короче эталонного;
    - LLM ожидает более “развёрнутое” покрытие всех формулировок expected answer.


## Ошибки
Тесты 5 и 20 завершились с ошибкой `RetryError ... TimeoutError`.
Вероятные причины:
- LLM-as-a-judge (gemma3 через Ollama) не успел ответить за заданный таймаут.

- Вопросы содержат:
  - более длинный контекст;
  - более сложную формулировку, что увеличило время генерации.

Ошибка не связана с retrieval-механизмом — retrieval для этих вопросов отработал корректно.


## Ограничения текущего подхода
1. Baseline-реализация
   - текущая схема оценки является первичной и демонстрационной;
   - код будет дорабатываться.
2. FAQ ≠ PDF
   - оценка проводилась на FAQ, где:
     - 1 документ = 1 ответ;
     - нет реального чанкинга.
   - для PDF-документов метрики и gold-разметка будут отличаться.
3. Precision@3 ограничен
   - текущая структура данных делает Precision@3 малопоказательной;
   - это не дефект retrieval, а особенность датасета.
4. Чанкинг ещё не финальный
   - стратегия разбиения документов (особенно PDF) будет пересматриваться;
   - после этого:
     - изменится распределение релевантных чанков;
     - потребуется повторная оценка retrieval.

## Вывод
Текущий retrieval-механизм корректно работает на FAQ-данных: релевантный документ почти всегда находится в топ-3 
и чаще всего — на первой позиции (высокие Hit@3 и MRR). Значение Precision@3 ≈ 0.33 ожидаемо и обусловлено тем, 
что для каждого вопроса существует только один релевантный чанк. Метрики LLM-as-a-judge подтверждают релевантность 
контекста, но зависят от формулировок ответов. Ошибки RetryError связаны с таймаутами judge-модели и не отражают 
качество retrieval. Полученные результаты являются baseline и будут пересмотрены после определения финальной 
стратегии чанкинга документов.


## Полный вывод программы
```
Success read 20 questions.

=== after_split ===
docs: 20
[0] content_len=1262 meta={'source_type': 'faq', 'source_file': 'data_files\\answers20.yaml', 'faq_id': 1, 'references': ['https://www.fa.ru/upload/constructor/0ce/v2jc8sysg7jyunar03dqfit1gfj7veyn/Prikaz-po-osnovnoy-deyatelnosti-_-0056_o-ot-20.01.2026-Ob-utv.-Pravil-priema-v-fed.-gos.-obraz.-byudzh.-uch.-vys.-obrazov.-_Finanso-_4574345-v1_stranitsy_2.pdf']}
[1] content_len=1419 meta={'source_type': 'faq', 'source_file': 'data_files\\answers20.yaml', 'faq_id': 2, 'references': ['https://www.fa.ru/upload/constructor/0ce/v2jc8sysg7jyunar03dqfit1gfj7veyn/Prikaz-po-osnovnoy-deyatelnosti-_-0056_o-ot-20.01.2026-Ob-utv.-Pravil-priema-v-fed.-gos.-obraz.-byudzh.-uch.-vys.-obrazov.-_Finanso-_4574345-v1_stranitsy_2.pdf']}
[2] content_len=415 meta={'source_type': 'faq', 'source_file': 'data_files\\answers20.yaml', 'faq_id': 3, 'references': ['https://www.fa.ru/upload/constructor/0ce/v2jc8sysg7jyunar03dqfit1gfj7veyn/Prikaz-po-osnovnoy-deyatelnosti-_-0056_o-ot-20.01.2026-Ob-utv.-Pravil-priema-v-fed.-gos.-obraz.-byudzh.-uch.-vys.-obrazov.-_Finanso-_4574345-v1_stranitsy_2.pdf']}
[3] content_len=646 meta={'source_type': 'faq', 'source_file': 'data_files\\answers20.yaml', 'faq_id': 4, 'references': ['https://www.fa.ru/upload/constructor/0ce/v2jc8sysg7jyunar03dqfit1gfj7veyn/Prikaz-po-osnovnoy-deyatelnosti-_-0056_o-ot-20.01.2026-Ob-utv.-Pravil-priema-v-fed.-gos.-obraz.-byudzh.-uch.-vys.-obrazov.-_Finanso-_4574345-v1_stranitsy_2.pdf']}
[4] content_len=1366 meta={'source_type': 'faq', 'source_file': 'data_files\\answers20.yaml', 'faq_id': 5, 'references': ['https://www.fa.ru/for-applicants/priyemka/min-balli']}
[5] content_len=1179 meta={'source_type': 'faq', 'source_file': 'data_files\\answers20.yaml', 'faq_id': 6, 'references': ['https://www.fa.ru/upload/constructor/0ce/v2jc8sysg7jyunar03dqfit1gfj7veyn/Prikaz-po-osnovnoy-deyatelnosti-_-0056_o-ot-20.01.2026-Ob-utv.-Pravil-priema-v-fed.-gos.-obraz.-byudzh.-uch.-vys.-obrazov.-_Finanso-_4574345-v1_stranitsy_2.pdf']}
[6] content_len=259 meta={'source_type': 'faq', 'source_file': 'data_files\\answers20.yaml', 'faq_id': 7, 'references': ['https://www.fa.ru/for-applicants/bachelor/control/']}
[7] content_len=363 meta={'source_type': 'faq', 'source_file': 'data_files\\answers20.yaml', 'faq_id': 8, 'references': ['https://www.fa.ru/for-applicants/bachelor/price/', 'https://www.fa.ru/for-applicants/bachelor/skidki/']}
[8] content_len=387 meta={'source_type': 'faq', 'source_file': 'data_files\\answers20.yaml', 'faq_id': 9, 'references': ['https://anketa.fa.ru/user/sign-in/start']}
[9] content_len=347 meta={'source_type': 'faq', 'source_file': 'data_files\\answers20.yaml', 'faq_id': 10, 'references': ['https://www.fa.ru/for-applicants/bachelor/sroki/']}
[10] content_len=375 meta={'source_type': 'faq', 'source_file': 'data_files\\answers20.yaml', 'faq_id': 11, 'references': ['https://podku.fa.ru/']}
[11] content_len=435 meta={'source_type': 'faq', 'source_file': 'data_files\\answers20.yaml', 'faq_id': 12, 'references': ['https://www.fa.ru/university/dormitories/#:~:text=%D0%BF%D0%BE%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F.%E2%80%8B.%20%D0%9A%D0%BE%D0%BD%D1%82%D0%B0%D0%BA%D1%82%D0%BD%D1%8B%D0%B9%20%D1%82%D0%B5%D0%BB%D0%B5%D1%84%D0%BE%D0%BD%20%D0%B4%D0%BB%D1%8F%20%D0%BE%D1%82%D0%B2%D0%B5%D1%82%D0%BE%D0%B2%20%D0%BD%D0%B0%20%D0%B2%D0%BE%D0%BF%D1%80%D0%BE%E2%80%8B%D1%81%D1%8B,%D1%81%D1%82%D1%83%D0%B4%D0%B5%D0%BD%D1%82%D0%B0%D0%BC:%20%E2%80%8B8(499)943%2D95%2D73%20%2D%20%D0%A1%D0%BB%D1%83%D0%B6%D0%B1%D0%B0%20%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F%20%D0%BF%D1%80%D0%BE%D0%B6%D0%B8%D0%B2%D0%B0%D1%8E%D1%89%D0%B8%D1%85%20%E2%80%8B.', 'https://altai.fa.ru/about/structural-units/hostel/moving-procedure/']}
[12] content_len=413 meta={'source_type': 'faq', 'source_file': 'data_files\\answers20.yaml', 'faq_id': 13, 'references': ['https://www.fa.ru/for-applicants/priyemka/prava/']}
[13] content_len=358 meta={'source_type': 'faq', 'source_file': 'data_files\\answers20.yaml', 'faq_id': 14, 'references': ['https://www.fa.ru/for-students/free/']}
[14] content_len=312 meta={'source_type': 'faq', 'source_file': 'data_files\\answers20.yaml', 'faq_id': 15, 'references': ['https://www.fa.ru/for-applicants/bachelor/#block-29480', 'https://www.fa.ru/for-applicants/master/#block-30278']}
[15] content_len=381 meta={'source_type': 'faq', 'source_file': 'data_files\\answers20.yaml', 'faq_id': 16, 'references': ['https://www.fa.ru/for-applicants/educational-programs/']}
[16] content_len=334 meta={'source_type': 'faq', 'source_file': 'data_files\\answers20.yaml', 'faq_id': 17, 'references': ['https://www.fa.ru/university/structure/educational-departments/dep/voen/']}
[17] content_len=382 meta={'source_type': 'faq', 'source_file': 'data_files\\answers20.yaml', 'faq_id': 18, 'references': ['https://www.fa.ru/employment/', 'https://www.fa.ru/university/structure/dpo/ipk/internships/', 'https://career.fa.ru/o-nas']}
[18] content_len=750 meta={'source_type': 'faq', 'source_file': 'data_files\\answers20.yaml', 'faq_id': 19, 'references': ['https://www.fa.ru/upload/constructor/0ce/v2jc8sysg7jyunar03dqfit1gfj7veyn/Prikaz-po-osnovnoy-deyatelnosti-_-0056_o-ot-20.01.2026-Ob-utv.-Pravil-priema-v-fed.-gos.-obraz.-byudzh.-uch.-vys.-obrazov.-_Finanso-_4574345-v1_stranitsy_2.pdf']}
[19] content_len=341 meta={'source_type': 'faq', 'source_file': 'data_files\\answers20.yaml', 'faq_id': 20, 'references': ['https://www.fa.ru/for-applicants/bachelor/ispitaniya/', 'https://www.fa.ru/for-applicants/educational-programs/']}
Batches: 100%|██████████| 1/1 [00:00<00:00,  1.40it/s]
Unsafe mode is enabled. This allows execution of arbitrary code in the Jinja template. Use this only if you trust the source of the template.
Batches: 100%|██████████| 1/1 [00:00<00:00, 62.60it/s]
Batches: 100%|██████████| 1/1 [00:00<00:00, 35.73it/s]
Batches: 100%|██████████| 1/1 [00:00<00:00, 21.91it/s]
Batches: 100%|██████████| 1/1 [00:00<00:00, 22.39it/s]
Batches: 100%|██████████| 1/1 [00:00<00:00, 66.66it/s]
Batches: 100%|██████████| 1/1 [00:00<00:00, 32.39it/s]
Batches: 100%|██████████| 1/1 [00:00<00:00, 26.82it/s]
Batches: 100%|██████████| 1/1 [00:00<00:00, 52.48it/s]
Batches: 100%|██████████| 1/1 [00:00<00:00, 52.48it/s]
Batches: 100%|██████████| 1/1 [00:00<00:00, 76.85it/s]
Batches: 100%|██████████| 1/1 [00:00<00:00, 73.24it/s]
Batches: 100%|██████████| 1/1 [00:00<00:00, 39.90it/s]
Batches: 100%|██████████| 1/1 [00:00<00:00, 62.81it/s]
Batches: 100%|██████████| 1/1 [00:00<00:00, 80.86it/s]
Batches: 100%|██████████| 1/1 [00:00<00:00, 41.86it/s]
Batches: 100%|██████████| 1/1 [00:00<00:00, 62.48it/s]
Batches: 100%|██████████| 1/1 [00:00<00:00, 49.35it/s]
Batches: 100%|██████████| 1/1 [00:00<00:00, 31.45it/s]
Batches: 100%|██████████| 1/1 [00:00<00:00, 19.75it/s]
Batches: 100%|██████████| 1/1 [00:00<00:00, 27.56it/s]

Evaluating question 1/20

IR → Hit@1=0.0 | Hit@3=1.0 | P@1=0.000 | P@3=0.333 | MRR=0.500 | Rank=2
✅ ContextualPrecision: 0.815
🧠 Reason: The contextual precision score is 0.81 because the relevant nodes (ranked 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11) successfully capture the core information about document requirements for admission, including specific details like document types, deadlines, and academic requirements. While some nodes (ranked 13) provide related information, the irrelevant nodes (ranked 14) focus on timelines, changing choices, and transfer options, which are tangential to the initial question about the necessary documents. The high score reflects the strong alignment of the top-ranked nodes with the input query.
✅ ContextualRecall: 1.000
🧠 Reason: The score is 1.00 because the expected output perfectly aligns with the retrieval context, which comprehensively details the required documents and procedures for applying to undergraduate and specialist programs, including submission formats, acceptance criteria, and related information. This demonstrates a highly accurate and relevant retrieval process, effectively capturing the essence of the original expected output.


Evaluating question 2/20

IR → Hit@1=1.0 | Hit@3=1.0 | P@1=1.000 | P@3=0.333 | MRR=1.000 | Rank=1
✅ ContextualPrecision: 0.705
🧠 Reason: The contextual precision score is 0.70 because the most relevant nodes (ranked 1, 2, 7, 8, and 9) successfully address the question about document submission deadlines, providing specific dates and requirements. However, several irrelevant nodes (ranked 3, 4, 5, 6, and 10) are present, causing a slight reduction in the score. The inclusion of these nodes, despite their lack of direct relevance to the question, impacts the overall precision.
✅ ContextualRecall: 1.000
🧠 Reason: The score is 1.00 because the retrieval context perfectly captures the expected output, providing a comprehensive and detailed timeline for both budget and paid place admissions in 2026, including deadlines, exam dates, and ranking list publication dates. All sentences are accurately represented by node(s) in retrieval context.


Evaluating question 3/20

IR → Hit@1=1.0 | Hit@3=1.0 | P@1=1.000 | P@3=0.333 | MRR=1.000 | Rank=1
✅ ContextualPrecision: 1.000
🧠 Reason: The score is 1.00 because the first three retrieval contexts, representing nodes 1, 2, and 3, all provide direct answers to the input question about the number of specializations one can choose when applying. Specifically, they state: 'При подаче заявления поступающий может выбрать до 5 специальностей и (или) направлений подготовки.' This demonstrates a high level of precision, with relevant nodes ranked optimally.
✅ ContextualRecall: 1.000
🧠 Reason: The score is 1.00 because the expected output perfectly aligns with the retrieval context, demonstrating a comprehensive and accurate understanding of the provided information regarding application procedures, specialization choices, and enrollment details. All sentences are directly attributable to nodes within the retrieval context, showcasing a strong contextual recall.


Evaluating question 4/20


IR → Hit@1=1.0 | Hit@3=1.0 | P@1=1.000 | P@3=0.333 | MRR=1.000 | Rank=1
✅ ContextualPrecision: 0.887
🧠 Reason: The score is 0.89 because the relevant nodes (ranks 1, 2, 4, 5, and 6) effectively address the input question about entrance tests and admission requirements, providing detailed explanations and aligning with the expected output. However, the lower score is due to the presence of irrelevant nodes (ranks 3, 7, 8, 9, and 10) which discuss unrelated topics like the 1968 Nobel Prize and tuition fees, preventing a perfect ranking of the pertinent information.
✅ ContextualRecall: 0.818
🧠 Reason: The score is 0.82 because the retrieval context effectively captures the core information about university entrance exams, including the requirements ( ЕГЭ results, potential additional tests), and specific categories of students who are exempt from exams (Olympiad winners, international Olympiad team members). This is clearly demonstrated by the presence of key sentences (1 & 2) within the first node of the retrieval context, providing a comprehensive overview of the process.

Evaluating question 5/20


❌ Evaluation failed: RetryError[<Future at 0x27d18a655e0 state=finished raised TimeoutError>]

Evaluating question 6/20


IR → Hit@1=1.0 | Hit@3=1.0 | P@1=1.000 | P@3=0.333 | MRR=1.000 | Rank=1
✅ ContextualPrecision: 0.610
🧠 Reason: The score is 0.61 because the most relevant nodes (ranked 1, 3, and 7) successfully address the question about obtaining target education, providing detailed steps and application processes. However, several irrelevant nodes (ranked 2, 4, 5, 6, 8, and 9) are present, and these nodes, particularly those discussing military training, tuition costs, and preparatory courses, are ranked higher than they should be, pulling down the overall score. The system needs to better prioritize the nodes directly related to the application process and target education.
✅ ContextualRecall: 0.462
🧠 Reason: The score is 0.46 because the retrieval context (node 1) primarily focuses on the process of obtaining target education, including finding a заказчик, submitting an application, and participating in a competition, aligning with the core topic of the expected output.

Evaluating question 7/20

IR → Hit@1=1.0 | Hit@3=1.0 | P@1=1.000 | P@3=0.333 | MRR=1.000 | Rank=1
✅ ContextualPrecision: 1.000
🧠 Reason: The score is 1.00 because the first two retrieval contexts provide highly relevant answers to the input question, directly stating the number of budget places allocated for 'Applied Machine Learning'. The third retrieval context, a node, is irrelevant as it discusses entrance exams and admission deadlines, which do not address the specific query about budget places.
✅ ContextualRecall: 1.000
🧠 Reason: The score is 1.00 because the expected output perfectly aligns with the information provided in the retrieval context (node(s) in retrieval context). Specifically, both sentences are directly present within the 1st node, offering a complete and accurate response to the query.


Evaluating question 8/20


IR → Hit@1=1.0 | Hit@3=1.0 | P@1=1.000 | P@3=0.333 | MRR=1.000 | Rank=1
✅ ContextualPrecision: 0.727
🧠 Reason: The contextual precision score of 0.73 reflects that while the most relevant nodes (ranked 1, 2, 4, 7, 8, 9, 10, 11, 12, 13) successfully address the input question about tuition costs and discounts, the lower-ranked nodes (ranked 3, 5, 6, 14) introduce irrelevant information. Specifically, the first node provides a direct answer to the question, the second confirms the existence of discounts, and the fourth reiterates the cost details. However, the lower-ranked nodes, such as the node at rank 3, which states, "'Вопрос: какова стоимость обучения и есть ли скидки?' is a question, not a piece of information that answers it. It's the query itself, not a relevant response," and nodes at ranks 5, 6, and 14, which discuss preparatory courses, accommodation, and transferring to budget education, are ranked lower and therefore contribute to the score.
✅ ContextualRecall: 0.182
🧠 Reason: The score is 0.18 because the retrieval context node(s) (node(s) in retrieval context: 'Вопрос: какова стоимость обучения и есть ли скидки? Ответ: Стоимость обучения по договору (контракту) составляет 190 000 – 762 500 рублей за год, в зависимости от направления подготовки и формы обучения. Предусмотрены Скидки и льготы (например, для победителей олимпиад, при высокой сумме баллов ЕГЭ и т.д.). С полным перечнем скидок можно ознакомиться на сайте.') contains the exact sentence about tuition costs and discounts, providing a direct match.

Evaluating question 9/20


IR → Hit@1=1.0 | Hit@3=1.0 | P@1=1.000 | P@3=0.333 | MRR=1.000 | Rank=1
✅ ContextualPrecision: 0.745
🧠 Reason: The contextual precision score of 0.75 is a good reflection of the retrieval context's performance. Several nodes, particularly those ranked higher (1, 2, 4, 5, 6, 7, 9, and 10), successfully answered the input question about applying documents online, providing direct instructions and details. However, the lower-ranked nodes (3, 8, and 11) contained irrelevant information, such as preparatory courses, admission benefits, and the university's military training center. These irrelevant nodes, despite being present in the retrieval context, were ranked lower, contributing to the overall score.
✅ ContextualRecall: 0.818
🧠 Reason: The score is 0.82 because the expected output effectively summarizes the online document submission process, aligning with node(s) in retrieval context, specifically node 1 and node 2, detailing the methods (ЕПГУ portal and university website) and steps involved.

Evaluating question 10/20


IR → Hit@1=1.0 | Hit@3=1.0 | P@1=1.000 | P@3=0.333 | MRR=1.000 | Rank=1
✅ ContextualPrecision: 0.784
🧠 Reason: The contextual precision score of 0.78 reflects that while many of the retrieval contexts (nodes 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12) are highly relevant, the lower score is due to the presence of several irrelevant nodes (nodes 13, 14, 15, 16). Specifically, nodes 13 and 16, which discuss preparatory courses and the university's military training center, are ranked lower than the nodes that directly address the question about publication dates of competitive lists and admission orders. The high ranking of nodes 1-12 ensures a good overall score, but the inclusion of these less relevant nodes prevents a higher score.
✅ ContextualRecall: 1.000
🧠 Reason: The score is 1.00 because the expected output provides a comprehensive and detailed response to the query about the publication dates and timelines for admission to the university, directly addressing the question through multiple sentences and referencing specific dates and procedures within the retrieval context (node(s) in retrieval context).

Evaluating question 11/20


IR → Hit@1=1.0 | Hit@3=1.0 | P@1=1.000 | P@3=0.333 | MRR=1.000 | Rank=1
✅ ContextualPrecision: 0.917
🧠 Reason: The contextual precision score is 0.92 because the first three retrieval contexts, containing the 'yes' verdicts, effectively rank the most relevant information about preparatory courses and their costs. The remaining nodes, particularly those ranked lower (e.g., nodes 4, 6, 7, 8, 9, 10), provide tangential details about application processes, tuition contracts, or student dormitories, which, while potentially useful, don't directly address the core question about preparatory courses and their costs. This demonstrates a strong ranking of the pertinent nodes, justifying the high score.
✅ ContextualRecall: 0.143
🧠 Reason: The score is 0.14 because the retrieval context primarily addresses the initial question about preparatory courses and their costs, as evidenced by sentences 1 and 2 within node(s) in retrieval context, but fails to capture details regarding application procedures, deadlines, or specific eligibility criteria, as found in sentences 6-13 within node(s) in retrieval context.

Evaluating question 12/20


IR → Hit@1=1.0 | Hit@3=1.0 | P@1=1.000 | P@3=0.333 | MRR=1.000 | Rank=1
✅ ContextualPrecision: 1.000
🧠 Reason: The score is 1.00 because the first three retrieval contexts, ranked highest, all provide affirmative answers to the question about hostel availability for international students. Specifically, nodes 1 and 2 directly state that accommodation is typically provided, and node 3 offers details about the accommodation. The remaining nodes, ranked lower, contain irrelevant information, such as details about transfers, online submissions, or tuition costs, ensuring that only the most pertinent contexts are prioritized.
✅ ContextualRecall: 0.500
🧠 Reason: The score is 0.50 because the retrieval context primarily addresses the initial question about providing dormitories to nonresident students (node(s) in retrieval context: 'Вопрос: предоставляется ли общежитие иногородним студентам?'). While the first two sentences are present in the context, the remaining sentences are not, indicating a partial overlap and thus a moderate recall score.

Evaluating question 13/20

IR → Hit@1=1.0 | Hit@3=1.0 | P@1=1.000 | P@3=0.333 | MRR=1.000 | Rank=1
✅ ContextualPrecision: 0.739
🧠 Reason: The contextual precision score of 0.74 reflects that while the most relevant nodes (ranked 1, 3, 4, 6, 7, 8, 9) successfully address the input question about benefits and special rights, the lower-ranked nodes (ranked 2, 5, 10) contain irrelevant information about preparatory courses, the online application process, required documents, and minimum passing scores. The presence of these irrelevant nodes, despite the higher-ranked nodes providing accurate answers, contributes to the score.
✅ ContextualRecall: 0.375
🧠 Reason: The contextual recall score is 0.38 because the retrieval context successfully captures key aspects of the expected output, particularly regarding admission benefits (nodes 1) and where to find further details (nodes 2). Specifically, sentences 1-6 directly reference information within node(s) in retrieval context, outlining benefits like olympiad admissions and preferential enrollment, while sentences 2-6 provide links to the official university website for complete details.


Evaluating question 14/20


IR → Hit@1=1.0 | Hit@3=1.0 | P@1=1.000 | P@3=0.333 | MRR=1.000 | Rank=1
✅ ContextualPrecision: 0.776
🧠 Reason: The contextual precision score of 0.78 reflects that while the most relevant nodes (ranked 1-10) successfully address the query about transferring between tuition types, the lower-ranked nodes (11-13) introduce tangential information about student accommodation, program changes, tuition costs, and preparatory courses. These irrelevant nodes, despite being present in the retrieval context, prevent the score from being higher, as they dilute the focus on the core question about transferring enrollment.
✅ ContextualRecall: 1.000
🧠 Reason: The score is 1.00 because the entire expected output seamlessly aligns with the retrieval context, specifically node(s) in retrieval context. The first sentence directly corresponds to node 1, and the second sentence aligns with node 2, providing a comprehensive and accurate representation of the topic.

Evaluating question 15/20


IR → Hit@1=1.0 | Hit@3=1.0 | P@1=1.000 | P@3=0.333 | MRR=1.000 | Rank=1
✅ ContextualPrecision: 0.767
🧠 Reason: The score is 0.77 because the top nodes (1, 2, 4, 7, 9) successfully identify relevant information about studying evening courses, including how to find details and submit documents. However, the lower-ranked nodes (3, 5, 6, 8, 10) provide irrelevant information about target education, preparatory courses, admissions timing, student housing, military departments, and tuition fees, which prevents the contextual precision from reaching a higher score.
✅ ContextualRecall: 1.000
🧠 Reason: The score is 1.00 because the provided text perfectly aligns with the expected output, demonstrating a comprehensive and accurate retrieval context. The first node (Вопрос: есть ли возможность учиться заочно/очно‑заочно на выбранной специальности? Ответ: Наличие заочной или очно‑заочной формы обучения зависит от направления подготовки. Информацию о формах обучения по конкретной специальности можно найти на сайте вуза (в описании программы) или уточнить в приёмной комиссии.) directly and completely answers the question about remote learning options, reflecting the core information of the expected output, and all other nodes provide relevant supplementary details.

Evaluating question 16/20


IR → Hit@1=1.0 | Hit@3=1.0 | P@1=1.000 | P@3=0.333 | MRR=1.000 | Rank=1
✅ ContextualPrecision: 1.000
🧠 Reason: The score is 1.00 because the relevant nodes (specifically, nodes 1 and 2) provide precise and directly applicable answers to the question about study duration, citing durations for various programs with clear details. The irrelevant node (node 3) discusses minimum entrance scores, which is a distinct topic and therefore ranked lower.
✅ ContextualRecall: 0.818
🧠 Reason: The score is 0.82 because the expected output effectively details the duration of studies across different educational levels (бакалавриат, специалитет, магистратура) and forms of study (очно, заочно), aligning with node(s) in retrieval context 1 and 2, which focuses on educational program timelines and minimum scores.

Evaluating question 17/20

IR → Hit@1=1.0 | Hit@3=1.0 | P@1=1.000 | P@3=0.333 | MRR=1.000 | Rank=1
✅ ContextualPrecision: 1.000
🧠 Reason: The score is 1.00 because the first three retrieval contexts, ranked highest, all provide affirmative responses regarding the existence of a military department within the university – specifically, the 'Военный учебный центр' at the Financial University. The remaining nodes, ranked lower, consistently offer irrelevant information about scholarships, tuition, or study programs, thus ensuring that the most pertinent nodes are prioritized and accurately reflect the input's intent.
✅ ContextualRecall: 0.118
🧠 Reason: The score is 0.12 because the first retrieval context node (node(s) in retrieval context: 1) contains the sentence 'Да, в Финансовом университете при Правительстве Российской Федерации (г. Москва) действует Военный учебный центр (ВУЦ), который заменил военную кафедру.' which directly addresses the core topic of the expected output.


Evaluating question 18/20


IR → Hit@1=1.0 | Hit@3=1.0 | P@1=1.000 | P@3=0.333 | MRR=1.000 | Rank=1
✅ ContextualPrecision: 0.906
🧠 Reason: The score is 0.91 because the retrieval contexts successfully rank the highly relevant nodes (nodes 1, 2, 3, 4, 5, 6, 7, 8, 9, and 10) higher than the irrelevant node (node 4). The high score reflects that the nodes containing information about internships, employment opportunities, admissions processes, and related university details are prioritized, effectively addressing the input question. The ranking ensures that the most pertinent contexts are presented first, maximizing the precision of the response.
✅ ContextualRecall: 0.231
🧠 Reason: The score is 0.23 because the retrieval context primarily focuses on the university's internship and career services offerings (node(s) in retrieval context: 1, 2, 3), but the provided expected output contains additional details about finding more information on the university website or contacting the career center (node(s) in retrieval context: 3).

Evaluating question 19/20


IR → Hit@1=1.0 | Hit@3=1.0 | P@1=1.000 | P@3=0.333 | MRR=1.000 | Rank=1
✅ ContextualPrecision: 1.000
🧠 Reason: The score is 1.00 because all retrieval contexts are highly relevant, with each node providing direct answers to the input question. Specifically, nodes 1, 2, and 3 offer explicit statements about changing directions after submitting an application, while nodes 4, 5, 6, 7, 8, 9, 10, 11, and 12 consistently rank higher than the irrelevant nodes, ensuring that the most pertinent information is presented first.
✅ ContextualRecall: 0.357
🧠 Reason: The score is 0.36 because the retrieval context (node(s) 1) accurately captures the core query about changing study directions after submitting an application, including details about modifying chosen groups and priorities, and the time limit for changes. The context provides specific sentences like 'После подачи заявления поступающий может изменить выбранные направления и конкурсные группы, а также приоритеты зачисления и другие сведения.' which directly addresses the question, demonstrating a strong connection to the original expected output.

Evaluating question 20/20

❌ Evaluation failed: RetryError[<Future at 0x27d18aedb50 state=finished raised TimeoutError>]


================================================================================
FINAL RESULTS (per question)
================================================================================
──────────────────────────────────────────────────
Question: Какие документы необходимы для подачи заявления на поступление?
IR metrics: {'gold_faq_id': 1, 'hit@1': 0.0, 'hit@3': 1.0, 'precision@1': 0.0, 'precision@3': 0.3333333333333333, 'mrr': 0.5, 'first_relevant_rank': 2}
Judge metrics: {'context_precision': {'score': 0.8148674242424243, 'reason': 'The contextual precision score is 0.81 because the relevant nodes (ranked 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11) successfully capture the core information about document requirements for admission, including specific details like document types, deadlines, and academic requirements. While some nodes (ranked 13) provide related information, the irrelevant nodes (ranked 14) focus on timelines, changing choices, and transfer options, which are tangential to the initial question about the necessary documents. The high score reflects the strong alignment of the top-ranked nodes with the input query.'}, 'context_recall': {'score': 1.0, 'reason': 'The score is 1.00 because the expected output perfectly aligns with the retrieval context, which comprehensively details the required documents and procedures for applying to undergraduate and specialist programs, including submission formats, acceptance criteria, and related information. This demonstrates a highly accurate and relevant retrieval process, effectively capturing the essence of the original expected output.'}}
──────────────────────────────────────────────────
Question: Каковы сроки приёма документов в этом году?
IR metrics: {'gold_faq_id': 2, 'hit@1': 1.0, 'hit@3': 1.0, 'precision@1': 1.0, 'precision@3': 0.3333333333333333, 'mrr': 1.0, 'first_relevant_rank': 1}
Judge metrics: {'context_precision': {'score': 0.7048611111111112, 'reason': 'The contextual precision score is 0.70 because the most relevant nodes (ranked 1, 2, 7, 8, and 9) successfully address the question about document submission deadlines, providing specific dates and requirements. However, several irrelevant nodes (ranked 3, 4, 5, 6, and 10) are present, causing a slight reduction in the score. The inclusion of these nodes, despite their lack of direct relevance to the question, impacts the overall precision.'}, 'context_recall': {'score': 1.0, 'reason': 'The score is 1.00 because the retrieval context perfectly captures the expected output, providing a comprehensive and detailed timeline for both budget and paid place admissions in 2026, including deadlines, exam dates, and ranking list publication dates. All sentences are accurately represented by node(s) in retrieval context.'}}
──────────────────────────────────────────────────
Question: Сколько направлений (специальностей) можно выбрать при подаче заявления?
IR metrics: {'gold_faq_id': 3, 'hit@1': 1.0, 'hit@3': 1.0, 'precision@1': 1.0, 'precision@3': 0.3333333333333333, 'mrr': 1.0, 'first_relevant_rank': 1}
Judge metrics: {'context_precision': {'score': 1.0, 'reason': "The score is 1.00 because the first three retrieval contexts, representing nodes 1, 2, and 3, all provide direct answers to the input question about the number of specializations one can choose when applying. Specifically, they state: 'При подаче заявления поступающий может выбрать до 5 специальностей и (или) направлений подготовки.' This demonstrates a high level of precision, with relevant nodes ranked optimally."}, 'context_recall': {'score': 1.0, 'reason': 'The score is 1.00 because the expected output perfectly aligns with the retrieval context, demonstrating a comprehensive and accurate understanding of the provided information regarding application procedures, specialization choices, and enrollment details. All sentences are directly attributable to nodes within the retrieval context, showcasing a strong contextual recall.'}}
──────────────────────────────────────────────────
Question: Какие вступительные испытания нужно пройти (ЕГЭ, дополнительные экзамены)?
IR metrics: {'gold_faq_id': 4, 'hit@1': 1.0, 'hit@3': 1.0, 'precision@1': 1.0, 'precision@3': 0.3333333333333333, 'mrr': 1.0, 'first_relevant_rank': 1}
Judge metrics: {'context_precision': {'score': 0.8875, 'reason': 'The score is 0.89 because the relevant nodes (ranks 1, 2, 4, 5, and 6) effectively address the input question about entrance tests and admission requirements, providing detailed explanations and aligning with the expected output. However, the lower score is due to the presence of irrelevant nodes (ranks 3, 7, 8, 9, and 10) which discuss unrelated topics like the 1968 Nobel Prize and tuition fees, preventing a perfect ranking of the pertinent information.'}, 'context_recall': {'score': 0.8181818181818182, 'reason': 'The score is 0.82 because the retrieval context effectively captures the core information about university entrance exams, including the requirements ( ЕГЭ results, potential additional tests), and specific categories of students who are exempt from exams (Olympiad winners, international Olympiad team members). This is clearly demonstrated by the presence of key sentences (1 & 2) within the first node of the retrieval context, providing a comprehensive overview of the process.'}}
──────────────────────────────────────────────────
Question: Каков минимальный проходной балл по каждому предмету?
Error: RetryError[<Future at 0x27d18a655e0 state=finished raised TimeoutError>]
IR metrics: {'gold_faq_id': 5, 'hit@1': 1.0, 'hit@3': 1.0, 'precision@1': 1.0, 'precision@3': 0.3333333333333333, 'mrr': 1.0, 'first_relevant_rank': 1}
Judge metrics: {'context_precision': {'score': None, 'reason': None}, 'context_recall': {'score': None, 'reason': None}}
──────────────────────────────────────────────────
Question: Есть ли в университете целевое обучение и как его получить?
IR metrics: {'gold_faq_id': 6, 'hit@1': 1.0, 'hit@3': 1.0, 'precision@1': 1.0, 'precision@3': 0.3333333333333333, 'mrr': 1.0, 'first_relevant_rank': 1}
Judge metrics: {'context_precision': {'score': 0.6104166666666666, 'reason': 'The score is 0.61 because the most relevant nodes (ranked 1, 3, and 7) successfully address the question about obtaining target education, providing detailed steps and application processes. However, several irrelevant nodes (ranked 2, 4, 5, 6, 8, and 9) are present, and these nodes, particularly those discussing military training, tuition costs, and preparatory courses, are ranked higher than they should be, pulling down the overall score. The system needs to better prioritize the nodes directly related to the application process and target education.'}, 'context_recall': {'score': 0.46153846153846156, 'reason': 'The score is 0.46 because the retrieval context (node 1) primarily focuses on the process of obtaining target education, including finding a заказчик, submitting an application, and participating in a competition, aligning with the core topic of the expected output.'}}
──────────────────────────────────────────────────
Question: Сколько бюджетных мест выделено на направлении Прикладное машинное обучение?
IR metrics: {'gold_faq_id': 7, 'hit@1': 1.0, 'hit@3': 1.0, 'precision@1': 1.0, 'precision@3': 0.3333333333333333, 'mrr': 1.0, 'first_relevant_rank': 1}
Judge metrics: {'context_precision': {'score': 1.0, 'reason': "The score is 1.00 because the first two retrieval contexts provide highly relevant answers to the input question, directly stating the number of budget places allocated for 'Applied Machine Learning'. The third retrieval context, a node, is irrelevant as it discusses entrance exams and admission deadlines, which do not address the specific query about budget places."}, 'context_recall': {'score': 1.0, 'reason': 'The score is 1.00 because the expected output perfectly aligns with the information provided in the retrieval context (node(s) in retrieval context). Specifically, both sentences are directly present within the 1st node, offering a complete and accurate response to the query.'}}
──────────────────────────────────────────────────
Question: Какова стоимость обучения и есть ли скидки?
IR metrics: {'gold_faq_id': 8, 'hit@1': 1.0, 'hit@3': 1.0, 'precision@1': 1.0, 'precision@3': 0.3333333333333333, 'mrr': 1.0, 'first_relevant_rank': 1}
Judge metrics: {'context_precision': {'score': 0.7268629518629519, 'reason': 'The contextual precision score of 0.73 reflects that while the most relevant nodes (ranked 1, 2, 4, 7, 8, 9, 10, 11, 12, 13) successfully address the input question about tuition costs and discounts, the lower-ranked nodes (ranked 3, 5, 6, 14) introduce irrelevant information. Specifically, the first node provides a direct answer to the question, the second confirms the existence of discounts, and the fourth reiterates the cost details. However, the lower-ranked nodes, such as the node at rank 3, which states, "\'Вопрос: какова стоимость обучения и есть ли скидки?\' is a question, not a piece of information that answers it. It\'s the query itself, not a relevant response," and nodes at ranks 5, 6, and 14, which discuss preparatory courses, accommodation, and transferring to budget education, are ranked lower and therefore contribute to the score.'}, 'context_recall': {'score': 0.18181818181818182, 'reason': "The score is 0.18 because the retrieval context node(s) (node(s) in retrieval context: 'Вопрос: какова стоимость обучения и есть ли скидки? Ответ: Стоимость обучения по договору (контракту) составляет 190 000 – 762 500 рублей за год, в зависимости от направления подготовки и формы обучения. Предусмотрены Скидки и льготы (например, для победителей олимпиад, при высокой сумме баллов ЕГЭ и т.д.). С полным перечнем скидок можно ознакомиться на сайте.') contains the exact sentence about tuition costs and discounts, providing a direct match."}}
──────────────────────────────────────────────────
Question: Можно ли подать документы онлайн, и как это сделать?
IR metrics: {'gold_faq_id': 9, 'hit@1': 1.0, 'hit@3': 1.0, 'precision@1': 1.0, 'precision@3': 0.3333333333333333, 'mrr': 1.0, 'first_relevant_rank': 1}
Judge metrics: {'context_precision': {'score': 0.7453968253968254, 'reason': "The contextual precision score of 0.75 is a good reflection of the retrieval context's performance. Several nodes, particularly those ranked higher (1, 2, 4, 5, 6, 7, 9, and 10), successfully answered the input question about applying documents online, providing direct instructions and details. However, the lower-ranked nodes (3, 8, and 11) contained irrelevant information, such as preparatory courses, admission benefits, and the university's military training center. These irrelevant nodes, despite being present in the retrieval context, were ranked lower, contributing to the overall score."}, 'context_recall': {'score': 0.8181818181818182, 'reason': 'The score is 0.82 because the expected output effectively summarizes the online document submission process, aligning with node(s) in retrieval context, specifically node 1 and node 2, detailing the methods (ЕПГУ portal and university website) and steps involved.'}}
──────────────────────────────────────────────────
Question: Когда будут опубликованы конкурсные списки и приказы о зачислении?
IR metrics: {'gold_faq_id': 10, 'hit@1': 1.0, 'hit@3': 1.0, 'precision@1': 1.0, 'precision@3': 0.3333333333333333, 'mrr': 1.0, 'first_relevant_rank': 1}
Judge metrics: {'context_precision': {'score': 0.7843033509700176, 'reason': "The contextual precision score of 0.78 reflects that while many of the retrieval contexts (nodes 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12) are highly relevant, the lower score is due to the presence of several irrelevant nodes (nodes 13, 14, 15, 16). Specifically, nodes 13 and 16, which discuss preparatory courses and the university's military training center, are ranked lower than the nodes that directly address the question about publication dates of competitive lists and admission orders. The high ranking of nodes 1-12 ensures a good overall score, but the inclusion of these less relevant nodes prevents a higher score."}, 'context_recall': {'score': 1.0, 'reason': 'The score is 1.00 because the expected output provides a comprehensive and detailed response to the query about the publication dates and timelines for admission to the university, directly addressing the question through multiple sentences and referencing specific dates and procedures within the retrieval context (node(s) in retrieval context).'}}
──────────────────────────────────────────────────
Question: Есть ли подготовительные курсы для абитуриентов и сколько они стоят?
IR metrics: {'gold_faq_id': 11, 'hit@1': 1.0, 'hit@3': 1.0, 'precision@1': 1.0, 'precision@3': 0.3333333333333333, 'mrr': 1.0, 'first_relevant_rank': 1}
Judge metrics: {'context_precision': {'score': 0.9166666666666666, 'reason': "The contextual precision score is 0.92 because the first three retrieval contexts, containing the 'yes' verdicts, effectively rank the most relevant information about preparatory courses and their costs. The remaining nodes, particularly those ranked lower (e.g., nodes 4, 6, 7, 8, 9, 10), provide tangential details about application processes, tuition contracts, or student dormitories, which, while potentially useful, don't directly address the core question about preparatory courses and their costs. This demonstrates a strong ranking of the pertinent nodes, justifying the high score."}, 'context_recall': {'score': 0.14285714285714285, 'reason': 'The score is 0.14 because the retrieval context primarily addresses the initial question about preparatory courses and their costs, as evidenced by sentences 1 and 2 within node(s) in retrieval context, but fails to capture details regarding application procedures, deadlines, or specific eligibility criteria, as found in sentences 6-13 within node(s) in retrieval context.'}}
──────────────────────────────────────────────────
Question: Предоставляется ли общежитие иногородним студентам?
IR metrics: {'gold_faq_id': 12, 'hit@1': 1.0, 'hit@3': 1.0, 'precision@1': 1.0, 'precision@3': 0.3333333333333333, 'mrr': 1.0, 'first_relevant_rank': 1}
Judge metrics: {'context_precision': {'score': 1.0, 'reason': 'The score is 1.00 because the first three retrieval contexts, ranked highest, all provide affirmative answers to the question about hostel availability for international students. Specifically, nodes 1 and 2 directly state that accommodation is typically provided, and node 3 offers details about the accommodation. The remaining nodes, ranked lower, contain irrelevant information, such as details about transfers, online submissions, or tuition costs, ensuring that only the most pertinent contexts are prioritized.'}, 'context_recall': {'score': 0.5, 'reason': "The score is 0.50 because the retrieval context primarily addresses the initial question about providing dormitories to nonresident students (node(s) in retrieval context: 'Вопрос: предоставляется ли общежитие иногородним студентам?'). While the first two sentences are present in the context, the remaining sentences are not, indicating a partial overlap and thus a moderate recall score."}}
──────────────────────────────────────────────────
Question: Какие льготы и особые права при поступлении предусмотрены (олимпиады, инвалидность и т.д.)?
IR metrics: {'gold_faq_id': 13, 'hit@1': 1.0, 'hit@3': 1.0, 'precision@1': 1.0, 'precision@3': 0.3333333333333333, 'mrr': 1.0, 'first_relevant_rank': 1}
Judge metrics: {'context_precision': {'score': 0.7392857142857142, 'reason': 'The contextual precision score of 0.74 reflects that while the most relevant nodes (ranked 1, 3, 4, 6, 7, 8, 9) successfully address the input question about benefits and special rights, the lower-ranked nodes (ranked 2, 5, 10) contain irrelevant information about preparatory courses, the online application process, required documents, and minimum passing scores. The presence of these irrelevant nodes, despite the higher-ranked nodes providing accurate answers, contributes to the score.'}, 'context_recall': {'score': 0.375, 'reason': 'The contextual recall score is 0.38 because the retrieval context successfully captures key aspects of the expected output, particularly regarding admission benefits (nodes 1) and where to find further details (nodes 2). Specifically, sentences 1-6 directly reference information within node(s) in retrieval context, outlining benefits like olympiad admissions and preferential enrollment, while sentences 2-6 provide links to the official university website for complete details.'}}
──────────────────────────────────────────────────
Question: Можно ли перевестись с платного обучения на бюджетное?
IR metrics: {'gold_faq_id': 14, 'hit@1': 1.0, 'hit@3': 1.0, 'precision@1': 1.0, 'precision@3': 0.3333333333333333, 'mrr': 1.0, 'first_relevant_rank': 1}
Judge metrics: {'context_precision': {'score': 0.7759259259259258, 'reason': 'The contextual precision score of 0.78 reflects that while the most relevant nodes (ranked 1-10) successfully address the query about transferring between tuition types, the lower-ranked nodes (11-13) introduce tangential information about student accommodation, program changes, tuition costs, and preparatory courses. These irrelevant nodes, despite being present in the retrieval context, prevent the score from being higher, as they dilute the focus on the core question about transferring enrollment.'}, 'context_recall': {'score': 1.0, 'reason': 'The score is 1.00 because the entire expected output seamlessly aligns with the retrieval context, specifically node(s) in retrieval context. The first sentence directly corresponds to node 1, and the second sentence aligns with node 2, providing a comprehensive and accurate representation of the topic.'}}
──────────────────────────────────────────────────
Question: Есть ли возможность учиться заочно/очно‑заочно на выбранной специальности?
IR metrics: {'gold_faq_id': 15, 'hit@1': 1.0, 'hit@3': 1.0, 'precision@1': 1.0, 'precision@3': 0.3333333333333333, 'mrr': 1.0, 'first_relevant_rank': 1}
Judge metrics: {'context_precision': {'score': 0.7666666666666666, 'reason': 'The score is 0.77 because the top nodes (1, 2, 4, 7, 9) successfully identify relevant information about studying evening courses, including how to find details and submit documents. However, the lower-ranked nodes (3, 5, 6, 8, 10) provide irrelevant information about target education, preparatory courses, admissions timing, student housing, military departments, and tuition fees, which prevents the contextual precision from reaching a higher score.'}, 'context_recall': {'score': 1.0, 'reason': 'The score is 1.00 because the provided text perfectly aligns with the expected output, demonstrating a comprehensive and accurate retrieval context. The first node (Вопрос: есть ли возможность учиться заочно/очно‑заочно на выбранной специальности? Ответ: Наличие заочной или очно‑заочной формы обучения зависит от направления подготовки. Информацию о формах обучения по конкретной специальности можно найти на сайте вуза (в описании программы) или уточнить в приёмной комиссии.) directly and completely answers the question about remote learning options, reflecting the core information of the expected output, and all other nodes provide relevant supplementary details.'}}
──────────────────────────────────────────────────
Question: Какова продолжительность обучения по моей программе (бакалавриат/специалитет/магистратура)?
IR metrics: {'gold_faq_id': 16, 'hit@1': 1.0, 'hit@3': 1.0, 'precision@1': 1.0, 'precision@3': 0.3333333333333333, 'mrr': 1.0, 'first_relevant_rank': 1}
Judge metrics: {'context_precision': {'score': 1.0, 'reason': 'The score is 1.00 because the relevant nodes (specifically, nodes 1 and 2) provide precise and directly applicable answers to the question about study duration, citing durations for various programs with clear details. The irrelevant node (node 3) discusses minimum entrance scores, which is a distinct topic and therefore ranked lower.'}, 'context_recall': {'score': 0.8181818181818182, 'reason': 'The score is 0.82 because the expected output effectively details the duration of studies across different educational levels (бакалавриат, специалитет, магистратура) and forms of study (очно, заочно), aligning with node(s) in retrieval context 1 and 2, which focuses on educational program timelines and minimum scores.'}}
──────────────────────────────────────────────────
Question: Есть ли военная кафедра в университете?
IR metrics: {'gold_faq_id': 17, 'hit@1': 1.0, 'hit@3': 1.0, 'precision@1': 1.0, 'precision@3': 0.3333333333333333, 'mrr': 1.0, 'first_relevant_rank': 1}
Judge metrics: {'context_precision': {'score': 1.0, 'reason': "The score is 1.00 because the first three retrieval contexts, ranked highest, all provide affirmative responses regarding the existence of a military department within the university – specifically, the 'Военный учебный центр' at the Financial University. The remaining nodes, ranked lower, consistently offer irrelevant information about scholarships, tuition, or study programs, thus ensuring that the most pertinent nodes are prioritized and accurately reflect the input's intent."}, 'context_recall': {'score': 0.11764705882352941, 'reason': "The score is 0.12 because the first retrieval context node (node(s) in retrieval context: 1) contains the sentence 'Да, в Финансовом университете при Правительстве Российской Федерации (г. Москва) действует Военный учебный центр (ВУЦ), который заменил военную кафедру.' which directly addresses the core topic of the expected output."}}
──────────────────────────────────────────────────
Question: Какие возможности стажировок и трудоустройства предлагает вуз?
IR metrics: {'gold_faq_id': 18, 'hit@1': 1.0, 'hit@3': 1.0, 'precision@1': 1.0, 'precision@3': 0.3333333333333333, 'mrr': 1.0, 'first_relevant_rank': 1}
Judge metrics: {'context_precision': {'score': 0.9060405643738976, 'reason': 'The score is 0.91 because the retrieval contexts successfully rank the highly relevant nodes (nodes 1, 2, 3, 4, 5, 6, 7, 8, 9, and 10) higher than the irrelevant node (node 4). The high score reflects that the nodes containing information about internships, employment opportunities, admissions processes, and related university details are prioritized, effectively addressing the input question. The ranking ensures that the most pertinent contexts are presented first, maximizing the precision of the response.'}, 'context_recall': {'score': 0.23076923076923078, 'reason': "The score is 0.23 because the retrieval context primarily focuses on the university's internship and career services offerings (node(s) in retrieval context: 1, 2, 3), but the provided expected output contains additional details about finding more information on the university website or contacting the career center (node(s) in retrieval context: 3)."}}
──────────────────────────────────────────────────
Question: Можно ли поменять выбранное направление после подачи заявления?
IR metrics: {'gold_faq_id': 19, 'hit@1': 1.0, 'hit@3': 1.0, 'precision@1': 1.0, 'precision@3': 0.3333333333333333, 'mrr': 1.0, 'first_relevant_rank': 1}
Judge metrics: {'context_precision': {'score': 1.0, 'reason': 'The score is 1.00 because all retrieval contexts are highly relevant, with each node providing direct answers to the input question. Specifically, nodes 1, 2, and 3 offer explicit statements about changing directions after submitting an application, while nodes 4, 5, 6, 7, 8, 9, 10, 11, and 12 consistently rank higher than the irrelevant nodes, ensuring that the most pertinent information is presented first.'}, 'context_recall': {'score': 0.35714285714285715, 'reason': "The score is 0.36 because the retrieval context (node(s) 1) accurately captures the core query about changing study directions after submitting an application, including details about modifying chosen groups and priorities, and the time limit for changes. The context provides specific sentences like 'После подачи заявления поступающий может изменить выбранные направления и конкурсные группы, а также приоритеты зачисления и другие сведения.' which directly addresses the question, demonstrating a strong connection to the original expected output."}}
──────────────────────────────────────────────────
Question: Где можно ознакомиться с учебными планами и программами вступительных испытаний?
Error: RetryError[<Future at 0x27d18aedb50 state=finished raised TimeoutError>]
IR metrics: {'gold_faq_id': 20, 'hit@1': 1.0, 'hit@3': 1.0, 'precision@1': 1.0, 'precision@3': 0.3333333333333333, 'mrr': 1.0, 'first_relevant_rank': 1}
Judge metrics: {'context_precision': {'score': None, 'reason': None}, 'context_recall': {'score': None, 'reason': None}}

Process finished with exit code 0
```