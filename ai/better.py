
model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a witty and imaginative assistant. Generate playful, creative, and descriptive filenames "
                    "for digital products based on provided prompts."
                ),
            },
            {
                "role": "user",
                "content": f"Create a unique filename for this design prompt: '{prompt}'",
            },
        ],
        max_tokens=20,
        temperature=0.7