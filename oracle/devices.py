from oracle.poem_model import Poem

# Poem Level poetic devices

def holder_for_poetic_device_analysis(poem: Poem):
    """Placeholder for future poetic device analysis at the poem level."""
    poem_text = poem.text

    anaphora_results = analyze_anaphora(poem_text)

    return anaphora_results

def analyze_anaphora(poem_text: str, min_chain_length = 3):
    container = []
    for line in poem_text.splitlines():
        stripped_line = line.strip()
        if stripped_line:
            first_words = stripped_line.split()
            if len(first_words) >= 2:
                container.append(tuple(first_words[:2]))

    chains = []
    if not container:
        return chains
    current_chain = [container[0]]
    for pair in container[1:]:
        if pair == current_chain[-1]:
            current_chain.append(pair)
        else:
            if len(current_chain) > 1:
                chains.append(current_chain)
            current_chain = [pair]

    if len(current_chain) >= min_chain_length:
        chains.append(current_chain)
    return chains