
# Conditions for syllable pattern detection
# If a stanza in a poem has all lines with same syllable count, then the confidence raises by 1
# If a stanza has less than 50% of lines with the same syllable count, then the confidence drops by 1

confidence = 0

def confidence_up():
    global confidence
    confidence += 1

def confidence_down():
    global confidence
    confidence -= 1

# BASE ALGORITHM FOR SIMPLE SYLLABLE PATTERN DETECTION

