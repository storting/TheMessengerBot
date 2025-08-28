from transformers import BertTokenizer, TFBertModel

# Определяем путь к модели Small BERT
MODEL_NAME = 'google/bert_uncased_L-4_H-512_A-8'

# Загрузим токенизатор и модель
tokenizer = BertTokenizer.from_pretrained(MODEL_NAME)
model = TFBertModel.from_pretrained(MODEL_NAME)

# Пример ввода
text = "Этот пример показывает использование Small BERT."

# Токенизируем входной текст
encoded_input = tokenizer(text, return_tensors='tf')  # Возвращает тензоры формата TensorFlow

# Прогоняем через модель
output = model(encoded_input)

# Распечатываем выходные значения
print(output)