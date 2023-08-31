from re import split

from sklearn.model_selection import train_test_split
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, Seq2SeqTrainingArguments, Seq2SeqTrainer


# 从文本文件中读取训练数据
def read_training_data(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
    return [line.strip().split("\t") for line in lines]


# 定义训练数据文件路径
training_data_path = "training_data.txt"

# 读取训练数据
data = read_training_data(training_data_path)

# 分割数据集
train_data, val_data = train_test_split(data, test_size=0.2, random_state=42)

# 加载预训练的变换器模型和分词器
model_name = "Helsinki-NLP/opus-mt-zh-en"  # 预训练的中英翻译模型
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# Prepare inputs and targets using tokenizer
train_inputs = tokenizer([item[0].split(" ")[0] for item in train_data], padding=True, truncation=True,
                         return_tensors="pt")
train_targets = tokenizer([item[0].split(" ")[len(item[0].split(" ")) - 1] for item in train_data], padding=True,
                          truncation=True, return_tensors="pt")

# Attach targets to inputs
train_inputs["input_ids"] = train_targets["input_ids"]


# Define training arguments
training_args = Seq2SeqTrainingArguments(
    output_dir="./corrector_model",
    evaluation_strategy="steps",
    eval_steps=200,
    save_steps=1000,
    logging_steps=100,
    num_train_epochs=3,
    learning_rate=1e-4,
    per_device_train_batch_size=4,
    save_total_limit=2,
)

# Define trainer
trainer = Seq2SeqTrainer(
    model=model,
    args=training_args,
    train_dataset=train_inputs
)

# Train the model
trainer.train()
