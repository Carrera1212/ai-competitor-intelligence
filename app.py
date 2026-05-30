from transformers import pipeline

print("--- STARTING AI CONTAINER ---")

# Initialize the pipeline
classifier = pipeline(
    "sentiment-analysis", 
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

# Test text
text = "Learning Docker to land a high-paying job is an incredible feeling!"

# Run prediction
result = classifier(text)[0]

print(f"\nText: {text}")
print(f"Result: {result['label']} ({result['score']:.2%})\n")
print("--- CONTAINER TASK FINISHED ---")