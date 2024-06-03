import os
import argparse
import torch
from peft import LoraConfig
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments, BitsAndBytesConfig
)
from datasets import load_dataset
from trl import SFTTrainer


def parse_args():
    parser = argparse.ArgumentParser(description="Train a language model.")
    parser.add_argument('--model_name', type=str, default='gpt2', help='Name of the model to use.')
    parser.add_argument('--data_dir', type=str, default='./train.csv', help='Name of the dataset to use.')
    parser.add_argument('--output_dir', type=str, default='./results', help='Directory to save the model and tokenizer.')
    parser.add_argument('--adapter_id', type=str, default='lora_adapter_it', help='Lora Adapter Model Id')
    parser.add_argument('--epochs', type=int, default=3, help='Number of training epochs.')
    parser.add_argument('--batch_size', type=int, default=8, help='Batch size for training.')
    parser.add_argument('--learning_rate', type=float, default=5e-5, help='Learning rate for training.')
    parser.add_argument('--max_seq_length', type=int, default=512, help='Maximum sequence length.')
    return parser.parse_args()

def main():
    args = parse_args()

    # Load the dataset
    dataset = load_dataset("csv", data_files=args.data_dir)
    print(f"Dataset loaded: {args.dataset_name}")

    # Load the tokenizer
    tokenizer = AutoTokenizer.from_pretrained(args.model_name, add_eos_token=True)
    print(f"Tokenizer loaded: {args.model_name}")

    def gemma_formatting(example):
        if example['input'] and len(example['input']) > 0:
            text = f'''user\n{example['instruction']}\n{example['input']}\nmodel\n{example['output']}{tokenizer.eos_token}'''
        else:
            text = f'''user\n{example['instruction']}\n\nmodel\n{example['output']}{tokenizer.eos_token}'''
        return {'prompt': text}

    dataset = dataset.map(lambda samples: tokenizer(samples["prompt"]), batched=True)
    train_data = dataset["train"]

    # Set Lora
    lora_config = LoraConfig(
        r=6,  # 학습 가능한 파라미터들을 정의한다.
        lora_alpha=8,
        lora_dropout=0.05,
        target_modules=["q_proj", "o_proj", "k_proj", "v_proj", "gate_proj", "up_proj", "down_proj"],  # lora로 바꿀 모
        task_type="CAUSAL_LM",
    )
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16
    )

    # Load the model
    model = AutoModelForCausalLM.from_pretrained(
        args.model_name,
        quantization_config=bnb_config,
        device_map="auto"
    )
    print(f"Model loaded: {args.model_name}")

    # Set up the training arguments
    training_args = TrainingArguments(
        output_dir=args.output_dir,
        num_train_epochs=args.epochs,
        per_device_train_batch_size=args.batch_size,
        per_device_eval_batch_size=args.batch_size,
        optim="paged_adamw_8bit",
        warmup_steps=500,
        weight_decay=0.01,
        logging_dir='./logs',
        logging_steps=10,
        learning_rate=args.learning_rate,
        fp16=True,
        push_to_hub=False,
        report_to='none',
        do_train=True,
        seed=2024
    )

    # Set up the trainer
    trainer = SFTTrainer(
        model=model,
        train_dataset=train_data,
        max_seq_length=args.max_seq_length,
        args=training_args,
        dataset_text_field="prompt",
        peft_config=lora_config,
        # data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False),
    )

    # Train the model
    trainer.train()

    # Save the model and tokenizer
    trainer.model.save_pretrained(os.path.join(args.output_dir, args.adapter_id))

if __name__ == "__main__":
    main()
