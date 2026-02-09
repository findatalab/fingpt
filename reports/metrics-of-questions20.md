## Данные
Всего протестировано: 20 вопросов из файла `questions20.yaml`.

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


## Результаты
### IR-метрики
Все IR-метрики 0, так как пока что нужно разобраться с чанкингом и в `questions20.yaml` нужно указать
chunk_id правильных контекстов для ответа на вопрос

### LLM-as-a-judge метрики
- Contextual Precision = 0
- Contextual Recall = 0

Обе метрики по 0, так как retrieval-механизм работает плохо, документ разбит по фиксированному размеру окна, а не по смыслу.


## Ограничения текущего подхода
1. Baseline-реализация
   - текущая схема оценки является первичной и демонстрационной;
   - код будет дорабатываться.
2. Чанкинг ещё не финальный
   - стратегия разбиения документов (особенно PDF) будет пересматриваться;
   - после этого:
     - изменится распределение релевантных чанков;
     - потребуется повторная оценка retrieval.

## Вывод
Полученные результаты являются baseline и будут пересмотрены после определения финальной стратегии чанкинга документов.


## Полный вывод программы
```
C:\Users\ashyr\PycharmProjects\fin-enroll-rag\.venv\Scripts\python.exe C:\Users\ashyr\PycharmProjects\fin-enroll-rag\eval.py 
Success read 20 questions.

=== after_split ===
docs: 54
[0] content_len=2908 meta={'file_path': 'Pravila-priema-2025-bakalavriat.pdf', 'source_id': 'f2cdb91300f837f8b1bfd6088e5946523d97a983ec70a7bca80f531d2ce40466', 'page_number': 1, 'split_id': 0, 'split_idx_start': 0, '_split_overlap': [{'doc_id': 'bc96123ee5a386c553cb2028130b7cc84765538fd433d27dc8ade3ab8056f371', 'range': (0, 677)}]}
[1] content_len=3056 meta={'file_path': 'Pravila-priema-2025-bakalavriat.pdf', 'source_id': 'f2cdb91300f837f8b1bfd6088e5946523d97a983ec70a7bca80f531d2ce40466', 'page_number': 2, 'split_id': 1, 'split_idx_start': 2231, '_split_overlap': [{'doc_id': '86a958f36e5989a9fdf9ef770d4f762ee2c5eadeaf15cc9eff63a6839f5c0c49', 'range': (2231, 2908)}, {'doc_id': 'ef8edf5acc04200d33bd9f231275b0397e2cb1f85b4af03d50f29003e33d175c', 'range': (0, 717)}]}
[2] content_len=2968 meta={'file_path': 'Pravila-priema-2025-bakalavriat.pdf', 'source_id': 'f2cdb91300f837f8b1bfd6088e5946523d97a983ec70a7bca80f531d2ce40466', 'page_number': 2, 'split_id': 2, 'split_idx_start': 4570, '_split_overlap': [{'doc_id': 'bc96123ee5a386c553cb2028130b7cc84765538fd433d27dc8ade3ab8056f371', 'range': (2339, 3056)}, {'doc_id': '27508d1d5b3db7089cc46a692eb189ffe92b4bce3d0dab70187a085e76c3feaa', 'range': (0, 581)}]}
[3] content_len=2592 meta={'file_path': 'Pravila-priema-2025-bakalavriat.pdf', 'source_id': 'f2cdb91300f837f8b1bfd6088e5946523d97a983ec70a7bca80f531d2ce40466', 'page_number': 3, 'split_id': 3, 'split_idx_start': 6957, '_split_overlap': [{'doc_id': 'ef8edf5acc04200d33bd9f231275b0397e2cb1f85b4af03d50f29003e33d175c', 'range': (2387, 2968)}, {'doc_id': '969ddd1215444183426f8ecf180461cceb5d1751b84eebfbe2999d0c440979c8', 'range': (0, 628)}]}
[4] content_len=2798 meta={'file_path': 'Pravila-priema-2025-bakalavriat.pdf', 'source_id': 'f2cdb91300f837f8b1bfd6088e5946523d97a983ec70a7bca80f531d2ce40466', 'page_number': 4, 'split_id': 4, 'split_idx_start': 8921, '_split_overlap': [{'doc_id': '27508d1d5b3db7089cc46a692eb189ffe92b4bce3d0dab70187a085e76c3feaa', 'range': (1964, 2592)}, {'doc_id': 'ed6a3ca992daf9c7e32870b188d07d0a3779f178f27ad319289bd2652aa840fc', 'range': (0, 607)}]}
[5] content_len=2768 meta={'file_path': 'Pravila-priema-2025-bakalavriat.pdf', 'source_id': 'f2cdb91300f837f8b1bfd6088e5946523d97a983ec70a7bca80f531d2ce40466', 'page_number': 5, 'split_id': 5, 'split_idx_start': 11112, '_split_overlap': [{'doc_id': '969ddd1215444183426f8ecf180461cceb5d1751b84eebfbe2999d0c440979c8', 'range': (2191, 2798)}, {'doc_id': '92a2827b83d1772006af28712042cc25ba979feb7710cf65acb2a163d5262e18', 'range': (0, 639)}]}
[6] content_len=2845 meta={'file_path': 'Pravila-priema-2025-bakalavriat.pdf', 'source_id': 'f2cdb91300f837f8b1bfd6088e5946523d97a983ec70a7bca80f531d2ce40466', 'page_number': 6, 'split_id': 6, 'split_idx_start': 13241, '_split_overlap': [{'doc_id': 'ed6a3ca992daf9c7e32870b188d07d0a3779f178f27ad319289bd2652aa840fc', 'range': (2129, 2768)}, {'doc_id': '068a6511716bf8b78315bd10023df9f8867084845624f9dcaff697a446193969', 'range': (0, 727)}]}
[7] content_len=3035 meta={'file_path': 'Pravila-priema-2025-bakalavriat.pdf', 'source_id': 'f2cdb91300f837f8b1bfd6088e5946523d97a983ec70a7bca80f531d2ce40466', 'page_number': 7, 'split_id': 7, 'split_idx_start': 15359, '_split_overlap': [{'doc_id': '92a2827b83d1772006af28712042cc25ba979feb7710cf65acb2a163d5262e18', 'range': (2118, 2845)}, {'doc_id': '6620b805713d7d44057cd57f5869f3f82c3a24a2b0e4be27f8c129cf3a724a1a', 'range': (0, 690)}]}
[8] content_len=2970 meta={'file_path': 'Pravila-priema-2025-bakalavriat.pdf', 'source_id': 'f2cdb91300f837f8b1bfd6088e5946523d97a983ec70a7bca80f531d2ce40466', 'page_number': 8, 'split_id': 8, 'split_idx_start': 17704, '_split_overlap': [{'doc_id': '068a6511716bf8b78315bd10023df9f8867084845624f9dcaff697a446193969', 'range': (2345, 3035)}, {'doc_id': 'f4b3fb3f8c585d4faf1369928e66d86084cc03bb0957a5005e3e660ae758eab4', 'range': (0, 588)}]}
[9] content_len=2664 meta={'file_path': 'Pravila-priema-2025-bakalavriat.pdf', 'source_id': 'f2cdb91300f837f8b1bfd6088e5946523d97a983ec70a7bca80f531d2ce40466', 'page_number': 9, 'split_id': 9, 'split_idx_start': 20086, '_split_overlap': [{'doc_id': '6620b805713d7d44057cd57f5869f3f82c3a24a2b0e4be27f8c129cf3a724a1a', 'range': (2382, 2970)}, {'doc_id': '30793a4c7db2563ccd0ed9341c305e204743ce0c9f643dc1e2b91908a6825614', 'range': (0, 778)}]}
[10] content_len=3055 meta={'file_path': 'Pravila-priema-2025-bakalavriat.pdf', 'source_id': 'f2cdb91300f837f8b1bfd6088e5946523d97a983ec70a7bca80f531d2ce40466', 'page_number': 9, 'split_id': 10, 'split_idx_start': 21972, '_split_overlap': [{'doc_id': 'f4b3fb3f8c585d4faf1369928e66d86084cc03bb0957a5005e3e660ae758eab4', 'range': (1886, 2664)}, {'doc_id': 'bef44fa0efcf22a9966d98347392ed291f8305911f4ca7bd041cb67faf353c24', 'range': (0, 625)}]}
[11] content_len=2854 meta={'file_path': 'Pravila-priema-2025-bakalavriat.pdf', 'source_id': 'f2cdb91300f837f8b1bfd6088e5946523d97a983ec70a7bca80f531d2ce40466', 'page_number': 10, 'split_id': 11, 'split_idx_start': 24402, '_split_overlap': [{'doc_id': '30793a4c7db2563ccd0ed9341c305e204743ce0c9f643dc1e2b91908a6825614', 'range': (2430, 3055)}, {'doc_id': '7ec8bb26c629246d55df32c778676185406ec281cfab08fc7cdf79ee6202e9b9', 'range': (0, 647)}]}
[12] content_len=3008 meta={'file_path': 'Pravila-priema-2025-bakalavriat.pdf', 'source_id': 'f2cdb91300f837f8b1bfd6088e5946523d97a983ec70a7bca80f531d2ce40466', 'page_number': 11, 'split_id': 12, 'split_idx_start': 26609, '_split_overlap': [{'doc_id': 'bef44fa0efcf22a9966d98347392ed291f8305911f4ca7bd041cb67faf353c24', 'range': (2207, 2854)}, {'doc_id': '9ca2125ddf48e1c2e4dcf39e3cf79dca9bdbaed4662c21caa3d967c36946df83', 'range': (0, 646)}]}
[13] content_len=2781 meta={'file_path': 'Pravila-priema-2025-bakalavriat.pdf', 'source_id': 'f2cdb91300f837f8b1bfd6088e5946523d97a983ec70a7bca80f531d2ce40466', 'page_number': 12, 'split_id': 13, 'split_idx_start': 28971, '_split_overlap': [{'doc_id': '7ec8bb26c629246d55df32c778676185406ec281cfab08fc7cdf79ee6202e9b9', 'range': (2362, 3008)}, {'doc_id': '81734a39c32bd122b611ba6c16759a4de8e736cf20ea2ca0737fe83b544cd493', 'range': (0, 617)}]}
[14] content_len=2715 meta={'file_path': 'Pravila-priema-2025-bakalavriat.pdf', 'source_id': 'f2cdb91300f837f8b1bfd6088e5946523d97a983ec70a7bca80f531d2ce40466', 'page_number': 13, 'split_id': 14, 'split_idx_start': 31135, '_split_overlap': [{'doc_id': '9ca2125ddf48e1c2e4dcf39e3cf79dca9bdbaed4662c21caa3d967c36946df83', 'range': (2164, 2781)}, {'doc_id': '55d527bfac9f9ad893b06d176de11bb6044ff4d8f669beb8d36b3c306c762b43', 'range': (0, 649)}]}
[15] content_len=2839 meta={'file_path': 'Pravila-priema-2025-bakalavriat.pdf', 'source_id': 'f2cdb91300f837f8b1bfd6088e5946523d97a983ec70a7bca80f531d2ce40466', 'page_number': 14, 'split_id': 15, 'split_idx_start': 33201, '_split_overlap': [{'doc_id': '81734a39c32bd122b611ba6c16759a4de8e736cf20ea2ca0737fe83b544cd493', 'range': (2066, 2715)}, {'doc_id': 'b27f72d4add7425dcb0a77b63cac05df957edcd7c67ba13b2de8591fabb7a3b1', 'range': (0, 622)}]}
[16] content_len=2716 meta={'file_path': 'Pravila-priema-2025-bakalavriat.pdf', 'source_id': 'f2cdb91300f837f8b1bfd6088e5946523d97a983ec70a7bca80f531d2ce40466', 'page_number': 15, 'split_id': 16, 'split_idx_start': 35418, '_split_overlap': [{'doc_id': '55d527bfac9f9ad893b06d176de11bb6044ff4d8f669beb8d36b3c306c762b43', 'range': (2217, 2839)}, {'doc_id': '5c5a9822200e573331e34df8f8ba68963d17affbf3748ad9132372100f648bc0', 'range': (0, 696)}]}
[17] content_len=3133 meta={'file_path': 'Pravila-priema-2025-bakalavriat.pdf', 'source_id': 'f2cdb91300f837f8b1bfd6088e5946523d97a983ec70a7bca80f531d2ce40466', 'page_number': 15, 'split_id': 17, 'split_idx_start': 37438, '_split_overlap': [{'doc_id': 'b27f72d4add7425dcb0a77b63cac05df957edcd7c67ba13b2de8591fabb7a3b1', 'range': (2020, 2716)}, {'doc_id': 'c3761f7c55afc872ee89edecbef525e045215d4385676762c8312f9114db6bac', 'range': (0, 738)}]}
[18] content_len=2834 meta={'file_path': 'Pravila-priema-2025-bakalavriat.pdf', 'source_id': 'f2cdb91300f837f8b1bfd6088e5946523d97a983ec70a7bca80f531d2ce40466', 'page_number': 16, 'split_id': 18, 'split_idx_start': 39833, '_split_overlap': [{'doc_id': '5c5a9822200e573331e34df8f8ba68963d17affbf3748ad9132372100f648bc0', 'range': (2395, 3133)}, {'doc_id': '319d29d94660542eecbe291905af9424abafee468af66014199d97e7df6543e6', 'range': (0, 527)}]}
[19] content_len=2694 meta={'file_path': 'Pravila-priema-2025-bakalavriat.pdf', 'source_id': 'f2cdb91300f837f8b1bfd6088e5946523d97a983ec70a7bca80f531d2ce40466', 'page_number': 17, 'split_id': 19, 'split_idx_start': 42140, '_split_overlap': [{'doc_id': 'c3761f7c55afc872ee89edecbef525e045215d4385676762c8312f9114db6bac', 'range': (2307, 2834)}, {'doc_id': '57c69b84d9af76d8cb7a98690cc4226ec714d0901126d964a4645793235617fc', 'range': (0, 599)}]}
[20] content_len=2762 meta={'file_path': 'Pravila-priema-2025-bakalavriat.pdf', 'source_id': 'f2cdb91300f837f8b1bfd6088e5946523d97a983ec70a7bca80f531d2ce40466', 'page_number': 18, 'split_id': 20, 'split_idx_start': 44235, '_split_overlap': [{'doc_id': '319d29d94660542eecbe291905af9424abafee468af66014199d97e7df6543e6', 'range': (2095, 2694)}, {'doc_id': '6f3228aaf871caeb8c4da85de461a82d96155bc0bd6bfd7bdb6cb8157c63f1a9', 'range': (0, 702)}]}
[21] content_len=2768 meta={'file_path': 'Pravila-priema-2025-bakalavriat.pdf', 'source_id': 'f2cdb91300f837f8b1bfd6088e5946523d97a983ec70a7bca80f531d2ce40466', 'page_number': 19, 'split_id': 21, 'split_idx_start': 46295, '_split_overlap': [{'doc_id': '57c69b84d9af76d8cb7a98690cc4226ec714d0901126d964a4645793235617fc', 'range': (2060, 2762)}, {'doc_id': 'ec3d0b569474ed050ad6bee3207bea8882e96ac1a4471da86ca988f6129e03da', 'range': (0, 664)}]}
[22] content_len=2785 meta={'file_path': 'Pravila-priema-2025-bakalavriat.pdf', 'source_id': 'f2cdb91300f837f8b1bfd6088e5946523d97a983ec70a7bca80f531d2ce40466', 'page_number': 19, 'split_id': 22, 'split_idx_start': 48399, '_split_overlap': [{'doc_id': '6f3228aaf871caeb8c4da85de461a82d96155bc0bd6bfd7bdb6cb8157c63f1a9', 'range': (2104, 2768)}, {'doc_id': 'b30e0d50635d436e75946680b197fa2565c1456766dfb399ca1490c16b45e3db', 'range': (0, 612)}]}
[23] content_len=2786 meta={'file_path': 'Pravila-priema-2025-bakalavriat.pdf', 'source_id': 'f2cdb91300f837f8b1bfd6088e5946523d97a983ec70a7bca80f531d2ce40466', 'page_number': 20, 'split_id': 23, 'split_idx_start': 50572, '_split_overlap': [{'doc_id': 'ec3d0b569474ed050ad6bee3207bea8882e96ac1a4471da86ca988f6129e03da', 'range': (2173, 2785)}, {'doc_id': '1c79415253dc6cf6ea6ab22e25dc7ab189dd7bd2b3a3055fc0b549f631f6d307', 'range': (0, 639)}]}
[24] content_len=2708 meta={'file_path': 'Pravila-priema-2025-bakalavriat.pdf', 'source_id': 'f2cdb91300f837f8b1bfd6088e5946523d97a983ec70a7bca80f531d2ce40466', 'page_number': 21, 'split_id': 24, 'split_idx_start': 52719, '_split_overlap': [{'doc_id': 'b30e0d50635d436e75946680b197fa2565c1456766dfb399ca1490c16b45e3db', 'range': (2147, 2786)}, {'doc_id': 'ba8cd89ce8c352d00130421e3526744b406028317227830345c3ebf8f9f44876', 'range': (0, 582)}]}
[25] content_len=2821 meta={'file_path': 'Pravila-priema-2025-bakalavriat.pdf', 'source_id': 'f2cdb91300f837f8b1bfd6088e5946523d97a983ec70a7bca80f531d2ce40466', 'page_number': 22, 'split_id': 25, 'split_idx_start': 54845, '_split_overlap': [{'doc_id': '1c79415253dc6cf6ea6ab22e25dc7ab189dd7bd2b3a3055fc0b549f631f6d307', 'range': (2126, 2708)}, {'doc_id': '0cd167fb10d84d40515c2c26b9a298fd1df8aebe553cb9cbeffdf96931a72e8b', 'range': (0, 584)}]}
[26] content_len=2543 meta={'file_path': 'Pravila-priema-2025-bakalavriat.pdf', 'source_id': 'f2cdb91300f837f8b1bfd6088e5946523d97a983ec70a7bca80f531d2ce40466', 'page_number': 23, 'split_id': 26, 'split_idx_start': 57082, '_split_overlap': [{'doc_id': 'ba8cd89ce8c352d00130421e3526744b406028317227830345c3ebf8f9f44876', 'range': (2237, 2821)}, {'doc_id': '3686affbbf63ef5483ff297dfa2060a640c6a30b9c5f84bf0283646526f1f4d9', 'range': (0, 599)}]}
[27] content_len=2655 meta={'file_path': 'Pravila-priema-2025-bakalavriat.pdf', 'source_id': 'f2cdb91300f837f8b1bfd6088e5946523d97a983ec70a7bca80f531d2ce40466', 'page_number': 23, 'split_id': 27, 'split_idx_start': 59026, '_split_overlap': [{'doc_id': '0cd167fb10d84d40515c2c26b9a298fd1df8aebe553cb9cbeffdf96931a72e8b', 'range': (1944, 2543)}, {'doc_id': 'c4b3e5a4c2d23be6e5549a790faa2f260de91a694f850807b9f627491746fa7f', 'range': (0, 603)}]}
[28] content_len=2748 meta={'file_path': 'Pravila-priema-2025-bakalavriat.pdf', 'source_id': 'f2cdb91300f837f8b1bfd6088e5946523d97a983ec70a7bca80f531d2ce40466', 'page_number': 24, 'split_id': 28, 'split_idx_start': 61078, '_split_overlap': [{'doc_id': '3686affbbf63ef5483ff297dfa2060a640c6a30b9c5f84bf0283646526f1f4d9', 'range': (2052, 2655)}, {'doc_id': '678aaa3711b09e174994aa6f41d00240dae48f4577a993945c7569dd7b06fbb3', 'range': (0, 612)}]}
[29] content_len=2683 meta={'file_path': 'Pravila-priema-2025-bakalavriat.pdf', 'source_id': 'f2cdb91300f837f8b1bfd6088e5946523d97a983ec70a7bca80f531d2ce40466', 'page_number': 25, 'split_id': 29, 'split_idx_start': 63214, '_split_overlap': [{'doc_id': 'c4b3e5a4c2d23be6e5549a790faa2f260de91a694f850807b9f627491746fa7f', 'range': (2136, 2748)}, {'doc_id': '3843cb50339deed22ec0bc173f95f189789720b60b007b1c5ac949d6f9db843d', 'range': (0, 596)}]}
[30] content_len=2717 meta={'file_path': 'Pravila-priema-2025-bakalavriat.pdf', 'source_id': 'f2cdb91300f837f8b1bfd6088e5946523d97a983ec70a7bca80f531d2ce40466', 'page_number': 26, 'split_id': 30, 'split_idx_start': 65301, '_split_overlap': [{'doc_id': '678aaa3711b09e174994aa6f41d00240dae48f4577a993945c7569dd7b06fbb3', 'range': (2087, 2683)}, {'doc_id': '4239ed9641037b9b030b8e1de578690d0cd110058813831ec481f43859d5b0fc', 'range': (0, 633)}]}
[31] content_len=2702 meta={'file_path': 'Pravila-priema-2025-bakalavriat.pdf', 'source_id': 'f2cdb91300f837f8b1bfd6088e5946523d97a983ec70a7bca80f531d2ce40466', 'page_number': 27, 'split_id': 31, 'split_idx_start': 67385, '_split_overlap': [{'doc_id': '3843cb50339deed22ec0bc173f95f189789720b60b007b1c5ac949d6f9db843d', 'range': (2084, 2717)}, {'doc_id': '18bdea0653ab196f03bd9b5a2ed554495f0d143ad9ab344ed06ca264e70f597b', 'range': (0, 621)}]}
[32] content_len=2616 meta={'file_path': 'Pravila-priema-2025-bakalavriat.pdf', 'source_id': 'f2cdb91300f837f8b1bfd6088e5946523d97a983ec70a7bca80f531d2ce40466', 'page_number': 28, 'split_id': 32, 'split_idx_start': 69466, '_split_overlap': [{'doc_id': '4239ed9641037b9b030b8e1de578690d0cd110058813831ec481f43859d5b0fc', 'range': (2081, 2702)}, {'doc_id': '520fe54273dd618c6d5a564810a01cd19246043cb7514732aeb286e6a140acaa', 'range': (0, 584)}]}
[33] content_len=2462 meta={'file_path': 'Pravila-priema-2025-bakalavriat.pdf', 'source_id': 'f2cdb91300f837f8b1bfd6088e5946523d97a983ec70a7bca80f531d2ce40466', 'page_number': 28, 'split_id': 33, 'split_idx_start': 71498, '_split_overlap': [{'doc_id': '18bdea0653ab196f03bd9b5a2ed554495f0d143ad9ab344ed06ca264e70f597b', 'range': (2032, 2616)}, {'doc_id': '356f4e35b87cf4b885080a82fef371fab19d2b998d1e0542ff8b47494d166c37', 'range': (0, 513)}]}
[34] content_len=2558 meta={'file_path': 'Pravila-priema-2025-bakalavriat.pdf', 'source_id': 'f2cdb91300f837f8b1bfd6088e5946523d97a983ec70a7bca80f531d2ce40466', 'page_number': 29, 'split_id': 34, 'split_idx_start': 73447, '_split_overlap': [{'doc_id': '520fe54273dd618c6d5a564810a01cd19246043cb7514732aeb286e6a140acaa', 'range': (1949, 2462)}, {'doc_id': '0280e3a1f9e62544c3d69b5ff47f43efb3091410c95ee67b94ea34734ae2e7e0', 'range': (0, 565)}]}
[35] content_len=2453 meta={'file_path': 'Pravila-priema-2025-bakalavriat.pdf', 'source_id': 'f2cdb91300f837f8b1bfd6088e5946523d97a983ec70a7bca80f531d2ce40466', 'page_number': 30, 'split_id': 35, 'split_idx_start': 75440, '_split_overlap': [{'doc_id': '356f4e35b87cf4b885080a82fef371fab19d2b998d1e0542ff8b47494d166c37', 'range': (1993, 2558)}, {'doc_id': 'cfed6a46de80974a2491a4d001aaf7e26f77b7d701e6a0a7b97dd1cf650feb11', 'range': (0, 562)}]}
[36] content_len=2627 meta={'file_path': 'Pravila-priema-2025-bakalavriat.pdf', 'source_id': 'f2cdb91300f837f8b1bfd6088e5946523d97a983ec70a7bca80f531d2ce40466', 'page_number': 31, 'split_id': 36, 'split_idx_start': 77331, '_split_overlap': [{'doc_id': '0280e3a1f9e62544c3d69b5ff47f43efb3091410c95ee67b94ea34734ae2e7e0', 'range': (1891, 2453)}, {'doc_id': '3c83100f0defc6b1c8cf3ce771ff5ecfba69505b83d47e27f7f3d7f7bb90298f', 'range': (0, 616)}]}
[37] content_len=2736 meta={'file_path': 'Pravila-priema-2025-bakalavriat.pdf', 'source_id': 'f2cdb91300f837f8b1bfd6088e5946523d97a983ec70a7bca80f531d2ce40466', 'page_number': 31, 'split_id': 37, 'split_idx_start': 79342, '_split_overlap': [{'doc_id': 'cfed6a46de80974a2491a4d001aaf7e26f77b7d701e6a0a7b97dd1cf650feb11', 'range': (2011, 2627)}, {'doc_id': '7239dccdc1a73fa56827a0254679366f43207f3ad3617cc97e4d154601bff224', 'range': (0, 614)}]}
[38] content_len=2745 meta={'file_path': 'Pravila-priema-2025-bakalavriat.pdf', 'source_id': 'f2cdb91300f837f8b1bfd6088e5946523d97a983ec70a7bca80f531d2ce40466', 'page_number': 32, 'split_id': 38, 'split_idx_start': 81464, '_split_overlap': [{'doc_id': '3c83100f0defc6b1c8cf3ce771ff5ecfba69505b83d47e27f7f3d7f7bb90298f', 'range': (2122, 2736)}, {'doc_id': 'f6bab2808d5c3569479b8ab8987c1f4db6a7dbedfd369d5a59145fd2e2ca6e6e', 'range': (0, 633)}]}
[39] content_len=2542 meta={'file_path': 'Pravila-priema-2025-bakalavriat.pdf', 'source_id': 'f2cdb91300f837f8b1bfd6088e5946523d97a983ec70a7bca80f531d2ce40466', 'page_number': 33, 'split_id': 39, 'split_idx_start': 83576, '_split_overlap': [{'doc_id': '7239dccdc1a73fa56827a0254679366f43207f3ad3617cc97e4d154601bff224', 'range': (2112, 2745)}, {'doc_id': '94ffe35877c3cfa0343f8fe79a8b0ad2ea8b4a0967069acf28fdeb1bc8893d11', 'range': (0, 573)}]}
[40] content_len=2454 meta={'file_path': 'Pravila-priema-2025-bakalavriat.pdf', 'source_id': 'f2cdb91300f837f8b1bfd6088e5946523d97a983ec70a7bca80f531d2ce40466', 'page_number': 34, 'split_id': 40, 'split_idx_start': 85545, '_split_overlap': [{'doc_id': 'f6bab2808d5c3569479b8ab8987c1f4db6a7dbedfd369d5a59145fd2e2ca6e6e', 'range': (1969, 2542)}, {'doc_id': '57e9456e134a838920a0b4359943a6baf6b001ee15e9fdb4fdc7e053af8ae284', 'range': (0, 565)}]}
[41] content_len=2786 meta={'file_path': 'Pravila-priema-2025-bakalavriat.pdf', 'source_id': 'f2cdb91300f837f8b1bfd6088e5946523d97a983ec70a7bca80f531d2ce40466', 'page_number': 35, 'split_id': 41, 'split_idx_start': 87434, '_split_overlap': [{'doc_id': '94ffe35877c3cfa0343f8fe79a8b0ad2ea8b4a0967069acf28fdeb1bc8893d11', 'range': (1889, 2454)}, {'doc_id': '206c648b7adb2735a4dd5b68d036be4c8215bf49fa1aa956d4b18c4d3aa67e70', 'range': (0, 645)}]}
[42] content_len=3151 meta={'file_path': 'Pravila-priema-2025-bakalavriat.pdf', 'source_id': 'f2cdb91300f837f8b1bfd6088e5946523d97a983ec70a7bca80f531d2ce40466', 'page_number': 36, 'split_id': 42, 'split_idx_start': 89575, '_split_overlap': [{'doc_id': '57e9456e134a838920a0b4359943a6baf6b001ee15e9fdb4fdc7e053af8ae284', 'range': (2141, 2786)}, {'doc_id': 'a19851162141b35475a72c573389b022841523d7f25ece2963033d380692ca9b', 'range': (0, 797)}]}
[43] content_len=2962 meta={'file_path': 'Pravila-priema-2025-bakalavriat.pdf', 'source_id': 'f2cdb91300f837f8b1bfd6088e5946523d97a983ec70a7bca80f531d2ce40466', 'page_number': 37, 'split_id': 43, 'split_idx_start': 91929, '_split_overlap': [{'doc_id': '206c648b7adb2735a4dd5b68d036be4c8215bf49fa1aa956d4b18c4d3aa67e70', 'range': (2354, 3151)}, {'doc_id': '24087f6730da8c700fa37bf23ae59a85e49e3ba447478b36b174edccc046e09d', 'range': (0, 627)}]}
[44] content_len=2787 meta={'file_path': 'Pravila-priema-2025-bakalavriat.pdf', 'source_id': 'f2cdb91300f837f8b1bfd6088e5946523d97a983ec70a7bca80f531d2ce40466', 'page_number': 38, 'split_id': 44, 'split_idx_start': 94264, '_split_overlap': [{'doc_id': 'a19851162141b35475a72c573389b022841523d7f25ece2963033d380692ca9b', 'range': (2335, 2962)}, {'doc_id': '4b9b2dd95cc022a0b3fb42440cfb4ad6474d7f7a0df468dd72a62bc59eff7fbf', 'range': (0, 698)}]}
[45] content_len=2892 meta={'file_path': 'Pravila-priema-2025-bakalavriat.pdf', 'source_id': 'f2cdb91300f837f8b1bfd6088e5946523d97a983ec70a7bca80f531d2ce40466', 'page_number': 38, 'split_id': 45, 'split_idx_start': 96353, '_split_overlap': [{'doc_id': '24087f6730da8c700fa37bf23ae59a85e49e3ba447478b36b174edccc046e09d', 'range': (2089, 2787)}, {'doc_id': '6e7c20f287c6159bdefbef4f4c8b9b69690ac4d22bd3a342364a9660e2b77162', 'range': (0, 677)}]}
[46] content_len=2727 meta={'file_path': 'Pravila-priema-2025-bakalavriat.pdf', 'source_id': 'f2cdb91300f837f8b1bfd6088e5946523d97a983ec70a7bca80f531d2ce40466', 'page_number': 39, 'split_id': 46, 'split_idx_start': 98568, '_split_overlap': [{'doc_id': '4b9b2dd95cc022a0b3fb42440cfb4ad6474d7f7a0df468dd72a62bc59eff7fbf', 'range': (2215, 2892)}, {'doc_id': '1f04f45c7cdd65bff1125e509c850c99800830bdd208662c37e7a7232085e6fa', 'range': (0, 545)}]}
[47] content_len=2652 meta={'file_path': 'Pravila-priema-2025-bakalavriat.pdf', 'source_id': 'f2cdb91300f837f8b1bfd6088e5946523d97a983ec70a7bca80f531d2ce40466', 'page_number': 40, 'split_id': 47, 'split_idx_start': 100750, '_split_overlap': [{'doc_id': '6e7c20f287c6159bdefbef4f4c8b9b69690ac4d22bd3a342364a9660e2b77162', 'range': (2182, 2727)}, {'doc_id': 'e22b868042a41350318f7a8b26c3578eba08685da23a64a510b696552c79c2c4', 'range': (0, 701)}]}
[48] content_len=2824 meta={'file_path': 'Pravila-priema-2025-bakalavriat.pdf', 'source_id': 'f2cdb91300f837f8b1bfd6088e5946523d97a983ec70a7bca80f531d2ce40466', 'page_number': 41, 'split_id': 48, 'split_idx_start': 102701, '_split_overlap': [{'doc_id': '1f04f45c7cdd65bff1125e509c850c99800830bdd208662c37e7a7232085e6fa', 'range': (1951, 2652)}, {'doc_id': '29cb8b162a32f4a75f72eacc01ca2a0329546c33165b52965e77b3a28c3b2747', 'range': (0, 654)}]}
[49] content_len=2834 meta={'file_path': 'Pravila-priema-2025-bakalavriat.pdf', 'source_id': 'f2cdb91300f837f8b1bfd6088e5946523d97a983ec70a7bca80f531d2ce40466', 'page_number': 42, 'split_id': 49, 'split_idx_start': 104871, '_split_overlap': [{'doc_id': 'e22b868042a41350318f7a8b26c3578eba08685da23a64a510b696552c79c2c4', 'range': (2170, 2824)}, {'doc_id': 'f7915534024dd25a134a5217cb9955977b3ff15acd4961d6de903c0f8378c204', 'range': (0, 622)}]}
[50] content_len=2768 meta={'file_path': 'Pravila-priema-2025-bakalavriat.pdf', 'source_id': 'f2cdb91300f837f8b1bfd6088e5946523d97a983ec70a7bca80f531d2ce40466', 'page_number': 43, 'split_id': 50, 'split_idx_start': 107083, '_split_overlap': [{'doc_id': '29cb8b162a32f4a75f72eacc01ca2a0329546c33165b52965e77b3a28c3b2747', 'range': (2212, 2834)}, {'doc_id': 'e68bc7c6390600637ca7f9dd5070d48aa7deb914defa1ce83909e0cc3f24d59f', 'range': (0, 607)}]}
[51] content_len=2753 meta={'file_path': 'Pravila-priema-2025-bakalavriat.pdf', 'source_id': 'f2cdb91300f837f8b1bfd6088e5946523d97a983ec70a7bca80f531d2ce40466', 'page_number': 43, 'split_id': 51, 'split_idx_start': 109244, '_split_overlap': [{'doc_id': 'f7915534024dd25a134a5217cb9955977b3ff15acd4961d6de903c0f8378c204', 'range': (2161, 2768)}, {'doc_id': 'cce979f01e0ea7894f6168880de0afd2972f1436d1bbe774e5739660e6ca6d01', 'range': (0, 656)}]}
[52] content_len=2955 meta={'file_path': 'Pravila-priema-2025-bakalavriat.pdf', 'source_id': 'f2cdb91300f837f8b1bfd6088e5946523d97a983ec70a7bca80f531d2ce40466', 'page_number': 44, 'split_id': 52, 'split_idx_start': 111341, '_split_overlap': [{'doc_id': 'e68bc7c6390600637ca7f9dd5070d48aa7deb914defa1ce83909e0cc3f24d59f', 'range': (2097, 2753)}, {'doc_id': '1892c5e3029672a2134223c74b6dc31702c2035826655026e194e6b2e948606c', 'range': (0, 656)}]}
[53] content_len=2706 meta={'file_path': 'Pravila-priema-2025-bakalavriat.pdf', 'source_id': 'f2cdb91300f837f8b1bfd6088e5946523d97a983ec70a7bca80f531d2ce40466', 'page_number': 45, 'split_id': 53, 'split_idx_start': 113640, '_split_overlap': [{'doc_id': 'cce979f01e0ea7894f6168880de0afd2972f1436d1bbe774e5739660e6ca6d01', 'range': (2299, 2955)}]}
Batches: 100%|██████████| 2/2 [00:01<00:00,  1.41it/s]
Unsafe mode is enabled. This allows execution of arbitrary code in the Jinja template. Use this only if you trust the source of the template.
Batches: 100%|██████████| 1/1 [00:00<00:00, 66.91it/s]
Batches: 100%|██████████| 1/1 [00:00<00:00, 79.62it/s]
Batches: 100%|██████████| 1/1 [00:00<00:00, 69.74it/s]
Batches: 100%|██████████| 1/1 [00:00<00:00, 75.08it/s]
Batches: 100%|██████████| 1/1 [00:00<00:00, 62.14it/s]
Batches: 100%|██████████| 1/1 [00:00<00:00, 75.71it/s]
Batches: 100%|██████████| 1/1 [00:00<00:00, 73.79it/s]
Batches: 100%|██████████| 1/1 [00:00<00:00, 69.89it/s]
Batches: 100%|██████████| 1/1 [00:00<00:00, 68.62it/s]
Batches: 100%|██████████| 1/1 [00:00<00:00, 72.16it/s]
Batches: 100%|██████████| 1/1 [00:00<00:00, 34.60it/s]
Batches: 100%|██████████| 1/1 [00:00<00:00, 88.68it/s]
Batches: 100%|██████████| 1/1 [00:00<00:00, 29.91it/s]
Batches: 100%|██████████| 1/1 [00:00<00:00, 86.51it/s]
Batches: 100%|██████████| 1/1 [00:00<00:00, 21.81it/s]
Batches: 100%|██████████| 1/1 [00:00<00:00, 62.03it/s]
Batches: 100%|██████████| 1/1 [00:00<00:00, 41.95it/s]
Batches: 100%|██████████| 1/1 [00:00<00:00, 35.49it/s]
Batches: 100%|██████████| 1/1 [00:00<00:00, 79.27it/s]
Batches: 100%|██████████| 1/1 [00:00<00:00, 32.97it/s]

Evaluating question 1/20

IR → Hit@1=0.0 | Hit@3=0.0 | P@1=0.000 | P@3=0.000 | MRR=0.000 | Rank=None
✅ ContextualPrecision: 0.000
🧠 Reason: The score is 0.00 because the first retrieval context node, despite containing detailed information about university admissions rules, does not directly answer the user's question about the documents needed to apply. The node focuses on the structure and content of a rules document, rather than the specific required paperwork, leading to a low precision score.
✅ ContextualRecall: 0.000
🧠 Reason: The score is 0.00 because the provided text outlines the required documents for applying to undergraduate and postgraduate programs at the Financial University, detailing various categories of documents and their specific requirements. This level of detail does not align with the retrieval context.


Evaluating question 2/20

IR → Hit@1=0.0 | Hit@3=0.0 | P@1=0.000 | P@3=0.000 | MRR=0.000 | Rank=None
✅ ContextualPrecision: 0.000
🧠 Reason: The score is 0.00 because the first retrieval context node, despite describing a formal admissions process with terms like 'конкурсные списки' and 'уникальный код поступающего', does not directly answer the question about 'сроки приёма документов'. The node focuses on the process itself rather than the specific timeframe for document submission, and the question is about the timeframe, not the process.
✅ ContextualRecall: 0.000
🧠 Reason: The score is 0.00 because the text provides a highly detailed and technical description of the admissions process for ЕПГУ, including specific dates, deadlines, and procedures for both budget and paid places. The information is tightly focused on the procedures and doesn't offer broader contextual information, leading to a low recall score.


Evaluating question 3/20


IR → Hit@1=0.0 | Hit@3=0.0 | P@1=0.000 | P@3=0.000 | MRR=0.000 | Rank=None
✅ ContextualPrecision: 0.000
🧠 Reason: The score is 0.00 because the first retrieval context node provides a detailed analysis of a complex legal document, which is irrelevant to the user's question about the number of specializations available when applying. The node focuses on admissions procedures and quota systems, failing to directly address the user's query about the number of specializations.
✅ ContextualRecall: 0.000
🧠 Reason: The score is 0.00 because the provided text lacks relevant information to the retrieval context, as indicated by the unsupportive reason referencing a 'comprehensive analysis' which doesn't connect to any specific sentences within the expected output or node(s) in retrieval context.

Evaluating question 4/20


IR → Hit@1=0.0 | Hit@3=0.0 | P@1=0.000 | P@3=0.000 | MRR=0.000 | Rank=None
✅ ContextualPrecision: 0.000
🧠 Reason: The score is 0.00 because the retrieval contexts primarily contain detailed explanations of the admissions process for the Financial University, focusing on regulations and procedures, rather than directly addressing the question about entrance tests (ЕГЭ, дополнительные экзамены). Specifically, nodes like 'Key Sections and Their Focus:' and 'General Admissions (Articles 55-69)' provide irrelevant information about university admissions, and the context's overall scope is far removed from the user's query.
✅ ContextualRecall: 0.000
🧠 Reason: The score is 0.00 because the provided text describes the admission process for Russian universities, including specific criteria and exemptions, but none of these details are directly linked to the retrieval context. The context lacks information about university admissions or related processes.

Evaluating question 5/20


IR → Hit@1=0.0 | Hit@3=0.0 | P@1=0.000 | P@3=0.000 | MRR=0.000 | Rank=None
✅ ContextualPrecision: 0.000
🧠 Reason: The score is 0.00 because the first retrieval context node, despite containing the word 'admissions', does not directly answer the question about minimum passing scores. The node focuses on the detailed rules and regulations of the Financial University's admissions process, which is a different topic than the user's query about passing grades.
✅ ContextualRecall: 0.000
🧠 Reason: The score is 0.00 because the provided text outlines minimum score requirements for various educational forms and payment types, lacking any direct connection to the retrieval context node(s).

Evaluating question 6/20

IR → Hit@1=0.0 | Hit@3=0.0 | P@1=0.000 | P@3=0.000 | MRR=0.000 | Rank=None
✅ ContextualPrecision: 0.000
🧠 Reason: The score is 0.00 because the first retrieval context node, despite being ranked first, does not address the user's question about targeted education or how to obtain it. Instead, it provides a detailed regulation about the admission process to the Financial University, focusing on administrative and procedural aspects, as stated in the 'reason' field.
✅ ContextualRecall: 0.000
🧠 Reason: The score is 0.00 because the text provides a detailed procedural guide for targeted education enrollment, including specific steps and deadlines, but lacks any connection to a retrieval context. The information focuses on the admissions process and requirements, without relating to any broader context.


Evaluating question 7/20


IR → Hit@1=0.0 | Hit@3=0.0 | P@1=0.000 | P@3=0.000 | MRR=0.000 | Rank=None
✅ ContextualPrecision: 0.000
🧠 Reason: The score is 0.00 because the first retrieval context node, which states "This document is a detailed regulation outlining the admission process for the Financial University," is irrelevant to the input question about budget places in Applied Machine Learning. The node does not contain information about budget places or the direction of Applied Machine Learning, and therefore, it should be ranked lower than nodes that do contain relevant information.
✅ ContextualRecall: 0.000
🧠 Reason: The score is 0.00 because the provided text only lists the number of budget places and paid educational services places, without any connection to the retrieval context node(s) in retrieval context.

Evaluating question 8/20

IR → Hit@1=0.0 | Hit@3=0.0 | P@1=0.000 | P@3=0.000 | MRR=0.000 | Rank=None
✅ ContextualPrecision: 0.000
🧠 Reason: The score is 0.00 because the first retrieval context node, a detailed regulation regarding admissions, is entirely irrelevant to the user's question about the cost of education and discounts. The node's content focuses on the structure and specifics of the Financial University's admissions process, while the input query asks about pricing and potential discounts, creating a significant mismatch in relevance.
✅ ContextualRecall: 0.000
🧠 Reason: The score is 0.00 because the provided text offers a detailed explanation of tuition costs and discounts, but lacks connection to any node(s) in retrieval context.


Evaluating question 9/20

IR → Hit@1=0.0 | Hit@3=0.0 | P@1=0.000 | P@3=0.000 | MRR=0.000 | Rank=None
✅ ContextualPrecision: 0.000
🧠 Reason: The score is 0.00 because the first node in the retrieval context, which states "The provided text is a complex legal document...", does not directly address the user's question about submitting documents online. The node's description is overly detailed and focuses on the document's nature rather than providing relevant information for answering the query, leading to a low score.
✅ ContextualRecall: 0.000
🧠 Reason: The score is 0.00 because the provided text describes how to submit documents online, specifically through the Gosuslugi portal and the university's personal account. However, none of the nodes in retrieval context relate to this process, and the unsupportive reason highlights the text's nature as a legal document, which is not present in the provided output.


Evaluating question 10/20

IR → Hit@1=0.0 | Hit@3=0.0 | P@1=0.000 | P@3=0.000 | MRR=0.000 | Rank=None
✅ ContextualPrecision: 0.000
🧠 Reason: The score is 0.00 because the first retrieval context node, despite describing a university's admission process, does not directly answer the question about the publication dates of contest lists and enrollment orders. The node focuses on the overall process, lacking the specific information requested in the input, and therefore, irrelevant nodes are ranked lower.
✅ ContextualRecall: 0.000
🧠 Reason: The score is 0.00 because the provided text describes the timing of publication of admission lists and acceptance orders by universities, referencing updates and publication periods, but lacks direct connection to any specific retrieval context node(s).


Evaluating question 11/20

IR → Hit@1=0.0 | Hit@3=0.0 | P@1=0.000 | P@3=0.000 | MRR=0.000 | Rank=None
✅ ContextualPrecision: 0.000
🧠 Reason: The score is 0.00 because the first retrieval context node, despite containing detailed information about university admissions regulations, does not directly address the user's question about preparatory courses and their cost. The node focuses on the legal framework for admissions, rather than providing practical information about courses themselves, leading to a low score.
✅ ContextualRecall: 0.000
🧠 Reason: The score is 0.00 because the expected output provides information about preparatory courses offered by universities, including details on cost, duration, and formats, but none of this information aligns with the retrieval context, which is dominated by legal regulations regarding university admissions (273-FZ).


Evaluating question 12/20

IR → Hit@1=0.0 | Hit@3=0.0 | P@1=0.000 | P@3=0.000 | MRR=0.000 | Rank=None
✅ ContextualPrecision: 0.000
🧠 Reason: The score is 0.00 because the first retrieval context node, a detailed legal document, does not directly address the question about student housing. The node's 'reason' states it outlines admission processes and regulations, which is irrelevant to the user's inquiry about housing provisions.
✅ ContextualRecall: 0.000
🧠 Reason: The score is 0.00 because the expected output provides specific details about dormitory availability for out-of-town students, including distance requirements and application procedures (sentence 1-2), which are not reflected in the retrieval context. The unsupportive reason highlights the document's formal nature, further distancing it from any potential relevance to the retrieval context.


Evaluating question 13/20


IR → Hit@1=0.0 | Hit@3=0.0 | P@1=0.000 | P@3=0.000 | MRR=0.000 | Rank=None
✅ ContextualPrecision: 0.000
🧠 Reason: The score is 0.00 because the first retrieval context node, which states 'The document is lengthy, detailed, and uses legal terminology, indicating its purpose as a formal set of rules governing the admissions process.', does not directly address the user's question about benefits and rights related to admissions, such as those concerning olympiads or disabilities. The node's focus on the document's structure and legal nature makes it irrelevant to the query's specific request.
✅ ContextualRecall: 0.000
🧠 Reason: The score is 0.00 because the provided text is a lengthy legal description of benefits and rights related to university admissions, referencing specific legislation and regulations (Federal Law No. 273-FZ), and does not align with any retrieval context. The document's detailed nature and use of legal terminology suggests a lack of relevance to the retrieval context.

Evaluating question 14/20


IR → Hit@1=0.0 | Hit@3=0.0 | P@1=0.000 | P@3=0.000 | MRR=0.000 | Rank=None
✅ ContextualPrecision: 0.000
🧠 Reason: The score is 0.00 because the retrieval contexts primarily contain a detailed legal document about university admissions, and the input question is about transferring between tuition types. The first node in the retrieval contexts, 'The provided text is a legal document...', does not address the core query about transferring between educational funding options, and therefore the irrelevant nodes are ranked higher than the relevant ones.
✅ ContextualRecall: 0.000
🧠 Reason: The score is 0.00 because the expected output describes a process for transferring from paid to subsidized education within a university, detailing conditions and procedures, but there's no direct connection to any node(s) in retrieval context.

Evaluating question 15/20


IR → Hit@1=0.0 | Hit@3=0.0 | P@1=0.000 | P@3=0.000 | MRR=0.000 | Rank=None
✅ ContextualPrecision: 0.000
🧠 Reason: The score is 0.00 because the retrieval contexts primarily discuss university admission procedures and ranking criteria, which doesn't directly address the question about studying part-time or full-time. Specifically, the first node states, "The text outlines procedures for application, ranking, and admission, including specific priorities and criteria for evaluating candidates," and this is not relevant to the user's query about learning opportunities.
✅ ContextualRecall: 0.000
🧠 Reason: The score is 0.00 because the provided text simply states that the form of study depends on the field of study and offers resources for finding information, lacking any connection to the retrieval context node(s).

Evaluating question 16/20

IR → Hit@1=0.0 | Hit@3=0.0 | P@1=0.000 | P@3=0.000 | MRR=0.000 | Rank=None
✅ ContextualPrecision: 0.000
🧠 Reason: The score is 0.00 because the retrieval contexts primarily contain a legal document detailing university admission procedures, and this document does not directly answer the question about the duration of study for a specific program. Specifically, the node's 'reason' states, "The text's structure, terminology, and focus on specific dates, quotas, and ranking methods strongly indicate a legal or regulatory document related to university admissions."
✅ ContextualRecall: 0.000
🧠 Reason: The score is 0.00 because the text provides a straightforward explanation of educational program durations across different levels (бакалавриат, специалитет, магистратура) – node(s) in retrieval context do not address this specific information about academic program timelines.


Evaluating question 17/20

IR → Hit@1=0.0 | Hit@3=0.0 | P@1=0.000 | P@3=0.000 | MRR=0.000 | Rank=None
✅ ContextualPrecision: 0.000
🧠 Reason: The score is 0.00 because the first retrieval context node, which states "The text is dense with legal terms, references to specific articles of a law (Federal Law No. 273-FZ), and detailed procedures," is not directly relevant to the user's question about a military department in a university. The node focuses on a complex legal document, while the input query is a simple inquiry about the existence of a specific academic department.
✅ ContextualRecall: 0.000
🧠 Reason: The score is 0.00 because the provided text describes the operation of a military training center at the Financial University, detailing training programs for sergeants and officers. However, there are no relevant node(s) in retrieval context to directly relate to this information, resulting in a low contextual recall score.


Evaluating question 18/20


IR → Hit@1=0.0 | Hit@3=0.0 | P@1=0.000 | P@3=0.000 | MRR=0.000 | Rank=None
✅ ContextualPrecision: 0.000
🧠 Reason: The score is 0.00 because the first retrieval context node, despite containing information about admissions processes, does not directly address the input question about internship and employment opportunities offered by the university. The node focuses on the rules and regulations governing admissions, including olympiad results, which is a tangential topic and fails to provide relevant information about the university's offerings for internships and employment.
✅ ContextualRecall: 0.000
🧠 Reason: The score is 0.00 because the provided text describes career services offered by a university (node(s) in retrieval context), including internships, career events, and job placement assistance, but it doesn't align with the expected output's focus on olympiad results and special privileges.

Evaluating question 19/20


IR → Hit@1=0.0 | Hit@3=0.0 | P@1=0.000 | P@3=0.000 | MRR=0.000 | Rank=None
✅ ContextualPrecision: 0.000
🧠 Reason: The score is 0.00 because the retrieval contexts, particularly the first node, are overly descriptive and focus on the document's structure and legal nature, rather than directly addressing the user's question about changing a direction after submitting an application. The subsequent nodes, while providing further details about the document, do not offer relevant information to answer the query, and the nodes are ranked in a way that prioritizes these irrelevant descriptions.
✅ ContextualRecall: 0.000
🧠 Reason: The score is 0.00 because the provided text is a detailed procedural document outlining changes and procedures related to admissions, with no clear connection to a retrieval context. Node(s) in retrieval context do not contain information relevant to the specifics of the document's content.

Evaluating question 20/20

IR → Hit@1=0.0 | Hit@3=0.0 | P@1=0.000 | P@3=0.000 | MRR=0.000 | Rank=None
✅ ContextualPrecision: 0.000
🧠 Reason: The score is 0.00 because the first retrieval context node, despite containing relevant information about admission processes and 'целевое обучение', is not ranked sufficiently high. The input question specifically asks about ' учебные планы и программы вступительных испытаний', and while the node discusses these, it does so within a broader description of the admission process, leading to a lower precision score.
✅ ContextualRecall: 0.000
🧠 Reason: The score is 0.00 because the provided text – ‘Учебный план и программа вступительных испытаний зависят от выбранного направления и уровня обучения.’ – does not align with the retrieval context, which is focused on a comprehensive guide to the admission process. There are no supportive reasons to link this sentence to any node(s) in retrieval context.


================================================================================
FINAL RESULTS (per question)
================================================================================
──────────────────────────────────────────────────
Question: Какие документы необходимы для подачи заявления на поступление?
IR metrics: {'gold_chunks_id': 1, 'hit@1': 0.0, 'hit@3': 0.0, 'precision@1': 0.0, 'precision@3': 0.0, 'mrr': 0.0, 'first_relevant_rank': None}
Judge metrics: {'contextual_precision': {'score': 0, 'reason': "The score is 0.00 because the first retrieval context node, despite containing detailed information about university admissions rules, does not directly answer the user's question about the documents needed to apply. The node focuses on the structure and content of a rules document, rather than the specific required paperwork, leading to a low precision score."}, 'contextual_recall': {'score': 0.0, 'reason': 'The score is 0.00 because the provided text outlines the required documents for applying to undergraduate and postgraduate programs at the Financial University, detailing various categories of documents and their specific requirements. This level of detail does not align with the retrieval context.'}}
──────────────────────────────────────────────────
Question: Каковы сроки приёма документов в этом году?
IR metrics: {'gold_chunks_id': 2, 'hit@1': 0.0, 'hit@3': 0.0, 'precision@1': 0.0, 'precision@3': 0.0, 'mrr': 0.0, 'first_relevant_rank': None}
Judge metrics: {'contextual_precision': {'score': 0, 'reason': "The score is 0.00 because the first retrieval context node, despite describing a formal admissions process with terms like 'конкурсные списки' and 'уникальный код поступающего', does not directly answer the question about 'сроки приёма документов'. The node focuses on the process itself rather than the specific timeframe for document submission, and the question is about the timeframe, not the process."}, 'contextual_recall': {'score': 0.0, 'reason': "The score is 0.00 because the text provides a highly detailed and technical description of the admissions process for ЕПГУ, including specific dates, deadlines, and procedures for both budget and paid places. The information is tightly focused on the procedures and doesn't offer broader contextual information, leading to a low recall score."}}
──────────────────────────────────────────────────
Question: Сколько направлений (специальностей) можно выбрать при подаче заявления?
IR metrics: {'gold_chunks_id': 3, 'hit@1': 0.0, 'hit@3': 0.0, 'precision@1': 0.0, 'precision@3': 0.0, 'mrr': 0.0, 'first_relevant_rank': None}
Judge metrics: {'contextual_precision': {'score': 0, 'reason': "The score is 0.00 because the first retrieval context node provides a detailed analysis of a complex legal document, which is irrelevant to the user's question about the number of specializations available when applying. The node focuses on admissions procedures and quota systems, failing to directly address the user's query about the number of specializations."}, 'contextual_recall': {'score': 0.0, 'reason': "The score is 0.00 because the provided text lacks relevant information to the retrieval context, as indicated by the unsupportive reason referencing a 'comprehensive analysis' which doesn't connect to any specific sentences within the expected output or node(s) in retrieval context."}}
──────────────────────────────────────────────────
Question: Какие вступительные испытания нужно пройти (ЕГЭ, дополнительные экзамены)?
IR metrics: {'gold_chunks_id': 4, 'hit@1': 0.0, 'hit@3': 0.0, 'precision@1': 0.0, 'precision@3': 0.0, 'mrr': 0.0, 'first_relevant_rank': None}
Judge metrics: {'contextual_precision': {'score': 0, 'reason': "The score is 0.00 because the retrieval contexts primarily contain detailed explanations of the admissions process for the Financial University, focusing on regulations and procedures, rather than directly addressing the question about entrance tests (ЕГЭ, дополнительные экзамены). Specifically, nodes like 'Key Sections and Their Focus:' and 'General Admissions (Articles 55-69)' provide irrelevant information about university admissions, and the context's overall scope is far removed from the user's query."}, 'contextual_recall': {'score': 0.0, 'reason': 'The score is 0.00 because the provided text describes the admission process for Russian universities, including specific criteria and exemptions, but none of these details are directly linked to the retrieval context. The context lacks information about university admissions or related processes.'}}
──────────────────────────────────────────────────
Question: Каков минимальный проходной балл по каждому предмету?
IR metrics: {'gold_chunks_id': 5, 'hit@1': 0.0, 'hit@3': 0.0, 'precision@1': 0.0, 'precision@3': 0.0, 'mrr': 0.0, 'first_relevant_rank': None}
Judge metrics: {'contextual_precision': {'score': 0, 'reason': "The score is 0.00 because the first retrieval context node, despite containing the word 'admissions', does not directly answer the question about minimum passing scores. The node focuses on the detailed rules and regulations of the Financial University's admissions process, which is a different topic than the user's query about passing grades."}, 'contextual_recall': {'score': 0.0, 'reason': 'The score is 0.00 because the provided text outlines minimum score requirements for various educational forms and payment types, lacking any direct connection to the retrieval context node(s).'}}
──────────────────────────────────────────────────
Question: Есть ли в университете целевое обучение и как его получить?
IR metrics: {'gold_chunks_id': 6, 'hit@1': 0.0, 'hit@3': 0.0, 'precision@1': 0.0, 'precision@3': 0.0, 'mrr': 0.0, 'first_relevant_rank': None}
Judge metrics: {'contextual_precision': {'score': 0, 'reason': "The score is 0.00 because the first retrieval context node, despite being ranked first, does not address the user's question about targeted education or how to obtain it. Instead, it provides a detailed regulation about the admission process to the Financial University, focusing on administrative and procedural aspects, as stated in the 'reason' field."}, 'contextual_recall': {'score': 0.0, 'reason': 'The score is 0.00 because the text provides a detailed procedural guide for targeted education enrollment, including specific steps and deadlines, but lacks any connection to a retrieval context. The information focuses on the admissions process and requirements, without relating to any broader context.'}}
──────────────────────────────────────────────────
Question: Сколько бюджетных мест выделено на направлении Прикладное машинное обучение?
IR metrics: {'gold_chunks_id': 7, 'hit@1': 0.0, 'hit@3': 0.0, 'precision@1': 0.0, 'precision@3': 0.0, 'mrr': 0.0, 'first_relevant_rank': None}
Judge metrics: {'contextual_precision': {'score': 0, 'reason': 'The score is 0.00 because the first retrieval context node, which states "This document is a detailed regulation outlining the admission process for the Financial University," is irrelevant to the input question about budget places in Applied Machine Learning. The node does not contain information about budget places or the direction of Applied Machine Learning, and therefore, it should be ranked lower than nodes that do contain relevant information.'}, 'contextual_recall': {'score': 0.0, 'reason': 'The score is 0.00 because the provided text only lists the number of budget places and paid educational services places, without any connection to the retrieval context node(s) in retrieval context.'}}
──────────────────────────────────────────────────
Question: Какова стоимость обучения и есть ли скидки?
IR metrics: {'gold_chunks_id': 8, 'hit@1': 0.0, 'hit@3': 0.0, 'precision@1': 0.0, 'precision@3': 0.0, 'mrr': 0.0, 'first_relevant_rank': None}
Judge metrics: {'contextual_precision': {'score': 0, 'reason': "The score is 0.00 because the first retrieval context node, a detailed regulation regarding admissions, is entirely irrelevant to the user's question about the cost of education and discounts. The node's content focuses on the structure and specifics of the Financial University's admissions process, while the input query asks about pricing and potential discounts, creating a significant mismatch in relevance."}, 'contextual_recall': {'score': 0.0, 'reason': 'The score is 0.00 because the provided text offers a detailed explanation of tuition costs and discounts, but lacks connection to any node(s) in retrieval context.'}}
──────────────────────────────────────────────────
Question: Можно ли подать документы онлайн, и как это сделать?
IR metrics: {'gold_chunks_id': 9, 'hit@1': 0.0, 'hit@3': 0.0, 'precision@1': 0.0, 'precision@3': 0.0, 'mrr': 0.0, 'first_relevant_rank': None}
Judge metrics: {'contextual_precision': {'score': 0, 'reason': 'The score is 0.00 because the first node in the retrieval context, which states "The provided text is a complex legal document...", does not directly address the user\'s question about submitting documents online. The node\'s description is overly detailed and focuses on the document\'s nature rather than providing relevant information for answering the query, leading to a low score.'}, 'contextual_recall': {'score': 0.0, 'reason': "The score is 0.00 because the provided text describes how to submit documents online, specifically through the Gosuslugi portal and the university's personal account. However, none of the nodes in retrieval context relate to this process, and the unsupportive reason highlights the text's nature as a legal document, which is not present in the provided output."}}
──────────────────────────────────────────────────
Question: Когда будут опубликованы конкурсные списки и приказы о зачислении?
IR metrics: {'gold_chunks_id': 10, 'hit@1': 0.0, 'hit@3': 0.0, 'precision@1': 0.0, 'precision@3': 0.0, 'mrr': 0.0, 'first_relevant_rank': None}
Judge metrics: {'contextual_precision': {'score': 0, 'reason': "The score is 0.00 because the first retrieval context node, despite describing a university's admission process, does not directly answer the question about the publication dates of contest lists and enrollment orders. The node focuses on the overall process, lacking the specific information requested in the input, and therefore, irrelevant nodes are ranked lower."}, 'contextual_recall': {'score': 0.0, 'reason': 'The score is 0.00 because the provided text describes the timing of publication of admission lists and acceptance orders by universities, referencing updates and publication periods, but lacks direct connection to any specific retrieval context node(s).'}}
──────────────────────────────────────────────────
Question: Есть ли подготовительные курсы для абитуриентов и сколько они стоят?
IR metrics: {'gold_chunks_id': 11, 'hit@1': 0.0, 'hit@3': 0.0, 'precision@1': 0.0, 'precision@3': 0.0, 'mrr': 0.0, 'first_relevant_rank': None}
Judge metrics: {'contextual_precision': {'score': 0, 'reason': "The score is 0.00 because the first retrieval context node, despite containing detailed information about university admissions regulations, does not directly address the user's question about preparatory courses and their cost. The node focuses on the legal framework for admissions, rather than providing practical information about courses themselves, leading to a low score."}, 'contextual_recall': {'score': 0.0, 'reason': 'The score is 0.00 because the expected output provides information about preparatory courses offered by universities, including details on cost, duration, and formats, but none of this information aligns with the retrieval context, which is dominated by legal regulations regarding university admissions (273-FZ).'}}
──────────────────────────────────────────────────
Question: Предоставляется ли общежитие иногородним студентам?
IR metrics: {'gold_chunks_id': 12, 'hit@1': 0.0, 'hit@3': 0.0, 'precision@1': 0.0, 'precision@3': 0.0, 'mrr': 0.0, 'first_relevant_rank': None}
Judge metrics: {'contextual_precision': {'score': 0, 'reason': "The score is 0.00 because the first retrieval context node, a detailed legal document, does not directly address the question about student housing. The node's 'reason' states it outlines admission processes and regulations, which is irrelevant to the user's inquiry about housing provisions."}, 'contextual_recall': {'score': 0.0, 'reason': "The score is 0.00 because the expected output provides specific details about dormitory availability for out-of-town students, including distance requirements and application procedures (sentence 1-2), which are not reflected in the retrieval context. The unsupportive reason highlights the document's formal nature, further distancing it from any potential relevance to the retrieval context."}}
──────────────────────────────────────────────────
Question: Какие льготы и особые права при поступлении предусмотрены (олимпиады, инвалидность и т.д.)?
IR metrics: {'gold_chunks_id': 13, 'hit@1': 0.0, 'hit@3': 0.0, 'precision@1': 0.0, 'precision@3': 0.0, 'mrr': 0.0, 'first_relevant_rank': None}
Judge metrics: {'contextual_precision': {'score': 0, 'reason': "The score is 0.00 because the first retrieval context node, which states 'The document is lengthy, detailed, and uses legal terminology, indicating its purpose as a formal set of rules governing the admissions process.', does not directly address the user's question about benefits and rights related to admissions, such as those concerning olympiads or disabilities. The node's focus on the document's structure and legal nature makes it irrelevant to the query's specific request."}, 'contextual_recall': {'score': 0.0, 'reason': "The score is 0.00 because the provided text is a lengthy legal description of benefits and rights related to university admissions, referencing specific legislation and regulations (Federal Law No. 273-FZ), and does not align with any retrieval context. The document's detailed nature and use of legal terminology suggests a lack of relevance to the retrieval context."}}
──────────────────────────────────────────────────
Question: Можно ли перевестись с платного обучения на бюджетное?
IR metrics: {'gold_chunks_id': 14, 'hit@1': 0.0, 'hit@3': 0.0, 'precision@1': 0.0, 'precision@3': 0.0, 'mrr': 0.0, 'first_relevant_rank': None}
Judge metrics: {'contextual_precision': {'score': 0, 'reason': "The score is 0.00 because the retrieval contexts primarily contain a detailed legal document about university admissions, and the input question is about transferring between tuition types. The first node in the retrieval contexts, 'The provided text is a legal document...', does not address the core query about transferring between educational funding options, and therefore the irrelevant nodes are ranked higher than the relevant ones."}, 'contextual_recall': {'score': 0.0, 'reason': "The score is 0.00 because the expected output describes a process for transferring from paid to subsidized education within a university, detailing conditions and procedures, but there's no direct connection to any node(s) in retrieval context."}}
──────────────────────────────────────────────────
Question: Есть ли возможность учиться заочно/очно‑заочно на выбранной специальности?
IR metrics: {'gold_chunks_id': 15, 'hit@1': 0.0, 'hit@3': 0.0, 'precision@1': 0.0, 'precision@3': 0.0, 'mrr': 0.0, 'first_relevant_rank': None}
Judge metrics: {'contextual_precision': {'score': 0, 'reason': 'The score is 0.00 because the retrieval contexts primarily discuss university admission procedures and ranking criteria, which doesn\'t directly address the question about studying part-time or full-time. Specifically, the first node states, "The text outlines procedures for application, ranking, and admission, including specific priorities and criteria for evaluating candidates," and this is not relevant to the user\'s query about learning opportunities.'}, 'contextual_recall': {'score': 0.0, 'reason': 'The score is 0.00 because the provided text simply states that the form of study depends on the field of study and offers resources for finding information, lacking any connection to the retrieval context node(s).'}}
──────────────────────────────────────────────────
Question: Какова продолжительность обучения по моей программе (бакалавриат/специалитет/магистратура)?
IR metrics: {'gold_chunks_id': 16, 'hit@1': 0.0, 'hit@3': 0.0, 'precision@1': 0.0, 'precision@3': 0.0, 'mrr': 0.0, 'first_relevant_rank': None}
Judge metrics: {'contextual_precision': {'score': 0, 'reason': 'The score is 0.00 because the retrieval contexts primarily contain a legal document detailing university admission procedures, and this document does not directly answer the question about the duration of study for a specific program. Specifically, the node\'s \'reason\' states, "The text\'s structure, terminology, and focus on specific dates, quotas, and ranking methods strongly indicate a legal or regulatory document related to university admissions."'}, 'contextual_recall': {'score': 0.0, 'reason': 'The score is 0.00 because the text provides a straightforward explanation of educational program durations across different levels (бакалавриат, специалитет, магистратура) – node(s) in retrieval context do not address this specific information about academic program timelines.'}}
──────────────────────────────────────────────────
Question: Есть ли военная кафедра в университете?
IR metrics: {'gold_chunks_id': 17, 'hit@1': 0.0, 'hit@3': 0.0, 'precision@1': 0.0, 'precision@3': 0.0, 'mrr': 0.0, 'first_relevant_rank': None}
Judge metrics: {'contextual_precision': {'score': 0, 'reason': 'The score is 0.00 because the first retrieval context node, which states "The text is dense with legal terms, references to specific articles of a law (Federal Law No. 273-FZ), and detailed procedures," is not directly relevant to the user\'s question about a military department in a university. The node focuses on a complex legal document, while the input query is a simple inquiry about the existence of a specific academic department.'}, 'contextual_recall': {'score': 0.0, 'reason': 'The score is 0.00 because the provided text describes the operation of a military training center at the Financial University, detailing training programs for sergeants and officers. However, there are no relevant node(s) in retrieval context to directly relate to this information, resulting in a low contextual recall score.'}}
──────────────────────────────────────────────────
Question: Какие возможности стажировок и трудоустройства предлагает вуз?
IR metrics: {'gold_chunks_id': 18, 'hit@1': 0.0, 'hit@3': 0.0, 'precision@1': 0.0, 'precision@3': 0.0, 'mrr': 0.0, 'first_relevant_rank': None}
Judge metrics: {'contextual_precision': {'score': 0, 'reason': "The score is 0.00 because the first retrieval context node, despite containing information about admissions processes, does not directly address the input question about internship and employment opportunities offered by the university. The node focuses on the rules and regulations governing admissions, including olympiad results, which is a tangential topic and fails to provide relevant information about the university's offerings for internships and employment."}, 'contextual_recall': {'score': 0.0, 'reason': "The score is 0.00 because the provided text describes career services offered by a university (node(s) in retrieval context), including internships, career events, and job placement assistance, but it doesn't align with the expected output's focus on olympiad results and special privileges."}}
──────────────────────────────────────────────────
Question: Можно ли поменять выбранное направление после подачи заявления?
IR metrics: {'gold_chunks_id': 19, 'hit@1': 0.0, 'hit@3': 0.0, 'precision@1': 0.0, 'precision@3': 0.0, 'mrr': 0.0, 'first_relevant_rank': None}
Judge metrics: {'contextual_precision': {'score': 0, 'reason': "The score is 0.00 because the retrieval contexts, particularly the first node, are overly descriptive and focus on the document's structure and legal nature, rather than directly addressing the user's question about changing a direction after submitting an application. The subsequent nodes, while providing further details about the document, do not offer relevant information to answer the query, and the nodes are ranked in a way that prioritizes these irrelevant descriptions."}, 'contextual_recall': {'score': 0.0, 'reason': "The score is 0.00 because the provided text is a detailed procedural document outlining changes and procedures related to admissions, with no clear connection to a retrieval context. Node(s) in retrieval context do not contain information relevant to the specifics of the document's content."}}
──────────────────────────────────────────────────
Question: Где можно ознакомиться с учебными планами и программами вступительных испытаний?
IR metrics: {'gold_chunks_id': 20, 'hit@1': 0.0, 'hit@3': 0.0, 'precision@1': 0.0, 'precision@3': 0.0, 'mrr': 0.0, 'first_relevant_rank': None}
Judge metrics: {'contextual_precision': {'score': 0, 'reason': "The score is 0.00 because the first retrieval context node, despite containing relevant information about admission processes and 'целевое обучение', is not ranked sufficiently high. The input question specifically asks about ' учебные планы и программы вступительных испытаний', and while the node discusses these, it does so within a broader description of the admission process, leading to a lower precision score."}, 'contextual_recall': {'score': 0.0, 'reason': 'The score is 0.00 because the provided text – ‘Учебный план и программа вступительных испытаний зависят от выбранного направления и уровня обучения.’ – does not align with the retrieval context, which is focused on a comprehensive guide to the admission process. There are no supportive reasons to link this sentence to any node(s) in retrieval context.'}}

Process finished with exit code 0

```