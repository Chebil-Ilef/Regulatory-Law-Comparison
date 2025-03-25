import requests

def compare_chunks_with_ollama(new_chunk, old_chunk, model="deepseek-r1:8b"):
    prompt = f"""
    You are a compliance analyst. Compare the following two regulatory clauses.

    Old Clause:
    """
    {old_chunk.strip()}
    """

    New Clause:
    """
    {new_chunk.strip()}
    """

    Please:
    - Summarize the key differences
    - Classify the change as one of: [No Change, Minor Update, Major Update, Removed, Added]
    - Return the result as a JSON with keys: "summary", "change_type"
    """

    response = requests.post("http://localhost:11434/api/generate", json={
        "model": model,
        "prompt": prompt,
        "stream": False
    })

    if response.status_code == 200:
        try:
            result_text = response.json().get("response", "{}")
            return result_text.strip()
        except Exception as e:
            return f"Error parsing Ollama response: {e}"
    else:
        return f"Error: {response.status_code} - {response.text}"


if __name__ == "__main__":
    old_example = "Patients have the right to access their medical data within 30 days."
    new_example = "Patients must be granted access to their medical data within 15 days."

    result = compare_chunks_with_ollama(new_example, old_example)
    print(result)