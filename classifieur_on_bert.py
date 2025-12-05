from transformers import CamembertTokenizerFast, TFCamembertForSequenceClassification
import json
from sklearn.model_selection import train_test_split
import torch
import transformers
import tensorflow as tf


#Chargement du corpus et split 

with open('/home/maiwenn/Documents/M1S2/enrichissementcorpus/contextes_on.json') as corpus_json :
    data = json.load(corpus_json)

corpus = []
labels = []
for texte_dict in data :
    texte = texte_dict['contexte_gauche'] + texte_dict['contexte_droit']
    corpus.append(texte)
    label = texte_dict['label']
    labels.append(label)
corpus_context = corpus

unique_labels = sorted(set(labels))
label2id = {label: idx for idx, label in enumerate(unique_labels)}
id2label = {idx: label for label, idx in label2id.items()}

labels_id = [label2id[l] for l in labels]

corpus_train, corpus_val, labels_train, labels_val = train_test_split(corpus_context, labels_id, test_size=0.20)
corpus_val, corpus_test, labels_val, labels_test = train_test_split(corpus_val, labels_val, test_size=0.50)


#Tokenization

tokenizer = CamembertTokenizerFast.from_pretrained("camembert-base")

def tokenize(texts):
    return tokenizer(
        texts,
        padding="max_length",
        truncation=True,
        max_length=256,
        return_tensors="tf"
    )

train_tok = tokenize(corpus_train)
val_tok   = tokenize(corpus_val)
test_tok  = tokenize(corpus_test)


train_dataset = tf.data.Dataset.from_tensor_slices((
    dict(train_tok),
    labels_train
)).shuffle(1000).batch(8)

val_dataset = tf.data.Dataset.from_tensor_slices((
    dict(val_tok),
    labels_val
)).batch(8)

test_dataset = tf.data.Dataset.from_tensor_slices((
    dict(test_tok),
    labels_test
)).batch(8)

#Modèle 

model = TFCamembertForSequenceClassification.from_pretrained("camembert-base",
                                                             num_labels=2,  
                                                             id2label=id2label,
                                                             label2id=label2id
                                                             )


loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
optimizer = tf.keras.optimizers.Adam(learning_rate=2e-5)

model.compile(
    optimizer, 
    loss, 
    metrics=["accuracy"]
)

model.fit(
    train_dataset,
    validation_data=val_dataset,
    epochs=3
)

print("\nÉvaluation sur le test set :")
model.evaluate(test_dataset)



'''
training_args = TrainingArguments(
    output_dir="./classifieur_on",
    evaluation_strategy="epoch",
    save_strategy="epoch",
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=3,
    learning_rate=2e-5,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_tok["train"],
    eval_dataset=val_tok["test"],
)

trainer.train()
'''