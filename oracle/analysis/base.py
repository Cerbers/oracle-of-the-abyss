from oracle.poem_model import Poem
from oracle.domain_objects import Stanza


stanzas = []

def poetic_devices(poem: Poem) -> list[Stanza]:
    for stanza in poem.stanzas:
        stanzas.append(stanza)
    return stanzas
 

def anaphora(poem_stanza: Stanza) -> None: 
    pass